#include "calendar.h"
#include "panel.h"
#include "state.h"

#include <assert.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOT_COUNT 4
struct memory {
	uint8_t bytes[SLOT_COUNT * sizeof(struct slot)];
	int remaining;
};

static int mem_read(void *ctx, size_t at, void *out, size_t len)
{
	struct memory *m = ctx;
	assert(at + len <= sizeof(m->bytes));
	memcpy(out, m->bytes + at, len);
	return 0;
}

static int mem_write(void *ctx, size_t at, const void *data, size_t len)
{
	struct memory *m = ctx;
	assert(at % 16 == 0 && len % 16 == 0 && at + len <= sizeof(m->bytes));
	size_t wrote = (size_t)m->remaining < len ? (size_t)m->remaining : len;
	memcpy(m->bytes + at, data, wrote);
	m->remaining -= (int)wrote;
	return wrote == len ? 0 : -EIO;
}

static struct scene make_scene(unsigned n)
{
	return (struct scene){ .seconds = n * 900, .pressure_pa = 101325 + n,
		.temp_centi_c = 2083 + (int)n * 3, .humidity_centi_pct = 5234,
		.battery_mv = 3980 - n, .flags = ASTRA_UTC, .buttons = (n == 2) ? 2 : 0 };
}

static void journal_tests(void)
{
	struct memory base;
	memset(base.bytes, 0xff, sizeof(base.bytes));
	base.remaining = INT_MAX;
	struct journal j = { .slots = SLOT_COUNT, .context = &base, .read = mem_read, .write = mem_write };
	struct history old, p;
	for (unsigned n = 1; n <= SLOT_COUNT; ++n) {
		struct scene s = make_scene(n);
		assert(journal_find(&j, &old) == 0);
		assert(journal_prepare(&j, &old, &s, n == 1 ? REFRESH_FULL : REFRESH_PARTIAL, &p) == 0);
		assert(journal_commit(&j, &p) == 0);
	}
	assert(journal_find(&j, &old) == 0 && old.committed && !old.damaged);
	struct scene next = make_scene(5), future = make_scene(6);
	assert(choose_refresh(&next, &old) == REFRESH_PARTIAL);
	for (int cut = 0; cut <= 80; ++cut) {
		struct memory mem = base; mem.remaining = cut; j.context = &mem;
		struct history pending, result;
		int prepared = journal_prepare(&j, &old, &next, REFRESH_PARTIAL, &pending);
		if (!prepared) {
			/* Before/during the display waveform: no commit has been written. */
			assert(journal_find(&j, &result) == 0);
			assert(result.found && !result.committed);
			assert(choose_refresh(&future, &result) == REFRESH_FULL);
			/* A seal is written only after verified BUSY high then low. */
			(void)journal_commit(&j, &pending);
		}
		assert(journal_find(&j, &result) == 0);
		if (result.committed && result.intent.generation == old.intent.generation) {
			assert(prepared != 0); /* Old optical state is still safe. */
		} else if (result.committed) {
			assert(!prepared && !memcmp(&result.intent.scene, &next, sizeof(next)));
		} else {
			assert(choose_refresh(&future, &result) == REFRESH_FULL);
		}
	}
	printf("PASS journal: all 81 byte-cut positions in clear, intent and seal on a reused slot\n");

	j.context = &base;
	for (size_t bit = 0; bit < sizeof(struct slot) * 8; ++bit) {
		struct memory mem = base;
		mem.bytes[old.index*sizeof(struct slot) + bit/8] ^= (uint8_t)(1u << (bit % 8));
		j.context = &mem;
		struct history read;
		assert(journal_find(&j, &read) == 0);
		assert(choose_refresh(&future, &read) == REFRESH_FULL);
		assert(journal_prepare(&j, &read, &future, REFRESH_FULL, &p) == 0);
		assert(journal_commit(&j, &p) == 0);
		assert(journal_clean_damaged(&j) == 0);
		assert(journal_find(&j, &read) == 0 && read.committed && !read.damaged);
	}
	printf("PASS journal: all 512 single-bit flips in latest intent/seal require full, then recover\n");

	struct memory wrap;
	memset(wrap.bytes, 0xff, sizeof(wrap.bytes)); wrap.remaining = INT_MAX;
	j.context = &wrap;
	old = (struct history){ .found = true, .index = 0, .intent.generation = UINT32_MAX-2 };
	for (unsigned n = 1; n <= 4; ++n) {
		struct scene s = make_scene(n);
		assert(journal_prepare(&j, &old, &s, REFRESH_FULL, &p) == 0);
		assert(journal_commit(&j, &p) == 0 && journal_find(&j, &old) == 0);
		assert(old.intent.generation == UINT32_MAX-2+n && old.committed);
	}
	printf("PASS journal: newest sequence selected across 32-bit wrap\n");

	struct scene n = make_scene(10);
	old = (struct history){ .found = true, .committed = true, .intent = {
		.renderer = ASTRA_RENDERER, .last_full = n.seconds-900, .scene = make_scene(9) } };
	assert(choose_refresh(&n,&old)==REFRESH_PARTIAL);
	old.intent.partials=5; assert(choose_refresh(&n,&old)==REFRESH_FULL);
	old.intent.partials=0; n.seconds=old.intent.scene.seconds+179;
	assert(choose_refresh(&n,&old)==REFRESH_SKIP);
	n.seconds++; assert(choose_refresh(&n,&old)==REFRESH_PARTIAL);
	n.temp_centi_c=1499; assert(choose_refresh(&n,&old)==REFRESH_FULL);
	n.temp_centi_c=-1; assert(choose_refresh(&n,&old)==REFRESH_SKIP);
	n.temp_centi_c=3501; assert(choose_refresh(&n,&old)==REFRESH_FULL);
	n.temp_centi_c=5001; assert(choose_refresh(&n,&old)==REFRESH_SKIP);
	n.temp_centi_c=2500; n.battery_mv=3299; assert(choose_refresh(&n,&old)==REFRESH_SKIP);
	n.battery_mv=4351; assert(choose_refresh(&n,&old)==REFRESH_SKIP);
	n.battery_mv=4000; n.buttons=1; assert(choose_refresh(&n,&old)==REFRESH_FULL);
	n.buttons=0; old.intent.renderer^=1; assert(choose_refresh(&n,&old)==REFRESH_FULL);
	old.intent.renderer=ASTRA_RENDERER; n.seconds=old.intent.last_full+86400;
	assert(choose_refresh(&n,&old)==REFRESH_FULL);
	n.seconds=100; n.flags|=ASTRA_CLOCK_RESET; assert(choose_refresh(&n,&old)==REFRESH_DEFER);
	assert(journal_prepare(&j,&old,&n,REFRESH_DEFER,&p)==0);
	n.flags &= (uint8_t)~ASTRA_CLOCK_RESET;
	n.seconds += 179; assert(choose_refresh(&n,&p)==REFRESH_SKIP);
	++n.seconds; assert(choose_refresh(&n,&p)==REFRESH_FULL);
	printf("PASS policy: cadence, forced full, time, thermal, low/high battery, renderer guards\n");
}

