CC=gcc
CFLAGS=-g -Wall

all: getip

%: %.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -rf *.dSYM getip
