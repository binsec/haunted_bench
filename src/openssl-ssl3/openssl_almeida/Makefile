CLFLAGS=-m32 -g -static -Wall -O3
CFLAGS=$(CLFLAGS) -fno-stack-protector
LIB= -L../__libsym__/ -lsym


.PHONY: tls1_cbc_remove_padding_patch tls1_cbc_remove_padding_lucky13

all: tls1_cbc_remove_padding_patch tls1_cbc_remove_padding_lucky13

tls1_cbc_remove_padding_patch:
	gcc $(CFLAGS) $@_wrapper.c -o $@ $(LIB)

tls1_cbc_remove_padding_lucky13:
	gcc $(CFLAGS) $@_wrapper.c -o $@ $(LIB)

# ssl3_cbc_copy_mac:
# 	gcc $(CFLAGS) $@_wrapper.c -O0 -o $@ $(LIB)

clean:
	rm -rf *.o *.csv *.out smtdir/*/*.smt2

mrproper: clean
	find . -type f -executable | xargs rm
