#include <stdio.h>
#include <stdlib.h>
#include "pngutil.h"
#include "util.h"

int main(int argc, char *argv[]) {
  FILE *fp;
  PNGFORMAT fmt;

  // argument parse
  if (argc<2) {
    usage(*argv);
    return(EXIT_FAILURE);
  }

  if ((fp = fopen(argv[1], "rb"))==NULL) {
    perror("fopen");
    return(EXIT_FAILURE);
  }

  fmt.nidat        = 0;
  fmt.chunks       = (PCHUNKS)malloc(sizeof(CHUNKS));
  fmt.chunks->next = NULL;
  if (!png_parser(fp, &fmt)) { // png
    png_viewer(&fmt);
    if (png_extract_image(&fmt)) {
      fprintf(stderr, "[!] Failed to extract image!\n");
      return (EXIT_FAILURE);
    }
  } else {
    fprintf(stderr, "[!] Unexpected image format or other errors!\n");
    return(EXIT_FAILURE);
  }

  fclose(fp);
  return (EXIT_SUCCESS);
}
