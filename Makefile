open_image: open_image.o util.o
	gcc -o open_image open_image.o util.o

open_image.o: open_image.c
	gcc -c open_image.c

util.o: util.c
	gcc -c util.c
