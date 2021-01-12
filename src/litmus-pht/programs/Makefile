CC=gcc
CFLAGS=-m32 -march=i386 -fno-stack-protector
LIB=-L../../__libsym__/ -lsym

.PHONY: clean spectrev1

# Compilation

spectrev1 : spectrev1.c
	$(CC) $(CFLAGS) $< -o $@

clean :
	rm spectrev1 forwarding
