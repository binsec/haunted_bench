#include "../../../__libsym__/sym.h"
#include "tea.c"

unsigned long key[4];     // The secret
unsigned long data[2];    // The message to encrypt/decrypt
unsigned long out[2];     // The output buffer
// Everything is high

int main() {
  
  encipher(data, out, key);

  return 0;
}
