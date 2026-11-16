#include "state.h"

#include <errno.h>
#include <stdio.h>
#include <string.h>

_Static_assert(sizeof(struct scene) == 16, "persistent scene changed");
_Static_assert(sizeof(struct intent) == 48 && offsetof(struct intent, crc) == 44,
	       "intent must fit three RRAM lines");
_Static_assert(sizeof(struct slot) == 64, "each record occupies four 16-byte RRAM lines");

#define INTENT_MAGIC 0x41535449u
#define SEAL_MAGIC 0x41535443u

static uint32_t crc32(const void *data, size_t len)
{
	const uint8_t *bytes = data;
	uint32_t crc = UINT32_MAX;
	for (size_t i = 0; i < len; ++i) {
		crc ^= bytes[i];
		for (int bit = 0; bit < 8; ++bit) {
			crc = (crc >> 1) ^ ((0u - (crc & 1u)) & 0xedb88320u);
		}
	}
	return ~crc;
}

static bool valid_intent(const struct intent *i)
{
	return i->magic == INTENT_MAGIC && crc32(i, offsetof(struct intent, crc)) == i->crc;
}

static bool erased(const struct slot *slot)
{
	const uint8_t *p = (const uint8_t *)slot;
	for (size_t i = 0; i < sizeof(*slot); ++i) {
		if (p[i] != UINT8_MAX) {
			return false;
		}
	}
	return true;
}

static struct seal make_seal(const struct intent *i)
{
	return (struct seal){ SEAL_MAGIC, i->generation, i->crc, ~i->crc };
}

int journal_find(const struct journal *j, struct history *out)
{
	if (!j || !out || j->slots < 2) {
		return -EINVAL;
	}
	*out = (struct history){0};
	for (size_t n = 0; n < j->slots; ++n) {
		struct slot s;
		int err = j->read(j->context, n * sizeof(s), &s, sizeof(s));
		if (err) {
			return err;
		}
		if (!valid_intent(&s.intent)) {
			out->damaged |= !erased(&s);
			continue;
		}
		/* Live records span fewer than 2^31 consecutive sequence numbers. */
		if (!out->found || (int32_t)(s.intent.generation - out->intent.generation) > 0) {
			struct seal expected = make_seal(&s.intent);
			out->found = true;
			out->index = n;
			out->intent = s.intent;
			out->committed = memcmp(&s.seal, &expected, sizeof(expected)) == 0;
		}
	}
	return 0;
}

static int write_verified(const struct journal *j, size_t address, const void *data, size_t len)
{
	uint8_t buffer[sizeof(struct slot)];
	int err = j->write(j->context, address, data, len);
	if (!err) {
		err = j->read(j->context, address, buffer, len);
	}
	if (err) {
		return err;
	}
	return memcmp(buffer, data, len) ? -EIO : 0;
}

int journal_prepare(const struct journal *j, const struct history *prior,
		    const struct scene *next, enum refresh mode, struct history *pending)
{
	if (mode == REFRESH_SKIP || (mode == REFRESH_PARTIAL && !prior->committed)) {
		return -EINVAL;
	}
	struct intent i = {
		.magic = INTENT_MAGIC, .generation = prior->found ? prior->intent.generation + 1 : 0,
		.renderer = ASTRA_RENDERER,
		.last_full = mode == REFRESH_PARTIAL ? prior->intent.last_full : next->seconds,
		.scene = *next, .partials = mode == REFRESH_PARTIAL ? prior->intent.partials + 1 : 0
	};
	i.crc = crc32(&i, offsetof(struct intent, crc));
	size_t n = prior->found ? (prior->index + 1) % j->slots : 0;
	size_t address = n * sizeof(struct slot);
	struct seal clear;
	memset(&clear, 0xff, sizeof(clear));
	int err = write_verified(j, address + offsetof(struct slot, seal), &clear, sizeof(clear));
	if (!err) {
		err = write_verified(j, address, &i, sizeof(i));
	}
	if (!err) {
		*pending = (struct history){ .found = true, .index = n, .intent = i };
	}
	return err;
}

int journal_commit(const struct journal *j, const struct history *pending)
{
	struct seal s = make_seal(&pending->intent);
	return write_verified(j, pending->index * sizeof(struct slot) + offsetof(struct slot, seal),
			      &s, sizeof(s));
}

int journal_clean_damaged(const struct journal *j)
{
	/* Call only after a fresh full waveform and its new verified commit. */
	struct slot clear;
	memset(&clear, 0xff, sizeof(clear));
	for (size_t n = 0; n < j->slots; ++n) {
		struct slot s;
		size_t addr = n * sizeof(s);
		int err = j->read(j->context, addr, &s, sizeof(s));
		if (!err && !valid_intent(&s.intent) && !erased(&s)) {
			err = write_verified(j, addr, &clear, sizeof(clear));
		}
		if (err) {
			return err;
		}
	}
	return 0;
}

