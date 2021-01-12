CFLAGS=-m32 -march=i386 -static -Wall -g -O3 -Wno-parentheses
WRAPPER=${NAME}_wrapper


.PHONY: clean mee-cbc

mee-cbc:
	gcc -Imac-then-encrypt \
      mac-then-encrypt/aes128.c mac-then-encrypt/aes128cbc.c \
      mac-then-encrypt/sha256blocks.c mac-then-encrypt/hmac.c mac-then-encrypt/verify_32.c \
      mac-then-encrypt/pad128.c mac-then-encrypt/pad_cbc_aes128.c \
      mac-then-encrypt/mac_then_encrypt.c \
      $(CFLAGS) $@_wrapper.c -o $@  $(LIB)

clean:
	rm -rf *.o *.csv *.out smtdir/*/*.smt2

mrproper: clean
	find . -type f -executable | xargs rm
