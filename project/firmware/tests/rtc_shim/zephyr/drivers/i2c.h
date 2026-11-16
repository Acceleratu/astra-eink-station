/* Test-only API boundary for the real clock.c. No Nordic or analog timing is emulated. */
#ifndef ASTRA_TEST_I2C_H
#define ASTRA_TEST_I2C_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
struct i2c_dt_spec { void *bus; };
#define I2C_DT_SPEC_GET(node) {0}
bool i2c_is_ready_dt(const struct i2c_dt_spec *);
int i2c_recover_bus(void *);
int i2c_reg_write_byte_dt(const struct i2c_dt_spec *, uint8_t, uint8_t);
int i2c_reg_read_byte_dt(const struct i2c_dt_spec *, uint8_t, uint8_t *);
int i2c_write_read_dt(const struct i2c_dt_spec *, const void *, size_t, void *, size_t);
int i2c_write_dt(const struct i2c_dt_spec *, const void *, size_t);
#endif
