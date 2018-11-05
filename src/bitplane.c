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
