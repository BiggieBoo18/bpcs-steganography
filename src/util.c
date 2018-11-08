#include <stdio.h>
#include "util.h"

void usage(char *argv) {
  printf("Usage: %s <IMAGE PATH>\n", argv);
}

int le2be(int src) {
  int ret     = 0;
  int i       = 0;
  int srcsize = sizeof(src);
  int mask, masked = 0;
  for (i=0; i<(srcsize-1); i++) {
    mask = 0xFF<<(srcsize*2*(srcsize-1-i));
    masked = (src&mask)>>(srcsize*2*(srcsize-1-(i*2)));
    printf("mask:0x%X\n", mask);
    printf("src:0x%X->0x%X\n", src, masked);
    printf("ret:0x%X\n", ret);
    ret |= masked;
  }
  return (ret);
}
