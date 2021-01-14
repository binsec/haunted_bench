CC=gcc
CFLAGS=-m32 -march=i386 -fno-stack-protector -static -no-pie -fno-pic

.PHONY: clean spectrev1 spectrev4

all: spectrev1 spectrev4

# Compilation

spectrev1 : spectrev1.c
	$(CC) $(CFLAGS) $< -o $@

spectrev4 : spectrev4.c
	$(CC) $(CFLAGS) $< -o $@

clean :
	rm spectrev1 spectrev4
