#ifndef HPNGUTIL
#define HPNGUTIL

typedef struct _PNGCOMMON {
  int  length;
  char chunktype[4];
} PNGCOMMON, *PPNGCOMMON;

#pragma pack(1)
typedef struct _PNGIHDR {
  PNGCOMMON common;
  int       width;
  int       height;
  char      bitdepth;
  char      colortype;
  char      compression;
  char      filter;
  char      interlace;
  int       crc;
} PNGIHDR, *PPNGIHDR;
#pragma pack()

typedef struct _PNGPLTE {
  PNGCOMMON common;
  char *data;
  int crc;
} PNGPLTE, *PPNGPLTE;

typedef struct _PNGGAMA {
  PNGCOMMON common;
  int data;
  int crc;
} PNGGAMA, *PPNGGAMA;

typedef struct _PNGCHRM {
  PNGCOMMON common;
  int data[32];
  int crc;
} PNGCHRM, *PPNGCHRM;

typedef struct _PNGTRNS {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGTRNS, *PPNGTRNS;

typedef struct _PNGIDAT {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGIDAT, *PPNGIDAT;

typedef struct _PNGIEND {
  PNGCOMMON common;
  int       crc;
} PNGIEND, *PPNGIEND;

typedef union _U_CHUNKS {
  PNGPLTE plte;
  PNGGAMA gama;
  PNGCHRM chrm;
  PNGTRNS trns;
  PNGIDAT idat;
} U_CHUNKS, *PU_CHUNKS;

typedef struct _CHUNKS {
  char           *chunk_name;
  U_CHUNKS        chunk;
  struct _CHUNKS *next;
} CHUNKS, *PCHUNKS;

typedef struct _PNGFORMAT {
  char      signature[8];
  PNGIHDR   ihdr;
  PCHUNKS   chunks;
  PNGIEND   iend;
} PNGFORMAT, *PPNGFORMAT;

int png_parser(FILE *fp, PPNGFORMAT fmt);
int png_viewer(PPNGFORMAT fmt);
int png_check_signature(char *signature);

#endif
