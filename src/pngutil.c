#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "pngutil.h"
#include "util.h"

int png_checksig(char *signature) {
    int ret = 0; // true if ret==0, false if ret==1
    int i   = 0;
    char png_signature[8] = {0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A};
    for (i=0; i<sizeof(png_signature); i++) {
        if (png_signature[i]!=signature[i]) {
            ret = 1;
        }
    }
    return (ret);
}

int png_parser(FILE *fp, PPNGFORMAT fmt) {
  int       i = 0;
  PNGCOMMON common;
  PCHUNKS   current_chunk = fmt->chunks;

  fread(&fmt->signature, 1, sizeof(fmt->signature), fp);
  if (png_checksig(fmt->signature)) {
    return (1);
  }
  while (strcmp(common.chunktype, "IEND")!=0) { // break if IEND
    fread(&common.length, sizeof(common.length), 1, fp); // COMMON
    fread(&common.chunktype, sizeof(common.chunktype), 1, fp); // COMMON
    common.length = swap32(common.length); // swap bytes
    if (strcmp(common.chunktype, "IHDR")==0) { // IHDR
      puts("here1");
      memcpy(&fmt->ihdr.common.length, &common.length, sizeof(common.length));
      memcpy(fmt->ihdr.common.chunktype, common.chunktype, sizeof(common.chunktype));
      fread(&fmt->ihdr.common+1, fmt->ihdr.common.length+sizeof(fmt->ihdr.crc), 1, fp); // data+crc
      /* fread(&fmt->ihdr.width, sizeof(fmt->ihdr.width), 1, fp); */
      /* fread(&fmt->ihdr.height, sizeof(fmt->ihdr.height), 1, fp); */
      /* fread(&fmt->ihdr.bitdepth, sizeof(fmt->ihdr.bitdepth), 1, fp); */
      /* fread(&fmt->ihdr.colortype, sizeof(fmt->ihdr.colortype), 1, fp); */
      /* fread(&fmt->ihdr.compression, sizeof(fmt->ihdr.compression), 1, fp); */
      /* fread(&fmt->ihdr.filter, sizeof(fmt->ihdr.filter), 1, fp); */
      /* fread(&fmt->ihdr.interlace, sizeof(fmt->ihdr.interlace), 1, fp); */
      /* fread(&fmt->ihdr.crc, sizeof(fmt->ihdr.crc), 1, fp); */
    } else if (strcmp(common.chunktype, "PLTE")==0) { // PLTE
      puts("here2");
      current_chunk->next = (PCHUNKS)malloc(sizeof(CHUNKS));
      current_chunk       = current_chunk->next;
      current_chunk->next = NULL;
      current_chunk->chunk_name = "PLTE";
      memcpy(&current_chunk->chunk.plte.common.length, &common.length, sizeof(common.length));
      memcpy(current_chunk->chunk.plte.common.chunktype, common.chunktype, sizeof(common.chunktype));
      current_chunk->chunk.plte.data = (char *)malloc(current_chunk->chunk.plte.common.length);
      for (i=0; i<current_chunk->chunk.plte.common.length; i++) {
        fread(&current_chunk->chunk.plte.data[i], sizeof(current_chunk->chunk.plte.data[i]), 1, fp);
      }
      fread(&current_chunk->chunk.plte.crc, sizeof(current_chunk->chunk.plte.crc), 1, fp);
    } else if (strcmp(common.chunktype, "gAMA")==0) { // gAMA
      puts("here3");
      current_chunk->next = (PCHUNKS)malloc(sizeof(CHUNKS));
      current_chunk       = current_chunk->next;
      current_chunk->next = NULL;
      current_chunk->chunk_name = "gAMA";
      memcpy(&current_chunk->chunk.gama.common.length, &common.length, sizeof(common.length));
      memcpy(current_chunk->chunk.gama.common.chunktype, common.chunktype, sizeof(common.chunktype));
      fread(&current_chunk->chunk.gama.data, sizeof(current_chunk->chunk.gama.data), 1, fp);
      fread(&current_chunk->chunk.gama.crc, sizeof(current_chunk->chunk.gama.crc), 1, fp);
    } else if (strcmp(common.chunktype, "cHRM")==0) { // cHRM
      puts("here4");
      current_chunk->next = (PCHUNKS)malloc(sizeof(CHUNKS));
      current_chunk       = current_chunk->next;
      current_chunk->next = NULL;
      current_chunk->chunk_name = "cHRM";
      memcpy(&current_chunk->chunk.chrm.common.length, &common.length, sizeof(common.length));
      memcpy(current_chunk->chunk.chrm.common.chunktype, common.chunktype, sizeof(common.chunktype));
      for (i=0; i<current_chunk->chunk.chrm.common.length; i++) {
        fread(&current_chunk->chunk.chrm.data[i], sizeof(current_chunk->chunk.chrm.data[i]), 1, fp);
      }
      fread(&current_chunk->chunk.chrm.crc, sizeof(current_chunk->chunk.chrm.crc), 1, fp);
    }  else if (strcmp(common.chunktype, "tRNS")==0) { // tRNS
      puts("here5");
      current_chunk->next = (PCHUNKS)malloc(sizeof(CHUNKS));
      current_chunk       = current_chunk->next;
      current_chunk->next = NULL;
      current_chunk->chunk_name = "tRNS";
      memcpy(&current_chunk->chunk.trns.common.length, &common.length, sizeof(common.length));
      memcpy(current_chunk->chunk.trns.common.chunktype, common.chunktype, sizeof(common.chunktype));
      current_chunk->chunk.trns.data = (char *)malloc(current_chunk->chunk.trns.common.length);
      for (i=0; i<current_chunk->chunk.trns.common.length; i++) {
        fread(&current_chunk->chunk.trns.data[i], sizeof(current_chunk->chunk.trns.data[i]), 1, fp);
      }
      fread(&current_chunk->chunk.trns.crc, sizeof(current_chunk->chunk.trns.crc), 1, fp);
    } else if (strcmp(common.chunktype, "IDAT")==0) { // IDAT
      puts("here6");
      current_chunk->next = (PCHUNKS)malloc(sizeof(CHUNKS));
      current_chunk       = current_chunk->next;
      current_chunk->next = NULL;
      current_chunk->chunk_name = "IDAT";
      memcpy(&current_chunk->chunk.idat.common.length, &common.length, sizeof(common.length));
      memcpy(current_chunk->chunk.idat.common.chunktype, common.chunktype, sizeof(common.chunktype));
      current_chunk->chunk.idat.data = (char *)malloc(current_chunk->chunk.idat.common.length);
      for (i=0; i<current_chunk->chunk.idat.common.length; i++) {
          fread(&current_chunk->chunk.idat.data[i], sizeof(current_chunk->chunk.idat.data[i]), 1, fp);
      }
      fread(&current_chunk->chunk.idat.crc, sizeof(current_chunk->chunk.idat.crc), 1, fp);
    } else if (strcmp(common.chunktype, "IEND")==0) { // IEND
      puts("here7");
      memcpy(&fmt->iend.common.length, &common.length, sizeof(common.length));
      memcpy(fmt->iend.common.chunktype, common.chunktype, sizeof(common.chunktype));
      fread(&fmt->iend.crc, sizeof(fmt->iend.crc), 1, fp);
    } else {
      printf("%p\n", current_chunk->next);
      printf("%s\n", common.chunktype);
      return (1);
    }
  }
  return (0);
}

