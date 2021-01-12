CFLAGS=-Wall -m32 -g -fno-stack-protector -static -Wno-parentheses
CFLAGSDYN=-Wall -m32 -g -fno-stack-protector -Wno-parentheses
LIB=-L../../../__libsym__/ -lsym
ENCR=tea_encrypt
DECR=tea_encrypt
NAME=tea
.PHONY: all clean

.PHONY: all tea_decrypt_O0 tea_decrypt_O1 tea_decrypt_O2 tea_decrypt_O3 tea_decrypt_Of tea_encrypt_O0 tea_encrypt_O1 tea_encrypt_O2 tea_encrypt_O3 tea_encrypt_Of

all: tea_decrypt_O0 tea_decrypt_O1 tea_decrypt_O2 tea_decrypt_O3 tea_decrypt_Of tea_encrypt_O0 tea_encrypt_O1 tea_encrypt_O2 tea_encrypt_O3 tea_encrypt_Of

# TEA Decrypt
WRAPPER=${DECR}_wrapper

tea_decrypt_O0:
	gcc $(CFLAGS) ${WRAPPER}.c -O0 -o $@  $(LIB)

tea_decrypt_O1:
	gcc $(CFLAGS) ${WRAPPER}.c -O1 -o $@  $(LIB)

tea_decrypt_O2:
	gcc $(CFLAGS) ${WRAPPER}.c -O2 -o $@  $(LIB)

tea_decrypt_O3:
	gcc $(CFLAGS) ${WRAPPER}.c -O3 -o $@  $(LIB)

tea_decrypt_Of:
	gcc $(CFLAGS) ${WRAPPER}.c -Ofast -o $@  $(LIB)

# TEA Encrypt
WRAPPER=${ENCR}_wrapper

tea_encrypt_O0:
	gcc $(CFLAGS) ${WRAPPER}.c -O0 -o $@  $(LIB)

tea_encrypt_O1:
	gcc $(CFLAGS) ${WRAPPER}.c -O1 -o $@  $(LIB)

tea_encrypt_O2:
	gcc $(CFLAGS) ${WRAPPER}.c -O2 -o $@  $(LIB)

tea_encrypt_O3:
	gcc $(CFLAGS) ${WRAPPER}.c -O3 -o $@  $(LIB)

tea_encrypt_Of:
	gcc $(CFLAGS) ${WRAPPER}.c -Ofast -o $@  $(LIB)

count:													# 7020 + 3901 + 2717 + 4503 + 4503
	gcc $(CFLAGSDYN) -O0 -c $(NAME).c
	objdump $(NAME).o -d -j .text | wc -l
	gcc $(CFLAGSDYN) -O1 -c $(NAME).c
	objdump $(NAME).o -d -j .text | wc -l
	gcc $(CFLAGSDYN) -O2 -c $(NAME).c
	objdump $(NAME).o -d -j .text | wc -l
	gcc $(CFLAGSDYN) -O3 -c $(NAME).c
	objdump $(NAME).o -d -j .text | wc -l
	gcc $(CFLAGSDYN) -Ofast -c $(NAME).c
	objdump $(NAME).o -d -j .text | wc -l

clean:
	rm -rf *.o *.csv *.out smtdir/*/*.smt2

mrproper: clean
	find . -type f -executable | xargs rm
