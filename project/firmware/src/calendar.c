#include "calendar.h"

static unsigned days_in_month(unsigned y, unsigned m)
{
	const uint8_t days[] = {31,28,31,30,31,30,31,31,30,31,30,31};
	return days[m - 1] + (m == 2 && y % 4 == 0);
}

bool calendar_seconds(const struct calendar *t, uint32_t *seconds)
{
	if (t->year < 2000 || t->year > 2099 || t->month == 0 || t->month > 12 || t->day == 0 ||
	    t->day > days_in_month(t->year, t->month) || t->hour > 23 || t->minute > 59 ||
	    t->second > 59) {
		return false;
	}
	uint32_t years = t->year - 2000;
	uint32_t days = 365 * years + (years + 3) / 4;
	for (unsigned m = 1; m < t->month; ++m) {
		days += days_in_month(t->year, m);
	}
	days += t->day - 1;
	*seconds = ((days * 24 + t->hour) * 60 + t->minute) * 60 + t->second;
	return true;
}

static uint8_t bcd(unsigned value) { return (uint8_t)((value / 10u) * 16u + value % 10u); }

static uint8_t from_bcd(uint8_t value)
{
	return (value & 15) > 9 || (value >> 4) > 9 ? 255 : (uint8_t)((value >> 4) * 10 + (value & 15));
}

bool calendar_decode(const uint8_t r[7], struct calendar *out)
{
	*out = (struct calendar){ .year = 2000 + from_bcd(r[6]), .month = from_bcd(r[5] & 31),
		.day = from_bcd(r[3] & 63), .hour = from_bcd(r[2] & 63),
		.minute = from_bcd(r[1] & 127), .second = from_bcd(r[0] & 127) };
	uint32_t seconds;
	return !(r[0] & 0x80) && calendar_seconds(out, &seconds);
}

void calendar_encode(const struct calendar *t, uint8_t out[7])
{
	uint32_t seconds = 0;
	(void)calendar_seconds(t, &seconds);
	out[0] = bcd(t->second);
	out[1] = bcd(t->minute);
	out[2] = bcd(t->hour);
	out[3] = bcd(t->day);
	out[4] = (uint8_t)((6 + seconds / 86400) % 7); /* 2000-01-01 was Saturday. */
	out[5] = bcd(t->month);
	out[6] = bcd(t->year % 100);
}

void next_alarm(const struct calendar *now, uint8_t regs[5])
{
	unsigned seconds = (unsigned)now->hour * 3600 + (unsigned)now->minute * 60 + now->second;
	unsigned wait = 900u - seconds % 900u;
	/* Coalesce a manual/fixture wake within two seconds of the queued boundary.
	 * Re-arming after display work stays on the same grid, without cumulative drift. */
	if (wait <= 2) { wait += 900; }
	unsigned at = ((seconds + wait) % 86400u) / 60u;
	regs[0] = 0;
	regs[1] = bcd(at % 60);
	regs[2] = bcd(at / 60);
	regs[3] = regs[4] = 0x80; /* Compare h:m:s daily, re-arm every wake. */
}
