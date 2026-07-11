#ifndef DATA
#define DATA

#include <stdio.h>

// example triangle structure
typedef struct triangle3_t
{
  float x, y, z;
} triangle3_t;

// use tag
// @SSSG [1]
typedef struct data_t
{
  int count;
  int max;
  char key;
  triangle3_t triangle;

  triangle3_t triangles[10];
  int fixed_size_arr[32];

  // set size variable before array !!
  int size;

  // if it is array use tag and size
  int* dynamic_size_arr; // @SIZE [s->size]
  
  // if it is NOT array (just pointer to value) not use tag
  int *pointer_to_value;
} data_t;

#endif // DATA  