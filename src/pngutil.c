#include <stdio.h>
#include "pngutil.h"
#include "util.h"

int png_parser(FILE *fp, PPNGFORMAT fmt) {
  fread(&fmt->signature, 1, sizeof(fmt->signature), fp);
  fread(&fmt->ihdr, sizeof(fmt->ihdr), 1, fp);
  return (0);
}

int png_viewer(PPNGFORMAT fmt) {
  int  i=0;
  printf("PNG Format\n");
  printf("SIGNATURE:");
  for (i=0; fmt->signature[i]!='\0'; i++) {
    printf("0x%02X ", fmt->signature[i]&0x000000FF);
  }
  printf("\n");
  printf("  IHDR\n");
  printf("    length:0x%X\n", le2be(fmt->ihdr.length));
  printf("    chunktype:");
  for (i=0; fmt->ihdr.chunktype[i]!='\0'; i++) {
    printf("0x%02X ", fmt->ihdr.chunktype[i]&0x000000FF);
  }
  printf("\n");
  printf("    width:0x%08X\n", le2be(fmt->ihdr.width));
  printf("    height:0x%08X\n", le2be(fmt->ihdr.height));
  printf("    bitdepth:0x%X\n", fmt->ihdr.bitdepth);
  printf("    colortype:0x%X\n", fmt->ihdr.colortype);
  printf("    compression:0x%X\n", fmt->ihdr.compression);
  printf("    filter:0x%X\n", fmt->ihdr.filter);
  printf("    interlace:0x%X\n", fmt->ihdr.interlace);
  printf("    crc:0x%08X\n", fmt->ihdr.crc);
  return (0);
}
