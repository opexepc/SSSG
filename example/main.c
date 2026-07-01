// example used SSS

#include <stdio.h>
#include "data.h"
#include "SSS_data.h"

#define PATH "data.bin"
// use flag for remove file
#define REMOVE_FLAG "-r"

// default data (if file not exist aka 1st run)
const data_t def_data =
{
  .count = 238,
  .key = 's',
  .max = 1700,
  .triangle = {0.509, 2.93, -0.7012}
};

static void print_data(data_t *data)
{
  printf("> DATA INFO <\n");
  printf("count = %d\n", data->count);
  printf("max = %d\n", data->max);
  printf("key = %c\n", data->key);

  printf("triangle X = %f\n", data->triangle.x);
  printf("triangle Y = %f\n", data->triangle.y);
  printf("triangle Z = %f\n", data->triangle.z);
}

int main(int argc, char *argv[])
{
  // remove .bin file
  for(int i = 0; i < argc; ++i)
  {
    if(strcmp(argv[i], REMOVE_FLAG) == 0)
      remove(PATH);
  }

  // runtime struct
  data_t data;

  // read structure
  FILE *f_in = fopen(PATH, "rb");
  if(!f_in)
    data = def_data;
  else
    SSS_read_data_t(f_in, &data);

  // print structure
  print_data(&data);
  
  // write structure
  FILE *f_out = fopen(PATH, "wb");
  if(f_out)
    SSS_write_data_t(f_out, &data);

  return 0;
}