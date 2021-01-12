CC=gcc
CFLAGS=-m32 -march=i386 -fno-stack-protector -static -no-pie -fno-pic
LIB=-L../../__libsym__/ -lsym

.PHONY: clean spectrev4

# Compilation

spectrev4 : spectrev4.c
	$(CC) $(CFLAGS) $< -o $@

clean :
	rm spectrev4
