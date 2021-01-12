#include "ssl3_cbc_remove_padding.c"

#define LEN 200

/* Here, we have to concretize the length because we cannot work with a symbolic pointer */
/* Solution: malloc stub ? */

int main(){
  unsigned char data[LEN];      /* Private */
  unsigned int length = LEN;    /* Public */
  unsigned int block_size;      /* Public */
  unsigned int mac_size;        /* Public */
  unsigned int rec_type;        /* Public */
  unsigned char input[200];     /* Public */

  // s is actually not used in the function
  SSL s_obj;
  const SSL *s = &s_obj;

  // only the length and data fields are used in the function
  SSL3_RECORD rec_obj = { length, data, rec_type, NULL };

  return ssl3_cbc_remove_padding(s,&rec_obj,block_size,mac_size);

}

