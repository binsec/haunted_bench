CC=gcc
CFLAGS=-m32 -march=i386 -fno-stack-protector
LIB=-L../../__libsym__/ -lsym

.PHONY: clean

# Compilation

spectrev1 : spectrev1.c
	$(CC) $(CFLAGS) $< -o $@

spectrev1_masking : spectrev1_masking.c
	$(CC) $(CFLAGS) $< -o $@

forwarding : forwarding.c
	$(CC) $(CFLAGS) $< -o $@

clean :
	rm spectrev1 forwarding
