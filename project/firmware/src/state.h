#ifndef ASTRA_STATE_H
#define ASTRA_STATE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define ASTRA_WIDTH 400
#define ASTRA_HEIGHT 300
#define ASTRA_FRAME_BYTES (ASTRA_WIDTH / 8 * ASTRA_HEIGHT)
#define ASTRA_RENDERER 0x41530102u
#define ASTRA_UTC 1u
#define ASTRA_CLOCK_RESET 2u

struct scene {
	uint32_t seconds;       /* Seconds since 2000-01-01, UTC or relative until provisioned. */
	uint32_t pressure_pa;
	int16_t temp_centi_c;
	uint16_t humidity_centi_pct;
	uint16_t battery_mv;
	uint8_t flags;
	uint8_t buttons;
};

struct intent {
	uint32_t magic;
	uint32_t generation;
	uint32_t renderer;
	uint32_t last_full;
	struct scene scene;
	uint8_t partials;
	uint8_t reserved[11];
	uint32_t crc;
};

struct seal {
	uint32_t magic;
	uint32_t generation;
	uint32_t crc;
	uint32_t inverse_crc;
};

struct slot {
	struct intent intent;
	struct seal seal;
};

struct journal {
	size_t slots;
	void *context;
	int (*read)(void *context, size_t address, void *data, size_t length);
	int (*write)(void *context, size_t address, const void *data, size_t length);
};

struct history {
	struct intent intent;
	size_t index;
	bool found;
	bool committed;
	bool damaged;
};

enum refresh { REFRESH_SKIP, REFRESH_FULL, REFRESH_PARTIAL, REFRESH_DEFER };

int journal_find(const struct journal *journal, struct history *out);
int journal_prepare(const struct journal *journal, const struct history *prior,
		    const struct scene *next, enum refresh mode, struct history *pending);
int journal_commit(const struct journal *journal, const struct history *pending);
int journal_clean_damaged(const struct journal *journal);
enum refresh choose_refresh(const struct scene *now, const struct history *prior);
void render_frame(const struct scene *scene, uint8_t frame[ASTRA_FRAME_BYTES]);

#endif