int png_viewer(PPNGFORMAT fmt) {
  int  i=0;
  PCHUNKS   current_chunk = fmt->chunks;
  printf("PNG Format\n");
  printf("SIGNATURE:");
  for (i=0; i<sizeof(fmt->signature); i++) {
    printf("0x%02X ", fmt->signature[i]&0x000000FF);
  }
  printf("\n");
  printf("  IHDR\n");
  printf("    length:0x%X\n", fmt->ihdr.common.length);
  printf("    chunktype:");
  for (i=0; i<sizeof(fmt->ihdr.common.chunktype); i++) {
    printf("0x%02X ", fmt->ihdr.common.chunktype[i]&0x000000FF);
  }
  printf("\n");
  printf("    width:0x%08X\n", swap32(fmt->ihdr.width));
  printf("    height:0x%08X\n", swap32(fmt->ihdr.height));
  printf("    bitdepth:0x%X\n", fmt->ihdr.bitdepth);
  printf("    colortype:0x%X\n", fmt->ihdr.colortype);
  printf("    compression:0x%X\n", fmt->ihdr.compression);
  printf("    filter:0x%X\n", fmt->ihdr.filter);
  printf("    interlace:0x%X\n", fmt->ihdr.interlace);
  printf("    crc:0x%08X\n", fmt->ihdr.crc);
  current_chunk = fmt->chunks->next;
  do {
    if (current_chunk==0x0) {
      puts("here");
    } else {
      puts("not");
    }
    printf("current_chunk=%p\n", current_chunk);
    /* printf(", %s\n", current_chunk->chunk_name); */
    if (strcmp(current_chunk->chunk_name, "gAMA")==0) {
      printf("  gAMA\n");
      printf("    length:0x%X\n", fmt->chunks->next->chunk.gama.common.length);
      printf("    chunktype:");
      for (i=0; i<sizeof(current_chunk->chunk.gama.common.chunktype); i++) {
        printf("0x%02X ", current_chunk->chunk.gama.common.chunktype[i]&0x000000FF);
      }
      printf("\n");
      printf("    data:0x%X\n", swap32(current_chunk->chunk.gama.data));
      printf("    crc:0x%08X\n", swap32(current_chunk->chunk.gama.crc));
    }
  } while ((current_chunk = current_chunk->next));
  return (0);
}
