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

  fmt.chunks       = (PCHUNKS)malloc(sizeof(CHUNKS));
  fmt.chunks->next = NULL;
  if (png_parser(fp, &fmt)) {
    fprintf(stderr, "[!] Unexpected image format or other errors!\n");
    return(EXIT_FAILURE);
  }
  png_viewer(&fmt);

  fclose(fp);
  return (EXIT_SUCCESS);
}
