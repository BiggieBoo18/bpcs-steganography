#include <stdio.h>
#include "util.h"

void usage(char *argv) {
  printf("Usage: %s <IMAGE PATH>\n", argv);
}

int le2be(int src) {
  int ret     = 0;
  int i       = 0;
  int srcsize = sizeof(src);
  int mask1, mask2, masked = 0;
  for (i=0; i<(srcsize-1); i++) {
    mask1   = 0xFF<<(srcsize*2*(srcsize-1-i));
    mask2   = 0xFF<<(srcsize*(i*2));
    masked  = (src&mask1)>>(-(srcsize*2*(srcsize-1-(i*2))));
    masked &= mask2;
    ret    |= masked;
    printf("mask1:0x%X\n", mask1);
    printf("mask2:0x%X\n", mask2);
    printf("src:0x%X->0x%X(0x%X>>%ld*2*(%ld-1-(%ld*2)))\n", src, masked, src&mask1, srcsize, srcsize, i);
    printf("ret:0x%X\n", ret);
  }
  return (ret);
}
