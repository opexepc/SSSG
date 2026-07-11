set -e

python ../sssg.py -i data.h -o SSS_data.h -p patterns.txt @i data.h @i ../include/sss.h @s 10000000
gcc main.c -o app