#ifndef DATA
#define DATA

#include <stdio.h>

// example triangle structure
typedef struct triangle3_t
{
  float x, y, z;
} triangle3_t;

// use tag
// @SSSG
typedef struct data_t
{
  int count;
  int max;
  char key;
  triangle3_t triangle;
} data_t;

#endif // DATA