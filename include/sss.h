// The Simple Struct Serializer core
// supported types:
// uint8_t, uint32_t, float
// also support arrays of this types

#ifndef _SSS__
#define _SSS__

#include <stdio.h>
#include <stdint.h>
#include <string.h>

#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
  #define _BIG_ENDIAN 1
#else
  #define _BIG_ENDIAN 0
#endif

static uint32_t SSS_swap_32__(uint32_t x)
{
  return
    (x >> 24) |
    ((x >> 8) & 0x0000FF00) |
    ((x << 8) & 0x00FF0000) |
    (x << 24);
}

static int SSS_read_i8(FILE *f, int8_t *x)
{
  if(fread(x, 1, 1, f) != 1)
    return 1;
  return 0;
}

static int SSS_write_i8(FILE *f, const int8_t *x)
{
  if(fwrite(x, 1, 1, f) != 1)
    return 1;
  return 0;
}

static int SSS_read_i32(FILE *f, int32_t *x)
{
  uint32_t tmp;
  if(fread(&tmp, 4, 1, f) != 1)
    return 1;

#if _BIG_ENDIAN
  tmp = SSS_swap_32__(tmp);
#endif

  *x = (int32_t)tmp;
  return 0;
}

static int SSS_write_i32(FILE *f, const int32_t *x)
{
  uint32_t tmp = (uint32_t)*x;
#if _BIG_ENDIAN
  tmp = swap_32(tmp);
#endif

  if(fwrite(&tmp, 4, 1, f) != 1)
    return 1;
  return 0;
}

static int SSS_read_f32(FILE *f, float *x)
{
  uint32_t tmp;
  if(fread(&tmp, 4, 1, f) != 1)
    return 1;

#if _BIG_ENDIAN
  tmp = SSS_swap_32__(tmp);
#endif

  memcpy(x, &tmp, 4);
  return 0;
}

static int SSS_write_f32(FILE *f, const float *x)
{
  uint32_t tmp;
  memcpy(&tmp, x, 4);
#if _BIG_ENDIAN
  tmp = SSS_swap_32__(tmp);
#endif

  if(fwrite(&tmp, 4, 1, f) != 1)
    return 1;
  return 0;
}

#endif // SSS
