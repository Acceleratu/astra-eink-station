#include "clock.h"
#include <zephyr/drivers/i2c.h>
#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>

static uint8_t regs[0x12];
static int ms, recoveries, resets;
static bool fail_first_read, fail_alarm_write, corrupt_alarm_readback, oscillator_permanently_stopped;

bool i2c_is_ready_dt(const struct i2c_dt_spec *spec) { (void)spec; return true; }
int i2c_recover_bus(void *bus) { (void)bus; ++recoveries; return 0; }
void k_msleep(int delay) { ms+=delay; }
int i2c_reg_write_byte_dt(const struct i2c_dt_spec *spec,uint8_t addr,uint8_t value)
{
	(void)spec; assert(addr<sizeof(regs));
	if (addr==0 && value==0x58) {
		memset(regs,0,sizeof(regs)); regs[4]=0x80; ++resets;
	} else {
		regs[addr]=value;
	}
	return 0;
}
int i2c_reg_read_byte_dt(const struct i2c_dt_spec *spec,uint8_t addr,uint8_t *out)
{
	(void)spec; assert(addr<sizeof(regs));
	if (fail_first_read) { fail_first_read=false; return -EIO; }
	*out=regs[addr];
	if (addr==4 && oscillator_permanently_stopped) { *out|=0x80; }
	return 0;
}
int i2c_write_read_dt(const struct i2c_dt_spec *spec,const void *tx,size_t nt,void *rx,size_t nr)
{
	(void)spec; assert(nt==1);
	uint8_t addr=*(const uint8_t*)tx; assert(addr+nr<=sizeof(regs)); memcpy(rx,regs+addr,nr);
	if (addr==0x0b && corrupt_alarm_readback) { ((uint8_t*)rx)[1]^=1; }
	return 0;
}
int i2c_write_dt(const struct i2c_dt_spec *spec,const void *tx,size_t len)
{
	(void)spec; const uint8_t *msg=tx; uint8_t addr=msg[0];
	assert(len>=2 && addr+len-1<=sizeof(regs));
	if (addr==0x0b && fail_alarm_write) { fail_alarm_write=false; return -EIO; }
	memcpy(regs+addr,msg+1,len-1); return 0;
}

int main(void)
{
	struct calendar t={2026,11,15,23,59,58};
	struct clock_reading r={0}; calendar_encode(&t,regs+4);
	regs[1]=0xC7; regs[3]=0xe7; fail_first_read=true; fail_alarm_write=true;
	assert(clock_read_arm(&r)==-EIO && r.was_alarm && recoveries==1);
	assert(clock_read_arm(&r)==0 && r.was_alarm && !r.reset && r.utc);
	assert(regs[1]==0x87 && !memcmp(regs+0x0b,(uint8_t[]){0,0x15,0,0x80,0x80},5));
	puts("PASS PCF85063A driver: AF retained across I2C re-arm retry, bus clear, 23:59:58 guard");

	memset(regs,0,sizeof(regs)); regs[4]=0x80; r=(struct clock_reading){0}; fail_alarm_write=true;
	assert(clock_read_arm(&r)==-EIO && r.reset && resets==1);
	assert(clock_read_arm(&r)==0 && r.reset && !r.utc && resets==1 && r.seconds==0);
	assert(!memcmp(regs+0x0b,(uint8_t[]){0,0x15,0,0x80,0x80},5));
	puts("PASS PCF85063A driver: persistent clock-reset provenance after a failed first alarm write");

	astra_time_mailbox.value=t; astra_time_mailbox.cookie=0x41535455u; r=(struct clock_reading){0};
	assert(clock_read_arm(&r)==0 && r.utc && r.reset && !astra_time_mailbox.cookie && regs[3]==0xe7);
	corrupt_alarm_readback=true; r=(struct clock_reading){0};
	assert(clock_read_arm(&r)==-EIO && regs[1]==0x07);
	corrupt_alarm_readback=false;
	regs[4]=0x80; oscillator_permanently_stopped=true; r=(struct clock_reading){0}; ms=0;
	assert(clock_read_arm(&r)==-ETIMEDOUT && ms<=2050);
	puts("PASS PCF85063A driver: UTC provisioning, alarm readback fault and bounded oscillator timeout");
}
