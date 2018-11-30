#ifndef HPNGUTIL
#define HPNGUTIL
#pragma pack(1)

typedef struct _PNGCOMMON {
  int  length;
  char chunktype[4];
} PNGCOMMON, *PPNGCOMMON;

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
  int data[8];
  int crc;
} PNGCHRM, *PPNGCHRM;

typedef struct _PNGTRNS {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGTRNS, *PPNGTRNS;

typedef struct _PNGSRGB {
  PNGCOMMON common;
  char      data;
  int       crc;
} PNGSRGB, *PPNGSRGB;

typedef struct _PNGICCP {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGICCP, *PPNGICCP;

typedef struct _PNGTEXT {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGTEXT, *PPNGTEXT;

typedef struct _PNGBKGD {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGBKGD, *PPNGBKGD;

typedef struct _PNGSBIT {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGSBIT, *PPNGSBIT;

typedef struct _PNGSPLT {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGSPLT, *PPNGSPLT;

typedef struct _PNGHIST {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGHIST, *PPNGHIST;

typedef struct _PNGPHYS {
  PNGCOMMON common;
  char      data[9];
  int       crc;
} PNGPHYS, *PPNGPHYS;

typedef struct _PNGIDAT {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGIDAT, *PPNGIDAT;

typedef struct _PNGZTXT {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGZTXT, *PPNGZTXT;

typedef struct _PNGITXT {
  PNGCOMMON common;
  char     *data;
  int       crc;
} PNGITXT, *PPNGITXT;

typedef struct _PNGTIME {
  PNGCOMMON common;
  char      data[7];
  int       crc;
} PNGTIME, *PPNGTIME;

typedef struct _PNGIEND {
  PNGCOMMON common;
  int       crc;
} PNGIEND, *PPNGIEND;

typedef union _U_CHUNKS {
  PNGPLTE plte;
  PNGGAMA gama;
  PNGCHRM chrm;
  PNGTRNS trns;
  PNGSRGB srgb;
  PNGICCP iccp;
  PNGTEXT text;
  PNGBKGD bkgd;
  PNGSBIT sbit;
  PNGSPLT splt;
  PNGHIST hist;
  PNGPHYS phys;
  PNGIDAT idat;
  PNGZTXT ztxt;
  PNGITXT itxt;
  PNGTIME time;
} U_CHUNKS, *PU_CHUNKS;

typedef struct _CHUNKS {
  char           *chunk_name;
  U_CHUNKS        chunk;
  struct _CHUNKS *next;
} CHUNKS, *PCHUNKS;

typedef struct _PNGFORMAT {
  char      signature[8];
  int       nidat;
  PNGIHDR   ihdr;
  PCHUNKS   chunks;
  PNGIEND   iend;
} PNGFORMAT, *PPNGFORMAT;

int png_check_signature(char *signature);
int png_parser(FILE *fp, PPNGFORMAT fmt);
int png_extract_idats(PCHUNKS **idats, PPNGFORMAT fmt);
int png_extract_image(PPNGFORMAT fmt);
int png_viewer(PPNGFORMAT fmt);

#endif
