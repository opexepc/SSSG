// generated with SSSG
#ifndef SSS_example_data
#define SSS_example_data

#include "include/sss.h"
#include "example/data.h"

static int SSS_read_data_t(FILE *f, data_t *s, int *version)
{
	const int __version = 1;
	int new_version;

	if(SSS_read_i32(f, &new_version)) return 1;
	if(new_version != __version)
	{
		if(version)
			*version = new_version;
		return SSS_BROKEN_VERSION;
	}

	if(SSS_read_i32(f, &s->count)) return 1;
	if(SSS_read_i32(f, &s->max)) return 1;
	if(SSS_read_i8(f, (int8_t*)&s->key)) return 1;
	if(SSS_read_f32(f, &s->triangle.x)) return 1;
	if(SSS_read_f32(f, &s->triangle.y)) return 1;
	if(SSS_read_f32(f, &s->triangle.z)) return 1;

	return 0;
}

static int SSS_write_data_t(FILE *f, data_t *s, int *version)
{
	const int __version = 1;
	if(SSS_write_i32(f, &__version)) return 1;

	if(SSS_write_i32(f, &s->count)) return 1;
	if(SSS_write_i32(f, &s->max)) return 1;
	if(SSS_write_i8(f, (int8_t*)&s->key)) return 1;
	if(SSS_write_f32(f, &s->triangle.x)) return 1;
	if(SSS_write_f32(f, &s->triangle.y)) return 1;
	if(SSS_write_f32(f, &s->triangle.z)) return 1;

	return 0;
}

#endif // SSS_example_data