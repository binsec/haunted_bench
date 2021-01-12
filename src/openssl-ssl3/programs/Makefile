CFLAGS=-m32 -march=i386 -static -Wall -g -O3
LIB= -L../../../__libsym__/ -lsym
WRAPPER=${NAME}_wrapper


.PHONY: clean ssl3_cbc_digest_record

ssl3_cbc_digest_record:
	gcc $(CFLAGS) $@_wrapper.c -o $@  $(LIB)

clean:
	rm -rf *.o *.csv *.out smtdir/*/*.smt2

mrproper: clean
	find . -type f -executable | xargs rm
