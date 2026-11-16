#ifndef ASTRA_CLOCK_H
#define ASTRA_CLOCK_H
#include "calendar.h"
#include <stdint.h>

struct clock_reading {
	uint32_t seconds;
	bool utc;
	bool reset;
	bool was_alarm;
};

/* Factory debugger sets time fields then cookie at astra_fixture_hook. */
struct time_mailbox {
	uint32_t cookie;
	struct calendar value;
};
extern volatile struct time_mailbox astra_time_mailbox;
void astra_fixture_hook(void);
int clock_read_arm(struct clock_reading *reading);
#endif
