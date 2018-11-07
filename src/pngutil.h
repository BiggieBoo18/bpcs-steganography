#ifndef HPNGUTIL
#define HPNGUTIL


typedef struct _PNGCOMMON {
  int length;
  char chunktype[4];
} PNGCOMMON, *PPNGCOMMON;

typedef struct _PNGIHDR {
  int width;
  int height;
  char bitdepth;
  char colortype;
  char compression;
  char filter;
  char interlace;
  int crc;
} PNGIHDR, *PPNGIHDR;

typedef struct _PNGIEND {
}

typedef struct _PNGFORMAT {
  char signature[8];
  PNGCOMMON common;
  PNGIHDR ihdr;
} PNGFORMAT, *PPNGFORMAT;

int png_parser(FILE *fp, PPNGFORMAT fmt);
int png_viewer(PPNGFORMAT fmt);
int png_check_signature(char *signature);

#endif