enum refresh choose_refresh(const struct scene *now, const struct history *prior)
{
	if (now->temp_centi_c < 0 || now->temp_centi_c > 5000 ||
	    now->battery_mv < 3300 || now->battery_mv > 4350) {
		return REFRESH_SKIP;
	}
	if (!prior->found) {
		return prior->damaged ? REFRESH_DEFER : REFRESH_FULL;
	}
	const struct intent *p = &prior->intent;
	bool same_timebase = ((p->scene.flags ^ now->flags) & ASTRA_UTC) == 0 &&
			     !(now->flags & ASTRA_CLOCK_RESET) && now->seconds >= p->scene.seconds;
	if (!same_timebase) {
		/* Record a new time anchor without applying any waveform. Rapid key wakes
		 * then see that anchor and cannot bypass the minimum interval. */
		return REFRESH_DEFER;
	}
	if (now->seconds - p->scene.seconds < 180) {
		return REFRESH_SKIP;
	}
	if (prior->damaged || !prior->committed || p->renderer != ASTRA_RENDERER ||
	    p->partials >= 5 || now->seconds < p->last_full ||
	    now->seconds - p->last_full >= 86400 || (now->buttons & 1) ||
	    now->temp_centi_c < 1500 || now->temp_centi_c > 3500) {
		return REFRESH_FULL;
	}
	return REFRESH_PARTIAL;
}

/* Five-bit rows. Only glyphs used by the fixed bring-up layout are defined. */
struct glyph { char c; uint8_t row[7]; };
static const struct glyph glyphs[] = {
	{'0',{14,17,19,21,25,17,14}}, {'1',{4,12,4,4,4,4,14}},
	{'2',{14,17,1,2,4,8,31}}, {'3',{30,1,1,14,1,1,30}},
	{'4',{2,6,10,18,31,2,2}}, {'5',{31,16,16,30,1,1,30}},
	{'6',{6,8,16,30,17,17,14}}, {'7',{31,1,2,4,8,8,8}},
	{'8',{14,17,17,14,17,17,14}}, {'9',{14,17,17,15,1,2,12}},
	{'A',{14,17,17,31,17,17,17}}, {'B',{30,17,17,30,17,17,30}},
	{'C',{14,17,16,16,16,17,14}}, {'D',{28,18,17,17,17,18,28}},
	{'E',{31,16,16,30,16,16,31}}, {'H',{17,17,17,31,17,17,17}},
	{'I',{14,4,4,4,4,4,14}}, {'K',{17,18,20,24,20,18,17}},
	{'L',{16,16,16,16,16,16,31}}, {'M',{17,27,21,21,17,17,17}},
	{'N',{17,25,25,21,19,19,17}}, {'O',{14,17,17,17,17,17,14}},
	{'P',{30,17,17,30,16,16,16}}, {'R',{30,17,17,30,20,18,17}},
	{'S',{15,16,16,14,1,1,30}}, {'T',{31,4,4,4,4,4,4}},
	{'U',{17,17,17,17,17,17,14}}, {'V',{17,17,17,17,17,10,4}},
	{'Y',{17,17,10,4,4,4,4}},     {'-',{0,0,0,31,0,0,0}},
	{'.',{0,0,0,0,0,12,12}},      {':',{0,12,12,0,12,12,0}},
	{'%',{17,2,4,8,16,17,0}},      {'m',{0,0,26,21,21,17,17}},
	{'h',{16,16,22,25,17,17,17}}, {'a',{0,0,14,1,15,17,15}},
	{'\x7f',{6,9,9,6,0,0,0}} /* degree sign in the one-byte bitmap font */
};

static void label(uint8_t *frame, int x, int y, unsigned scale, const char *text)
{
	for (; *text && x + (int)(5 * scale) <= ASTRA_WIDTH; ++text, x += 6 * (int)scale) {
		for (size_t n = 0; n < sizeof(glyphs)/sizeof(glyphs[0]); ++n) {
			if (glyphs[n].c != *text) {
				continue;
			}
			for (unsigned row = 0; row < 7 * scale; ++row) {
				for (unsigned col = 0; col < 5 * scale; ++col) {
					if (glyphs[n].row[row / scale] & (16u >> (col / scale))) {
						unsigned px = (unsigned)x + col;
						size_t a = (y + row) * (ASTRA_WIDTH / 8) + px / 8;
						frame[a] &= (uint8_t)~(0x80u >> (px & 7));
					}
				}
			}
			break;
		}
	}
}

void render_frame(const struct scene *s, uint8_t frame[ASTRA_FRAME_BYTES])
{
	char buf[40];
	memset(frame, 0xff, ASTRA_FRAME_BYTES);
	label(frame, 14, 12, 3, "ASTRA METEO");
	int t = s->temp_centi_c;
	int mag = t < 0 ? -t : t;
	snprintf(buf, sizeof(buf), "%s%d.%02d \x7f" "C", t < 0 ? "-" : "", mag/100, mag%100);
	label(frame, 14, 50, 5, buf);
	snprintf(buf, sizeof(buf), "RH %u.%u%%", (unsigned)s->humidity_centi_pct / 100,
		 (unsigned)s->humidity_centi_pct % 100 / 10);
	label(frame, 14, 110, 3, buf);
	snprintf(buf, sizeof(buf), "P %u.%u hPa", (unsigned)s->pressure_pa / 100,
		 (unsigned)s->pressure_pa % 100 / 10);
	label(frame, 14, 145, 3, buf);
	snprintf(buf, sizeof(buf), "BAT %u mV", (unsigned)s->battery_mv);
	label(frame, 14, 180, 3, buf);
	snprintf(buf, sizeof(buf), "%s %02u:%02u", s->flags & ASTRA_UTC ? "UTC" : "REL",
		 (unsigned)(s->seconds / 3600 % 24), (unsigned)(s->seconds / 60 % 60));
	label(frame, 14, 230, 2, buf);
	snprintf(buf, sizeof(buf), "KEYS %u%u%u", !!(s->buttons & 1u), !!(s->buttons & 2u),
		 !!(s->buttons & 4u));
	label(frame, 14, 262, 2, buf);
}
