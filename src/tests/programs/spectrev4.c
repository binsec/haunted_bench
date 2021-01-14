// Set of litmus tests for Spectre-v4

#include <stdint.h>
#include <stddef.h>

uint32_t publicarray_size = 16;
uint8_t publicarray[16] = { 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 };
uint8_t publicarray2[512 * 256] = { 20 };

// The attacker's goal in all of these examples is to learn any of the secret data in secretarray
uint32_t secretarray_size = 16;
uint8_t secretarray[16] = { 10,21,32,43,54,65,76,87,98,109,110,121,132,143,154,165 };

// this is mostly used to prevent the compiler from optimizing out certain operations
volatile uint8_t temp = 0;


// In all of these examples, the arguments to the functions are attacker-controlled

/* Examples marked as INSECURE violate Speculative Constant-Time (SCT)
   when compiled with gcc-10.2.0 -O0 -m32 -march=i386
   -fno-stack-protector -static -no-pie -fno-pic */


/* Based on original POC for Spectre-v4 */
/* https://github.com/IAIK/transientfail/blob/master/pocs/spectre/STL/main.c */
void case_1(uint32_t idx) {  /* INSECURE */
  register uint32_t ridx asm ("edx");
  ridx = idx & (secretarray_size - 1);

  uint8_t* data = secretarray;
  uint8_t** data_slowptr = &data;
  uint8_t*** data_slowslowptr = &data_slowptr;
  
  /* Overwrite secret value */
  (*(*data_slowslowptr))[ridx] = 0; // Bypassed store
  
  /* Access overwritten secret */
  temp &= publicarray2[secretarray[ridx] * 512];  
}



/* Discalaimer: The following test cases are probably not vulnerable
   to Spectre-STL attacks because the stored that are supposed to be
   bypassed are fast. They can however be adapted following the method
   in case_1 to slow down the store to bypass. */

/* The example is insecure because index masking is compiled to a
   store that can be bypassed */
void case_2(uint32_t idx) { // INSECURE
  idx = idx & (publicarray_size - 1);
  
  /* Access overwritten secret */
  temp &= publicarray2[publicarray[idx] * 512];  
}

/* Same example as before but the index is put in a register so the
   example is now secure */
void case_3(uint32_t idx) { // SECURE
  register uint32_t ridx asm ("edx");
  ridx = idx & (secretarray_size - 1);
  
  /* Access overwritten secret */
  temp &= publicarray2[publicarray[ridx] * 512];  
}

/* In the following examples the index is put in a register so the
   masking is never bypassed */

/* Similar to case_1 but without intermediate pointers */
void case_4(uint32_t idx) { // INSECURE
  register uint32_t ridx asm ("edx");
  ridx = idx & (secretarray_size - 1);

  /* Overwrite secret value */
  secretarray[ridx] = 0;  // Bypassed store
  
  /* Access overwritten secret */
  temp &= publicarray2[secretarray[ridx] * 512];  
}

uint8_t *case5_ptr = secretarray;
void case_5(uint32_t idx) {  // INSECURE
  register uint32_t ridx asm ("edx");
  ridx = idx & (secretarray_size - 1);
  
  case5_ptr = publicarray;       // Bypassed store

  uint8_t toleak = case5_ptr[ridx];
  temp &= publicarray2[toleak * 512];   
}

uint32_t case6_idx = 0;
uint8_t *case6_array[2] = { secretarray, publicarray };
void case_6(uint32_t idx) { // INSECURE
  register uint32_t ridx asm ("edx");
  ridx = idx & (secretarray_size - 1);

  case6_idx = 1;       // Bypassed store

  uint8_t toleak = (case6_array[case6_idx])[ridx];
  temp &= publicarray2[toleak * 512];
}


uint32_t case7_mask = UINT32_MAX;
void case_7(uint32_t idx) {  // INSECURE
  case7_mask = (secretarray_size - 1); // Bypassed store

  uint8_t toleak = publicarray[idx & case7_mask];
  temp &= publicarray2[toleak * 512];
}

uint32_t case8_mult = 200;

void case_8(uint32_t idx) {  // INSECURE
  case8_mult = 0; // Bypassed store

  uint8_t toleak = publicarray[idx * case8_mult];
  temp &= publicarray2[toleak * 512];
}

/* This store should be secure assuming no speculation on conditionals
   because when the programs fetches the last line, the store that
   overwrites the secret should be retired. */
void case_9(uint32_t idx) {  // SECURE
  register uint32_t ridx asm ("edx");
  ridx = idx & (secretarray_size - 1);

  /* Overwrite secret value */
  secretarray[ridx] = 0;  // Bypassed store
  
  register uint32_t i asm ("ecx");
  for (i = 0; i < 200; ++i) temp &= i;
  
  /* Access overwritten secret */
  temp &= publicarray2[secretarray[ridx] * 512];  
}

/* Same as case 8 but this time the store is not retired yet when the
   load is executed. */
void case_9_bis(uint32_t idx) { // INSECURE
  register uint32_t ridx asm ("edx");
  ridx = idx & (secretarray_size - 1);

  /* Overwrite secret value */
  secretarray[ridx] = 0;  // Bypassed store
  
  register uint32_t i asm ("ecx");
  for (i = 0; i < 10; ++i) temp &= i;
  
  /* Access overwritten secret */
  temp &= publicarray2[secretarray[ridx] * 512];  
}

/* Same as case 3 (secure) but masking is made by a function call */
uint32_t case_10_mask(uint32_t idx) {
  register uint32_t ridx asm ("edx");
  ridx = idx & (secretarray_size - 1);
  return ridx;
}
void case_10(uint32_t idx) { // INSECURE
  uint32_t fidx = case_10_mask(idx);
  
  /* Access overwritten secret */
  temp &= publicarray2[publicarray[fidx] * 512];  
}

/* Same as case 3 (secure) but first load is made by a function call */
uint8_t case_11_load_value(uint32_t idx) {
  register uint32_t ridx asm ("edx");
  ridx = idx & (secretarray_size - 1);
  uint8_t to_leak = publicarray[ridx];
  return to_leak;
}
void case_11(uint32_t idx) { // INSECURE
  uint8_t to_leak = case_11_load_value(idx);

  /* Access overwritten secret */
  temp &= publicarray2[to_leak * 512];  
}


/* Same as 10 but result of function is in register */
uint32_t case_12_mask(uint32_t idx) {
  register uint32_t ridx asm ("edx");
  ridx = idx & (secretarray_size - 1);
  return ridx;
}
void case_12(uint32_t idx) { // SECURE
  register uint32_t ridx asm ("edx");
  ridx = case_10_mask(idx);
  
  /* Access overwritten secret */
  temp &= publicarray2[publicarray[ridx] * 512];  
}

/* Same as case 10 but result of function is in register */
uint8_t case_13_load_value(uint32_t idx) {
  register uint32_t ridx asm ("edx");
  ridx = idx & (secretarray_size - 1);
  uint8_t to_leak = publicarray[ridx];
  return to_leak;
}

void case_13(uint32_t idx) {  // SECURE
  register uint8_t to_leak asm ("edx");
  to_leak = case_11_load_value(idx);

  /* Access overwritten secret */
  temp &= publicarray2[to_leak * 512];  
}


int main() {
    return 0;
}
