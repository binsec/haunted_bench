CFLAGS=-m32 -march=i386 -static -Wall -fno-stack-protector -g
LIB= -L../../../__libsym__/ -lsym
LIBCRYPTO= -I./libsodium/inc/ ./libsodium/lib/libsodium.a
WRAPPER=${NAME}_wrapper


.PHONY: clean secretbox secretbox_easy

secretbox:
	gcc $(CFLAGS) $@_wrapper.c -o $@  $(LIB) $(LIBCRYPTO)

secretbox_easy:
	gcc $(CFLAGS) $@_wrapper.c -o $@  $(LIB) $(LIBCRYPTO)

clean:
	rm -rf *.o *.csv *.out smtdir/*/*.smt2

mrproper: clean
	find . -type f -executable | xargs rm
