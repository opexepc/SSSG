// generated with SSSG 0.0.1
#ifndef SSS_data
#define SSS_data

#include "data.h"
#include "../include/sss.h"

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

	size_t __size = 0;
	memset(s, 0, sizeof(data_t));

	if(SSS_read_i32(f, &s->count)) goto fail;
	if(SSS_read_i32(f, &s->max)) goto fail;
	if(SSS_read_i8(f, (int8_t*)&s->key)) goto fail;
	if(SSS_read_f32(f, &s->triangle.x)) goto fail;
	if(SSS_read_f32(f, &s->triangle.y)) goto fail;
	if(SSS_read_f32(f, &s->triangle.z)) goto fail;

	for(int i = 0; i < 10; ++i)
	{
		if(SSS_read_f32(f, &s->triangles[i].x)) goto fail;
		if(SSS_read_f32(f, &s->triangles[i].y)) goto fail;
		if(SSS_read_f32(f, &s->triangles[i].z)) goto fail;
	}

	for(int i = 0; i < 32; ++i)
	{
		if(SSS_read_i32(f, &s->fixed_size_arr[i])) goto fail;
	}
	if(SSS_read_i32(f, &s->size)) goto fail;

	if(s->size < 0) goto fail;
	__size = sizeof(int) * s->size;
	if(__size > 100000000)
		goto fail;
	s->dynamic_size_arr = (int*)malloc(__size);
	if(!s->dynamic_size_arr) goto fail;

	for(int i = 0; i < s->size; ++i)
	{
		if(SSS_read_i32(f, &s->dynamic_size_arr[i])) goto fail;
	}

	if(1 < 0) goto fail;
	__size = sizeof(int) * 1;
	if(__size > 100000000)
		goto fail;
	s->pointer_to_value = (int*)malloc(__size);
	if(!s->pointer_to_value) goto fail;
	if(SSS_read_i32(f, s->pointer_to_value)) goto fail;

	goto success;

fail:
	if(s->dynamic_size_arr)
	{
		free(s->dynamic_size_arr);
		s->dynamic_size_arr = NULL;
	}
	if(s->pointer_to_value)
	{
		free(s->pointer_to_value);
		s->pointer_to_value = NULL;
	}
	return 1;

success:
	return 0;
}

static int SSS_write_data_t(FILE *f, data_t *s)
{
	const int __version = 1;
	if(SSS_write_i32(f, &__version)) return 1;

	if(SSS_write_i32(f, &s->count)) goto fail;
	if(SSS_write_i32(f, &s->max)) goto fail;
	if(SSS_write_i8(f, (int8_t*)&s->key)) goto fail;
	if(SSS_write_f32(f, &s->triangle.x)) goto fail;
	if(SSS_write_f32(f, &s->triangle.y)) goto fail;
	if(SSS_write_f32(f, &s->triangle.z)) goto fail;

	for(int i = 0; i < 10; ++i)
	{
		if(SSS_write_f32(f, &s->triangles[i].x)) goto fail;
		if(SSS_write_f32(f, &s->triangles[i].y)) goto fail;
		if(SSS_write_f32(f, &s->triangles[i].z)) goto fail;
	}

	for(int i = 0; i < 32; ++i)
	{
		if(SSS_write_i32(f, &s->fixed_size_arr[i])) goto fail;
	}
	if(SSS_write_i32(f, &s->size)) goto fail;

	for(int i = 0; i < s->size; ++i)
	{
		if(SSS_write_i32(f, &s->dynamic_size_arr[i])) goto fail;
	}
	if(SSS_write_i32(f, s->pointer_to_value)) goto fail;

	goto success;

fail:
	return 1;

success:
	return 0;
}

#endif // SSS_data