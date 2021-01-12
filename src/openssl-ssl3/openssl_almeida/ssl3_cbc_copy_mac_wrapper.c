#include "../__libsym__/sym.h"
#include "ssl3_cbc_copy_mac.c"

#define ORIG_LEN 384 // > 64 + 255 + 1

int main() {
  unsigned char out[EVP_MAX_MD_SIZE]; // private
  unsigned char data[ORIG_LEN];       // private
  unsigned int length;                // private
  unsigned int md_size;               // public
  unsigned int orig_len = ORIG_LEN;   // public

  // pointer _values_ are public, but not the contents
  HIGH_INPUT(EVP_MAX_MD_SIZE)(out);
  HIGH_INPUT(ORIG_LEN)(data);
 
  // these lengths are all public
  LOW_INPUT(4)(&length);
  LOW_INPUT(4)(&md_size);
  LOW_INPUT(4)(&orig_len);

  // only the length and data fields are used in the function
  SSL3_RECORD rec_obj = { length, data, 0, NULL };

  /*   rec->orig_len >= md_size
   *   md_size <= EVP_MAX_MD_SIZE */
  ssl3_cbc_copy_mac(out,&rec_obj,md_size,orig_len);
  return 0;
}

