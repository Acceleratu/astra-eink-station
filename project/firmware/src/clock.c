#include "clock.h"
#include <errno.h>
#include <string.h>
#include <zephyr/drivers/i2c.h>
#include <zephyr/kernel.h>

static const struct i2c_dt_spec rtc = I2C_DT_SPEC_GET(DT_NODELABEL(external_rtc));
volatile struct time_mailbox astra_time_mailbox;

__attribute__((noinline,used)) void astra_fixture_hook(void)
{
	__asm__ volatile ("" ::: "memory");
}

static int registers(uint8_t addr, uint8_t *data, size_t n)
{
	return i2c_write_read_dt(&rtc, &addr, 1, data, n);
}

static int set_time(const struct calendar *t, bool utc)
{
	uint8_t burst[8] = {0x04};
	uint32_t ignored;
	if (!calendar_seconds(t, &ignored)) {
		return -EINVAL;
	}
	/* Invalidate UTC trust before changing calendar, including interruption mid-write. */
	int err = i2c_reg_write_byte_dt(&rtc, 0x03, 0);
	if (err) {
		return err;
	}
	calendar_encode(t, &burst[1]);
	err = i2c_write_dt(&rtc, burst, sizeof(burst));
	if (!err && utc) {
		uint8_t raw[7];
		uint32_t wrote, read;
		struct calendar check;
		err = registers(0x04, raw, sizeof(raw));
		if (!err && (!calendar_decode(raw, &check) || !calendar_seconds(&check, &read) ||
			     !calendar_seconds(t, &wrote) || (read != wrote && read != wrote + 1))) {
			err = -EIO;
		}
		if (!err) {
			err = i2c_reg_write_byte_dt(&rtc, 0x03, 0xe7);
		}
	}
	return err;
}

static int start_relative_clock(void)
{
	/* NXP power-up procedure: software reset only after loss of clock integrity. */
	int err = i2c_reg_write_byte_dt(&rtc, 0x00, 0x58);
	if (err) {
		return err;
	}
	k_msleep(5);
	err = i2c_reg_write_byte_dt(&rtc, 0x00, 0); /* 7 pF, 24 h, running */
	if (!err) { err = i2c_reg_write_byte_dt(&rtc, 0x01, 0x07); }
	struct calendar epoch = {.year = 2000, .month = 1, .day = 1};
	/* OS is sticky and may reassert until the crystal oscillates. */
	for (int n = 0; !err && n < 40; ++n) {
		err = set_time(&epoch, false);
		if (err) {
			break;
		}
		k_msleep(50);
		uint8_t seconds;
		err = i2c_reg_read_byte_dt(&rtc, 0x04, &seconds);
		if (!err && !(seconds & 0x80)) {
			return 0;
		}
	}
	return err ? err : -ETIMEDOUT;
}

int clock_read_arm(struct clock_reading *reading)
{
	if (!i2c_is_ready_dt(&rtc)) { return -ENODEV; }
	uint8_t ctrl2, raw[7], ram;
	int err = i2c_reg_read_byte_dt(&rtc, 0x01, &ctrl2);
	if (err) {
		(void)i2c_recover_bus(rtc.bus);
		err = i2c_reg_read_byte_dt(&rtc, 0x01, &ctrl2);
	}
	if (err) { return err; }
	reading->was_alarm |= !!(ctrl2 & 0x40);
	err = i2c_reg_write_byte_dt(&rtc, 0x01, 0x07); /* AF clear, AIE off, CLKOUT off. */
	if (!err) { err = i2c_reg_write_byte_dt(&rtc, 0x00, 0); }
	if (!err) { err = registers(0x04, raw, sizeof(raw)); }
	if (err) { return err; }

	struct calendar now;
	bool lost_time = !calendar_decode(raw, &now);
	/* Preserve a cleared AF or a recovered clock across an I2C re-arm retry. */
	reading->reset |= lost_time;
	if (lost_time) {
		err = start_relative_clock();
		if (err) { return err; }
	}

	if (astra_time_mailbox.cookie == 0x41535455u) {
		struct calendar requested = astra_time_mailbox.value;
		astra_time_mailbox.cookie = 0;
		err = set_time(&requested, true);
		reading->reset = true;
		if (err) { return err; }
	}

	err = registers(0x04, raw, sizeof(raw));
	if (!err) { err = i2c_reg_read_byte_dt(&rtc, 0x03, &ram); }
	if (err) { return err; }
	if (!calendar_decode(raw, &now) || !calendar_seconds(&now, &reading->seconds)) {
		return -ENODATA;
	}
	reading->utc = ram == 0xe7;
	uint8_t burst[6] = {0x0b};
	uint8_t check[5];
	next_alarm(&now, &burst[1]);
	err = i2c_write_dt(&rtc, burst, sizeof(burst));
	if (!err) { err = registers(0x0b, check, sizeof(check)); }
	if (!err && memcmp(check, &burst[1], sizeof(check))) { err = -EIO; }
	if (!err) { err = i2c_reg_write_byte_dt(&rtc, 0x01, 0x87); }
	if (!err) { err = i2c_reg_read_byte_dt(&rtc, 0x01, &ctrl2); }
	if (!err && (ctrl2 & 0xc7) != 0x87) { err = -EIO; }
	return err;
}