struct panel_mock {
	uint32_t ms, started;
	uint8_t op, waveform, red[ASTRA_FRAME_BYTES], black[ASTRA_FRAME_BYTES];
	unsigned activate, resets, origins_x, origins_y, data26, data24, calls;
	int fault_at, stuck;
	bool level;
};

static int mock_send(void *ctx, bool data, const uint8_t *buf, size_t len)
{
	struct panel_mock *m=ctx;
	if ((int)m->calls++ == m->fault_at) { return -EIO; }
	if (!data) {
		assert(len == 1); m->op=buf[0];
		if (m->op==0x20) { ++m->activate; m->started=m->ms; }
		return 0;
	}
	switch (m->op) {
	case 0x4e: assert(len==1 && buf[0]==0); ++m->origins_x; break;
	case 0x4f: assert(len==2 && buf[0]==0 && buf[1]==0); ++m->origins_y; break;
	case 0x44: assert(len==2 && buf[0]==0 && buf[1]==49); break;
	case 0x45: assert(len==4 && !memcmp(buf,(uint8_t[]){0,0,0x2b,1},4)); break;
	case 0x26: assert(len==ASTRA_FRAME_BYTES && m->origins_x==1 && m->origins_y==1);
		memcpy(m->red,buf,len); ++m->data26; break;
	case 0x24: assert(len==ASTRA_FRAME_BYTES && m->origins_x==2 && m->origins_y==2);
		memcpy(m->black,buf,len); ++m->data24; break;
	case 0x22: assert(len==1); m->waveform=buf[0]; break;
	default: break;
	}
	return 0;
}
static int mock_reset(void *ctx, bool asserted)
{
	struct panel_mock *m=ctx;
	m->level=asserted;
	if (asserted) { ++m->resets; memset(m->red,0xcc,sizeof(m->red)); memset(m->black,0x55,sizeof(m->black)); }
	return 0;
}
static int mock_busy(void *ctx)
{
	struct panel_mock *m=ctx;
	if (!m->activate) { return m->stuck==3; }
	if (m->stuck==1) { return 0; }
	if (m->stuck==2) { return 1; }
	uint32_t since=m->ms-m->started;
	return since >= 3 && since < 120;
}
static void mock_delay(void *ctx, unsigned n) { ((struct panel_mock *)ctx)->ms+=n; }
static uint32_t mock_ms(void *ctx) { return ((struct panel_mock *)ctx)->ms; }

