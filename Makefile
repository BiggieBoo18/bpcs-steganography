CFLAGS  = -g -Wall -O2
CC      = gcc
LIBS    = 
TARGET  = ./bin/bitplane
INCLUDE = 
SRCDIR  = ./src
SRCS    = $(wildcard $(SRCDIR)/*.c) # ./src/*.c
OBJDIR  = ./obj
OBJS    = $(addprefix $(OBJDIR)/, $(notdir $(SRCS:.c=.o))) # obj/*.o
DEPS    = $(OBJECTS:.o=.d)

all: clean $(TARGET)

-include $(DEPS)

$(TARGET): $(OBJS)
	$(CC) -o $@ $^ $(LIBS)

$(OBJDIR)/%.o: $(SRCDIR)/%.c
	-mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) $(INCLUDE) -o $@ -c $<

pngtest:
	./bin/bitplane images/sample.png

.PHONY: clean
clean:
	rm -f $(OBJS) $(DEPS) $(TARGET)
