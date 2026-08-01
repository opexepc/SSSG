// base container realization
#ifndef ARR
#define ARR

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// @SSSG [0]
typedef struct arr_t
{
  int element_size;
  int count;
  int capacity;

  void *ptr; // @SIZE[s->count | s->element_size]
} arr_t;

static arr_t *arr_make(int element_size, int capacity)
{
  arr_t *arr = (arr_t*)malloc(sizeof(arr_t));
  if(!arr)
    return NULL;

  arr->ptr = malloc(element_size * capacity);
  if(!arr->ptr)
  {
    free(arr);
    return NULL;
  }

  arr->element_size = element_size;
  arr->count = 0;
  arr->capacity = capacity;
  return arr;
}

static int arr_push(arr_t *arr, void *element)
{
  if(arr->count >= arr->capacity)
  {
    int tmp_capacity = arr->capacity * 2;
    if(arr->capacity == 0)
      tmp_capacity = 1;
    
    void *tmp_ptr = realloc(arr->ptr, tmp_capacity * arr->element_size);
    if(!tmp_ptr)
      return 0x01;

    arr->ptr = tmp_ptr;
    arr->capacity = tmp_capacity;
  }

  memcpy
  (
    (char*)arr->ptr + arr->count * arr->element_size,
    element,
    arr->element_size
  );

  arr->count++;
  return 0;
}

static int arr_erase_shift(arr_t *arr, int index)
{
  char *byte_ptr = (char*)arr->ptr;

  if(index < arr->count - 1)
  {
    memmove
    (
      byte_ptr + index * arr->element_size,
      byte_ptr + (index + 1) * arr->element_size,
      (arr->count - index - 1) * arr->element_size
    );
  }
  
  arr->count--;

  if(arr->count == 0)
  {
    free(arr->ptr);
    arr->ptr = NULL;
    arr->capacity = 0;
    return 0;
  }

  if(arr->count < arr->capacity / 2)
  {
    arr->capacity /= 2;
    void *tmp_ptr = realloc(arr->ptr, arr->element_size * arr->capacity);
    if(tmp_ptr)
      arr->ptr = tmp_ptr;
  }
  return 0;
}

static int arr_erase_swap(arr_t *arr, int index)
{
  char *byte_ptr = (char*)arr->ptr;

  void *dst_ptr = byte_ptr + index * arr->element_size;
  void *src_ptr = byte_ptr + (arr->count - 1) * arr->element_size;
  memcpy(dst_ptr, src_ptr, arr->element_size);
  
  arr->count--;

  if(arr->count == 0)
  {
    free(arr->ptr);
    arr->ptr = NULL;
    arr->capacity = 0;
    return 0;
  }

  if(arr->count < arr->capacity / 2)
  {
    arr->capacity /= 2;
    void *tmp_ptr = realloc(arr->ptr, arr->element_size * arr->capacity);
    if(tmp_ptr)
      arr->ptr = tmp_ptr;
  }
  return 0;
}

inline static void *arr_get(arr_t *arr, int index)
{
  return
    (char*)arr->ptr + index * arr->element_size;
}

#define ARR_GET_EL(type, arr, index) (*(type*)arr_get(arr, index))

static void arr_clear(arr_t *arr)
{
  arr->count = 0;
}

// static int arr_clear(arr_t *arr, int new_capacity)
// {
//   // void *tmp_ptr = NULL;

//   // if(new_capacity > 0)
//   // {
//   //   tmp_ptr = malloc(arr->element_size * arr->capacity);
//   //   if(!tmp_ptr)
//   //     return 1;
//   // }
//   // free(arr->ptr);

//   // arr->ptr = tmp_ptr;
//   // arr->count = 0;
//   // arr->capacity = new_capacity;
//   // return 0;
// }

static void arr_free(arr_t **arr)
{
  if(!arr || !*arr)
    return;

  free((*arr)->ptr);
  free(*arr);

  *arr = NULL;
}

#endif