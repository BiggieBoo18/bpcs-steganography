#ifndef HPNGUTIL
#define HPNGUTIL

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

int png_parser(FILE *fp, PPNGFORMAT fmt);
int png_viewer(PPNGFORMAT fmt);

#endif

