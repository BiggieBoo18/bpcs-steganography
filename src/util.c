#include <stdio.h>
#include "util.h"

void usage(char *argv) {
  printf("Usage: %s <IMAGE PATH>\n", argv);
}

/* REF:https://qiita.com/tobira-code/items/a03f39a02678d80bbd26 */
unsigned short swap16(unsigned short value) {
  unsigned short ret;
  ret  = value << 8;
  ret |=value  >> 8;
  return (ret);
}

unsigned int swap32(unsigned int value) {
  unsigned int ret;
  ret  = value              << 24;
  ret |= (value&0x0000FF00) << 8;
  ret |= (value&0x00FF0000) >> 8;
  ret |= value              >> 24;
  return (ret);
}
