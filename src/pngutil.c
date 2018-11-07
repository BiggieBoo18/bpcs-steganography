#include <stdio.h>
#include <string.h>
#include "pngutil.h"
#include "util.h"

int png_checksig(char *signature) {
    int ret = 0; // true if ret==0, false if ret==1
    int i   = 0;
    char png_signature[9] = {0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, '\0'};
    for (i=0; png_signature[i]!='\0'; i++) {
        if (png_signature[i]!=signature[i]) {
            ret = 1;
        }
    }
    return (ret);
}

int png_parser(FILE *fp, PPNGFORMAT fmt) {
  fread(&fmt->signature, 1, sizeof(fmt->signature), fp);
  if (png_checksig(fmt->signature)) {
      return (1);
  }
  fread(&fmt->common.length, sizeof(fmt->common.length), 1, fp);
  fread(&fmt->common.chunktype, sizeof(fmt->common.chunktype), 1, fp);
  if (strcmp(fmt->ihdr.chunktype, "IHDR")==0) {
    fread(&fmt->ihdr.width, sizeof(fmt->ihdr.width), 1, fp);
    fread(&fmt->ihdr.height, sizeof(fmt->ihdr.height), 1, fp);
    fread(&fmt->ihdr.bitdepth, sizeof(fmt->ihdr.bitdepth), 1, fp);
    fread(&fmt->ihdr.colortype, sizeof(fmt->ihdr.colortype), 1, fp);
    fread(&fmt->ihdr.compression, sizeof(fmt->ihdr.compression), 1, fp);
    fread(&fmt->ihdr.filter, sizeof(fmt->ihdr.filter), 1, fp);
    fread(&fmt->ihdr.interlace, sizeof(fmt->ihdr.interlace), 1, fp);
    fread(&fmt->ihdr.crc, sizeof(fmt->ihdr.crc), 1, fp);
  }
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
  printf("    length:0x%X\n", le2be(fmt->common.length));
  printf("    chunktype:");
  for (i=0; fmt->common.chunktype[i]!='\0'; i++) {
    printf("0x%02X ", fmt->ihdr.chunktype[i]&0x000000FF);
  }
  printf("\n");
  printf("    sizeof(char)=%ld\n", sizeof(char));
  printf("    sizeof(fmt->ihdr)=%ld\n", sizeof(fmt->ihdr));
  printf("        length:%ld\n", sizeof(fmt->ihdr.length));
  printf("        chunktype:%ld\n", sizeof(fmt->ihdr.chunktype));
  printf("        width:%ld\n", sizeof(fmt->ihdr.width));
  printf("        height:%ld\n", sizeof(fmt->ihdr.height));
  printf("        bitdepth:%ld\n", sizeof(fmt->ihdr.bitdepth));
  printf("        colortype:%ld\n", sizeof(fmt->ihdr.colortype));
  printf("        compression:%ld\n", sizeof(fmt->ihdr.compression));
  printf("        filter:%ld\n", sizeof(fmt->ihdr.filter));
  printf("        interlace:%ld\n", sizeof(fmt->ihdr.interlace));
  printf("        crc:%ld\n", sizeof(fmt->ihdr.crc));
  printf("    width:0x%08X\n", le2be(fmt->ihdr.width));
  printf("    height:0x%08X\n", le2be(fmt->ihdr.height));
  printf("    bitdepth:0x%X\n", fmt->ihdr.bitdepth);
  printf("    colortype:0x%X\n", fmt->ihdr.colortype);
  printf("    compression:0x%X\n", fmt->ihdr.compression);
  printf("    filter:0x%X\n", fmt->ihdr.filter);
  printf("    interlace:0x%X\n", fmt->ihdr.interlace);
  printf("    crc:0x%08X\n", fmt->ihdr.crc);
  /* printf("    crc:0x%lX\n", fmt->ihdr.crc); */
  return (0);
}
