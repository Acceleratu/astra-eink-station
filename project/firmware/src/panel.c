#include "panel.h"
#include <errno.h>

static int command(const struct panel_io *io, uint8_t opcode, const uint8_t *data, size_t length)
{
	int err = io->send(io->context, false, &opcode, 1);
	if (!err && length) {
		err = io->send(io->context, true, data, length);
	}
	return err;
}

static int byte_command(const struct panel_io *io, uint8_t opcode, uint8_t value)
{
	return command(io, opcode, &value, 1);
}

static int wait_level(const struct panel_io *io, int expected, unsigned timeout, unsigned poll)
{
	uint32_t start = io->time_ms(io->context);
	do {
		int level = io->busy(io->context);
		if (level < 0) {
			return level;
		}
		if (level == expected) {
			return 0;
		}
		io->delay_ms(io->context, poll);
	} while ((uint32_t)(io->time_ms(io->context) - start) < timeout);
	return -ETIMEDOUT;
}

static int origin(const struct panel_io *io)
{
	uint8_t y[] = {0, 0};
	int err = byte_command(io, 0x4e, 0);
	return err ? err : command(io, 0x4f, y, sizeof(y));
}

static int initialize(const struct panel_io *io, enum refresh mode)
{
	/* Recreate registers after VMAIN loss. Power-up, HW reset, SW reset. */
	io->delay_ms(io->context, 100);
	int err = io->reset(io->context, true);
	if (!err) {
		io->delay_ms(io->context, 2);
		err = io->reset(io->context, false);
	}
	if (!err) {
		io->delay_ms(io->context, 100);
		err = wait_level(io, 0, 2000, 2);
	}
	if (!err) {
		err = command(io, 0x12, NULL, 0);
	}
	if (!err) {
		io->delay_ms(io->context, 10);
		err = wait_level(io, 0, 2000, 2);
	}
	uint8_t gate[] = {0x2b, 0x01, 0x00};
	uint8_t wave[] = {mode == REFRESH_PARTIAL ? 0x00 : 0x40, 0x00};
	uint8_t x_range[] = {0x00, 0x31};
	uint8_t y_range[] = {0x00, 0x00, 0x2b, 0x01};
	if (!err) { err = command(io, 0x01, gate, sizeof(gate)); }
	if (!err) { err = byte_command(io, 0x18, 0x80); }  /* Internal temperature sensor. */
	if (!err) { err = command(io, 0x21, wave, sizeof(wave)); }
	if (!err) { err = byte_command(io, 0x3c, mode == REFRESH_PARTIAL ? 0x80 : 0x05); }
	if (!err) { err = byte_command(io, 0x11, 0x03); }
	if (!err) { err = command(io, 0x44, x_range, sizeof(x_range)); }
	if (!err) { err = command(io, 0x45, y_range, sizeof(y_range)); }
	return err;
}

int panel_refresh(const struct panel_io *io, enum refresh mode, const struct scene *old,
		  const struct scene *next, uint8_t scratch[ASTRA_FRAME_BYTES])
{
	if ((mode != REFRESH_FULL && mode != REFRESH_PARTIAL) || (mode == REFRESH_PARTIAL && !old)) {
		return -EINVAL;
	}
	int err = initialize(io, mode);
	if (!err) {
		err = origin(io);
	}
	if (!err) {
		render_frame(mode == REFRESH_PARTIAL ? old : next, scratch);
		err = command(io, 0x26, scratch, ASTRA_FRAME_BYTES);
	}
	if (!err) {
		err = origin(io);
	}
	if (!err) {
		if (mode == REFRESH_PARTIAL) {
			render_frame(next, scratch);
		}
		err = command(io, 0x24, scratch, ASTRA_FRAME_BYTES);
	}
	if (!err) {
		err = byte_command(io, 0x22, mode == REFRESH_PARTIAL ? 0xff : 0xf7);
	}
	if (!err) {
		err = command(io, 0x20, NULL, 0);
	}
	if (!err) {
		/* A disconnected BUSY pulled low must never authorize journal commit. */
		err = wait_level(io, 1, 250, 1);
	}
	if (!err) {
		err = wait_level(io, 0, 25000, 5);
	}
	return err;
}

int panel_sleep(const struct panel_io *io)
{
	int err = byte_command(io, 0x10, 0x01);
	if (!err) {
		io->delay_ms(io->context, 100);
	}
	return err;
}
