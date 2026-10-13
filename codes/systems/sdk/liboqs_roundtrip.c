/* Author-written liboqs API integration check; no secret bytes are logged.
   Build against fixed liboqs 0.15.0, see run_liboqs.py. */
#include <oqs/oqs.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static int check(const char *name) {
    OQS_KEM *kem=OQS_KEM_new(name);
    if (!kem) return 1;
    uint8_t *pk=OQS_MEM_malloc(kem->length_public_key);
    uint8_t *sk=OQS_MEM_malloc(kem->length_secret_key);
    uint8_t *ct=OQS_MEM_malloc(kem->length_ciphertext);
    uint8_t *ss1=OQS_MEM_malloc(kem->length_shared_secret);
    uint8_t *ss2=OQS_MEM_malloc(kem->length_shared_secret);
    if (!pk||!sk||!ct||!ss1||!ss2) return 2;
    int ok=0, rejected=0;
    for (int j=0;j<10;j++) {
        if (OQS_KEM_keypair(kem,pk,sk)!=OQS_SUCCESS ||
            OQS_KEM_encaps(kem,ct,ss1,pk)!=OQS_SUCCESS ||
            OQS_KEM_decaps(kem,ss2,ct,sk)!=OQS_SUCCESS) return 3;
        if (memcmp(ss1,ss2,kem->length_shared_secret)!=0) return 4;
        ok++;
        ct[0]^=1;
        /* ML-KEM implicit rejection returns a different secret, not an error oracle. */
        if (OQS_KEM_decaps(kem,ss2,ct,sk)!=OQS_SUCCESS) return 5;
        if (memcmp(ss1,ss2,kem->length_shared_secret)==0) return 6;
        rejected++;
    }
    printf("{\"algorithm\":\"%s\",\"public_key_bytes\":%zu,\"secret_key_bytes\":%zu,\"ciphertext_bytes\":%zu,\"shared_secret_bytes\":%zu,\"valid_roundtrips\":%d,\"tampered_different_secrets\":%d}",
        name,kem->length_public_key,kem->length_secret_key,kem->length_ciphertext,kem->length_shared_secret,ok,rejected);
    OQS_MEM_insecure_free(pk);OQS_MEM_insecure_free(ct);
    OQS_MEM_secure_free(sk,kem->length_secret_key);OQS_MEM_secure_free(ss1,kem->length_shared_secret);OQS_MEM_secure_free(ss2,kem->length_shared_secret);
    OQS_KEM_free(kem);return 0;
}
int main(void) {
    OQS_init(); printf("[");
    const char *names[]={"ML-KEM-512","ML-KEM-768","ML-KEM-1024"};
    for (int i=0;i<3;i++) { if(i)printf(",");int result=check(names[i]);if(result){fprintf(stderr,"check failed %d\n",result);return result;} }
    printf("]\n");OQS_destroy();return 0;
}
