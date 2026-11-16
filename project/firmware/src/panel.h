#ifndef ASTRA_PANEL_H
#define ASTRA_PANEL_H
#include "state.h"

struct panel_io {
	void *context;
	int (*send)(void *ctx, bool data, const uint8_t *buf, size_t len);
	int (*reset)(void *ctx, bool asserted);
	int (*busy)(void *ctx);
	void (*delay_ms)(void *ctx, unsigned ms);
	uint32_t (*time_ms)(void *ctx);
};

int panel_refresh(const struct panel_io *io, enum refresh mode, const struct scene *old,
		  const struct scene *next, uint8_t scratch[ASTRA_FRAME_BYTES]);
int panel_sleep(const struct panel_io *io);
#endif
