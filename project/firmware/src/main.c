#include "clock.h"
#include "panel.h"
#include "state.h"

#include <errno.h>
#include <nrf.h>
#include <hal/nrf_rramc.h>
#include <string.h>
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/drivers/adc.h>
#include <zephyr/drivers/flash.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/i2c.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/drivers/spi.h>
#include <zephyr/init.h>
#include <zephyr/kernel.h>
#include <zephyr/storage/flash_map.h>

#define USER DT_PATH(zephyr_user)
static const struct gpio_dt_spec done = GPIO_DT_SPEC_GET(USER, done_gpios);
static const struct gpio_dt_spec measure_en = GPIO_DT_SPEC_GET(USER, measure_enable_gpios);
static const struct gpio_dt_spec keys[] = {
	GPIO_DT_SPEC_GET_BY_IDX(USER, button_gpios, 0), GPIO_DT_SPEC_GET_BY_IDX(USER, button_gpios, 1),
	GPIO_DT_SPEC_GET_BY_IDX(USER, button_gpios, 2)
};
static const struct gpio_dt_spec dc = GPIO_DT_SPEC_GET(USER, epd_dc_gpios);
static const struct gpio_dt_spec reset = GPIO_DT_SPEC_GET(USER, epd_reset_gpios);
static const struct gpio_dt_spec busy = GPIO_DT_SPEC_GET(USER, epd_busy_gpios);
static const struct spi_dt_spec epd_spi = SPI_DT_SPEC_GET(DT_NODELABEL(panel),
	SPI_OP_MODE_MASTER | SPI_TRANSFER_MSB | SPI_WORD_SET(8));
static const struct adc_dt_spec battery = ADC_DT_SPEC_GET(USER);
static const struct device *const bme = DEVICE_DT_GET(DT_NODELABEL(bme));
static const struct i2c_dt_spec bme_i2c = I2C_DT_SPEC_GET(DT_NODELABEL(bme));
static const struct device *const rram = FIXED_PARTITION_DEVICE(panel_state);
static uint8_t framebuffer[ASTRA_FRAME_BYTES] __aligned(4);
static uint8_t boot_keys;
static int early_status;

/* Inspect this named RAM object through SWD before or during astra_done_hook(). */
struct bringup_report {
	uint32_t version, part, variant, package;
	int32_t gpio, rtc, sensor, adc, journal, panel, sleep, radio;
	uint32_t sequence, timestamp;
	uint16_t battery_mv;
	int16_t temperature;
	uint8_t keys, rtc_alarm, mode, reserved;
	uint32_t done_pulses;
};
volatile struct bringup_report astra_report;

static int sample_keys(uint8_t *mask)
{
	for (size_t i = 0; i < ARRAY_SIZE(keys); i++) {
		int value = gpio_pin_get_dt(&keys[i]);
		if (value < 0) { return value; }
		if (value) { *mask |= (uint8_t)BIT(i); }
	}
	return 0;
}

static int capture_keys(void)
{
	early_status = gpio_pin_configure_dt(&done, GPIO_OUTPUT_INACTIVE);
	if (!early_status) { early_status = gpio_pin_configure_dt(&measure_en, GPIO_OUTPUT_INACTIVE); }
	for (size_t i = 0; !early_status && i < ARRAY_SIZE(keys); ++i) {
		early_status = gpio_pin_configure_dt(&keys[i], GPIO_INPUT);
	}
	if (!early_status) { early_status = sample_keys(&boot_keys); }
	return 0;
}
/* Capture after PRE_KERNEL_1 GPIO priority 40 and before POST_KERNEL sensor probe. */
SYS_INIT(capture_keys, PRE_KERNEL_1, 41);

static int sample_divider(uint16_t *millivolts)
{
	if (!adc_is_ready_dt(&battery)) { return -ENODEV; }
	int err = adc_channel_setup_dt(&battery);
	int16_t raw;
	struct adc_sequence sample = {.buffer = &raw, .buffer_size = sizeof(raw), .calibrate = true};
	if (!err) { err = adc_sequence_init_dt(&battery, &sample); }
	if (!err) { err = adc_read_dt(&battery, &sample); }
	if (err) { return err; }
	int32_t scaled = raw;
	err = adc_raw_to_millivolts_dt(&battery, &scaled);
	if (err) { return err; }
	if (scaled < 0 || scaled > 3000) { return -ERANGE; }
	*millivolts = (uint16_t)(scaled * 2);
	return 0;
}

static int measure_battery(uint16_t *millivolts)
{
	int err = gpio_pin_set_dt(&measure_en, 1);
	if (!err) {
		k_msleep(5);
		err = sample_divider(millivolts);
	}
	int clear_err = gpio_pin_set_dt(&measure_en, 0);
	k_msleep(1);
	return err ? err : clear_err;
}

