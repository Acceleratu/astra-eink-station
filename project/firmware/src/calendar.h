#ifndef ASTRA_CALENDAR_H
#define ASTRA_CALENDAR_H
#include <stdbool.h>
#include <stdint.h>

struct calendar {
	uint16_t year;
	uint8_t month, day, hour, minute, second;
};
bool calendar_seconds(const struct calendar *t, uint32_t *seconds);
bool calendar_decode(const uint8_t regs[7], struct calendar *out);
void calendar_encode(const struct calendar *t, uint8_t regs[7]);
void next_alarm(const struct calendar *now, uint8_t regs[5]);
#endif
