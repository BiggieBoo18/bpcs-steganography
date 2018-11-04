#include <stdio.h>
#include <stdlib.h>
#include "util.h"

typedef struct _PNGIHDR {
  int length;
  char chunktype[4];
  int width;
  int height;
  char bitdepth;
  char colortype;
  char compression;
  char filter;
  char interlace;
  int crc;
} PNGIHDR, *PPNGIHDR;

typedef struct _PNGFORMAT {
  char signature[8];
  PNGIHDR ihdr;
} PNGFORMAT, *PPNGFORMAT;

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
  printf("    length:0x%X\n", fmt->ihdr.length);
  printf("    chunktype:");
  for (i=0; fmt->ihdr.chunktype[i]!='\0'; i++) {
    printf("0x%02X ", fmt->ihdr.chunktype[i]&0x000000FF);
  }
  printf("\n");
  printf("    width:0x%08X\n", fmt->ihdr.width);
}

int main(int argc, char *argv[]) {
  FILE *fp;
  PNGFORMAT fmt;

  // argument parse
  if (argc<2) {
    usage(*argv);
    exit(EXIT_FAILURE);
  }

  if ((fp = fopen(argv[1], "rb"))==NULL) {
    perror("fopen");
    exit(EXIT_FAILURE);
  }

  png_parser(fp, &fmt);
  png_viewer(&fmt);

  fclose(fp);
  return (EXIT_SUCCESS);
}