static int weather(struct scene *scene)
{
	if (!device_is_ready(bme)) { return -ENODEV; }
	uint8_t id = 0;
	int err = i2c_reg_read_byte_dt(&bme_i2c, 0xd0, &id);
	if (err) { return err; }
	if (id != 0x60) { return -ENODEV; } /* BMP280 is pressure-only. */
	err = sensor_sample_fetch(bme);
	struct sensor_value t, p, h;
	if (!err) { err = sensor_channel_get(bme, SENSOR_CHAN_AMBIENT_TEMP, &t); }
	if (!err) { err = sensor_channel_get(bme, SENSOR_CHAN_PRESS, &p); }
	if (!err) { err = sensor_channel_get(bme, SENSOR_CHAN_HUMIDITY, &h); }
	if (err) { return err; }
	int32_t temp_c100 = sensor_value_to_milli(&t) / 10;
	int32_t rh100 = sensor_value_to_milli(&h) / 10;
	int32_t pascals = sensor_value_to_milli(&p); /* Zephyr SENSOR_CHAN_PRESS uses kPa. */
	if (temp_c100 < -4000 || temp_c100 > 8500 || rh100 < 0 || rh100 > 10000 ||
	    pascals < 30000 || pascals > 110000) { return -ERANGE; }
	scene->temp_centi_c = (int16_t)temp_c100;
	scene->humidity_centi_pct = (uint16_t)rh100;
	scene->pressure_pa = (uint32_t)pascals;
	return 0;
}

static int panel_setup(void)
{
	if (!spi_is_ready_dt(&epd_spi) || !gpio_is_ready_dt(&dc) || !gpio_is_ready_dt(&reset) ||
	    !gpio_is_ready_dt(&busy)) { return -ENODEV; }
	int err = gpio_pin_configure_dt(&dc, GPIO_OUTPUT_INACTIVE);
	if (!err) { err = gpio_pin_configure_dt(&reset, GPIO_OUTPUT_INACTIVE); }
	if (!err) { err = gpio_pin_configure_dt(&busy, GPIO_INPUT); }
	return err;
}

static int panel_send(void *ctx, bool data, const uint8_t *buf, size_t n)
{
	ARG_UNUSED(ctx);
	struct spi_buf part = {.buf = (void *)buf, .len = n};
	struct spi_buf_set set = {.buffers = &part, .count = 1};
	int err = gpio_pin_set_dt(&dc, data);
	if (!err) {
		err = spi_write_dt(&epd_spi, &set);
		/* CS is high upon synchronous completion. Meet SSD1683 tCSHIGH. */
		k_busy_wait(1);
	}
	return err;
}

static int panel_reset_pin(void *ctx, bool asserted)
{
	ARG_UNUSED(ctx);
	return gpio_pin_set_dt(&reset, asserted);
}
static int panel_busy_pin(void *ctx) { ARG_UNUSED(ctx); return gpio_pin_get_dt(&busy); }
static void panel_delay(void *ctx, unsigned ms) { ARG_UNUSED(ctx); k_msleep(ms); }
static uint32_t panel_time(void *ctx) { ARG_UNUSED(ctx); return k_uptime_get_32(); }

static const struct panel_io screen = {
	.send = panel_send, .reset = panel_reset_pin, .busy = panel_busy_pin,
	.delay_ms = panel_delay, .time_ms = panel_time
};

static int read_slot(void *ctx, size_t address, void *data, size_t length)
{
	ARG_UNUSED(ctx);
	return flash_read(rram, FIXED_PARTITION_OFFSET(panel_state) + address, data, length);
}
static int write_slot(void *ctx, size_t address, const void *data, size_t length)
{
	ARG_UNUSED(ctx);
	int err = flash_write(rram, FIXED_PARTITION_OFFSET(panel_state) + address, data, length);
	if (err) { return err; }
	/* Subsequent flash_read alone cannot distinguish data in an in-flight buffer. */
	uint32_t start = k_uptime_get_32();
	while (!nrf_rramc_empty_buffer_check(NRF_RRAMC) || !nrf_rramc_ready_check(NRF_RRAMC)) {
		if (k_uptime_get_32() - start >= 20) { return -ETIMEDOUT; }
		k_busy_wait(5);
	}
	return 0;
}
static const struct journal journal = {
	.slots = FIXED_PARTITION_SIZE(panel_state)/sizeof(struct slot), .read = read_slot, .write = write_slot
};
BUILD_ASSERT(FIXED_PARTITION_SIZE(panel_state) % sizeof(struct slot) == 0);