static void display_tests(const char *preview)
{
	static struct panel_mock m;
	static uint8_t buf[ASTRA_FRAME_BYTES], old_image[ASTRA_FRAME_BYTES], new_image[ASTRA_FRAME_BYTES];
	struct scene old=make_scene(1), next=make_scene(2);
	render_frame(&old,old_image); render_frame(&next,new_image);
	assert(memcmp(old_image,new_image,sizeof(old_image))!=0);
	struct panel_io io={&m,mock_send,mock_reset,mock_busy,mock_delay,mock_ms};
	for (int mode=REFRESH_FULL; mode<=REFRESH_PARTIAL; ++mode) {
		m=(struct panel_mock){.fault_at=-1, .ms=UINT32_MAX-201};
		assert(panel_refresh(&io,(enum refresh)mode,&old,&next,buf)==0);
		assert(m.activate==1 && m.resets==1 && m.data24==1 && m.data26==1);
		assert(!memcmp(m.black,new_image,sizeof(new_image)));
		assert(!memcmp(m.red,mode==REFRESH_FULL?new_image:old_image,sizeof(old_image)));
		assert(m.waveform==(mode==REFRESH_FULL?0xf7:0xff));
		unsigned calls=m.calls;
		for (unsigned fault=0; fault<calls; ++fault) {
			m=(struct panel_mock){.fault_at=(int)fault};
			assert(panel_refresh(&io,(enum refresh)mode,&old,&next,buf)==-EIO);
		}
		printf("PASS SSD1683 command sink: %s, both 15000-byte planes match, origins reset, %u SPI fault sites\n",
		       mode==REFRESH_FULL?"full":"cold differential",calls);
	}
	for (int stuck=1; stuck<=3; ++stuck) {
		m=(struct panel_mock){.fault_at=-1,.stuck=stuck};
		assert(panel_refresh(&io,REFRESH_PARTIAL,&old,&next,buf)==-ETIMEDOUT);
		assert(m.ms <= 26000);
	}
	printf("PASS BUSY: disconnected low, stuck during waveform, stuck before reset; bounded timeout\n");
	if (preview) {
		FILE *fp=fopen(preview,"wb"); assert(fp);
		assert(fprintf(fp,"P4\n400 300\n")>0);
		for(size_t i=0;i<sizeof(new_image);++i) { assert(fputc((~new_image[i])&255,fp)!=EOF); }
		assert(fclose(fp)==0);
	}
}

static void calendar_tests(void)
{
	uint32_t count=0, last=0;
	for (unsigned year=2000;year<=2099;++year)
		for (unsigned m=1;m<=12;++m)
			for (unsigned d=1;d<=31;++d) {
				struct calendar c={(uint16_t)year,(uint8_t)m,(uint8_t)d,23,55,58},decoded;
				uint32_t s,s2;
				if (!calendar_seconds(&c,&s)) { continue; }
				assert(!count || s-last==86400); ++count; last=s;
				uint8_t r[7],alarm[5];
				calendar_encode(&c,r);
				assert(calendar_decode(r,&decoded) && calendar_seconds(&decoded,&s2) && s2==s);
				next_alarm(&c,alarm);
				assert(!memcmp(alarm,(uint8_t[]){0,0,0,0x80,0x80},5));
			}
	assert(count==36525);
	uint8_t bad[7]={0x80,0,0,1,0,1,0};
	struct calendar c;
	assert(!calendar_decode(bad,&c)); bad[0]=0; bad[1]=0x3f; assert(!calendar_decode(bad,&c));
	printf("PASS PCF85063A calendar: all 36525 dates 2000..2099, midnight alarm, OS and malformed BCD\n");
	for (unsigned now=0; now<86400; ++now) {
		c=(struct calendar){.year=2026,.month=1,.day=1,.hour=now/3600,
			.minute=now/60%60,.second=now%60};
		uint8_t a[5]; next_alarm(&c,a);
		unsigned h=(a[2]>>4)*10+(a[2]&15), m=(a[1]>>4)*10+(a[1]&15);
		unsigned target=(h*3600+m*60)%86400;
		unsigned first_after_guard=(((now+2)/900+1)*900)%86400;
		assert(!a[0] && target==first_after_guard && a[3]==0x80 && a[4]==0x80);
	}
	for (unsigned wake=0; wake<86400; wake+=900) {
		uint8_t early[5],late[5];
		c=(struct calendar){.year=2026,.month=11,.day=15,.hour=wake/3600,.minute=wake/60%60};
		next_alarm(&c,early);
		c.second=(uint8_t)(1+(wake/900*13)%25);
		next_alarm(&c,late);
		assert(!memcmp(early,late,sizeof(early)));
	}
	printf("PASS RTC cadence: all 86400 input seconds, midnight and 2 s boundary guard; 96 varying active runtimes add zero accumulated software drift\n");
}

int main(int argc,char **argv)
{
	journal_tests(); display_tests(argc>1?argv[1]:NULL); calendar_tests();
	return 0;
}