static void update_panel(const struct scene *now)
{
	struct history prior, pending;
	if (!device_is_ready(rram)) { astra_report.journal = -ENODEV; return; }
	astra_report.journal = journal_find(&journal, &prior);
	if (astra_report.journal) { return; }
	enum refresh mode = choose_refresh(now, &prior);
	astra_report.mode = (uint8_t)mode;
	if (mode == REFRESH_SKIP) { return; }
	if (mode != REFRESH_DEFER) {
		astra_report.panel = panel_setup();
		if (astra_report.panel) { return; }
	}
	astra_report.journal = journal_prepare(&journal, &prior, now, mode, &pending);
	if (astra_report.journal) { return; }
	astra_report.sequence = pending.intent.generation;
	if (mode == REFRESH_DEFER) { return; }
	astra_report.panel = panel_refresh(&screen, mode, &prior.intent.scene, now, framebuffer);
	if (astra_report.panel) { return; }
	astra_report.journal = journal_commit(&journal, &pending);
	if (!astra_report.journal && prior.damaged && mode == REFRESH_FULL) {
		astra_report.journal = journal_clean_damaged(&journal);
	}
	astra_report.sleep = panel_sleep(&screen);
}

static K_SEM_DEFINE(radio_ready, 0, 1);
static int radio_status;
static void ready(int err) { radio_status = err; k_sem_give(&radio_ready); }
static int advertise_test(void)
{
	int err = bt_enable(ready);
	if (!err) { err = k_sem_take(&radio_ready, K_SECONDS(3)); }
	if (!err) { err = radio_status; }
	if (err) { return err; }
	const struct bt_data payload[] = {
		BT_DATA_BYTES(BT_DATA_FLAGS, BT_LE_AD_NO_BREDR),
		BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME, sizeof(CONFIG_BT_DEVICE_NAME) - 1),
	};
	err = bt_le_adv_start(BT_LE_ADV_NCONN, payload, ARRAY_SIZE(payload), NULL, 0);
	if (err) { return err; }
	k_msleep(2000);
	return bt_le_adv_stop();
}

__attribute__((noinline,used)) void astra_done_hook(void)
{
	__asm__ volatile ("" ::: "memory");
}

int main(void)
{
	astra_report = (struct bringup_report){ .version = 1, .part = NRF_FICR->INFO.PART,
		.variant = NRF_FICR->INFO.VARIANT, .package = NRF_FICR->INFO.PACKAGE, .gpio = early_status,
		.journal = -ENODATA, .panel = -ENODATA, .sleep = -ENODATA, .radio = -ENODATA };
	struct scene sample = { .buttons = boot_keys };
	k_msleep(5);
	if (!early_status) { astra_report.gpio = sample_keys(&sample.buttons); }
	astra_report.keys = sample.buttons;
	struct clock_reading reading = {0};
	astra_fixture_hook();
	for (unsigned attempt = 0; attempt < 3; ++attempt) {
		astra_report.rtc = clock_read_arm(&reading);
		if (!astra_report.rtc) { break; }
		k_msleep(25);
	}
	if ((reading.reset || astra_report.rtc) && sample.buttons) {
		/* The three wake RCs can all indicate a key on first AON rise. */
		uint32_t start = k_uptime_get_32();
		do {
			uint8_t levels = 0;
			if (sample_keys(&levels) || !levels) { break; }
			k_msleep(20);
		} while (k_uptime_get_32() - start < 2000);
		sample.buttons = 0;
		astra_report.keys = 0;
	}
	astra_report.rtc_alarm = reading.was_alarm;
	astra_report.timestamp = sample.seconds = reading.seconds;
	sample.flags = (reading.utc ? ASTRA_UTC : 0) | (reading.reset ? ASTRA_CLOCK_RESET : 0);
	astra_report.adc = measure_battery(&sample.battery_mv);
	astra_report.battery_mv = sample.battery_mv;
	astra_report.sensor = weather(&sample);
	astra_report.temperature = sample.temp_centi_c;
	if (!astra_report.gpio && !astra_report.rtc && !astra_report.adc && !astra_report.sensor) {
		update_panel(&sample);
	}
	if ((sample.buttons & BIT(2)) && !astra_report.adc && sample.battery_mv >= 3300 &&
	    sample.battery_mv <= 4350) {
		astra_report.radio = advertise_test();
	}
	astra_done_hook();
	/* Re-arm after a debugger stop or slow display. While a fixture holds manual
	 * wake high, keep an upcoming alarm scheduled and send a fresh DONE after release. */
	uint32_t armed_at = 0;
	for (;;) {
		uint32_t now = k_uptime_get_32();
		if (!astra_report.done_pulses || now - armed_at >= 14u * 60u * 1000u) {
			struct clock_reading again = {0};
			int arm_err = clock_read_arm(&again);
			if (arm_err) { astra_report.rtc = arm_err; }
			armed_at = now;
		}
		++astra_report.done_pulses;
		(void)gpio_pin_set_dt(&done, 1);
		k_msleep(10);
		(void)gpio_pin_set_dt(&done, 0);
		k_msleep(astra_report.done_pulses < 10 ? 90 : 990);
	}
}
