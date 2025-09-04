#pragma once

#include <cstddef>
#include <cstdint>

#if defined(_WIN32)
	#define FLORA_API __declspec(dllexport)
#else
	#define FLORA_API __attribute__((visibility("default")))
#endif

extern "C" {

// Devuelve 0 en éxito, !=0 en error
// key_len: 16/24/32, nonce_len: 12, tag_len (in/out) debe ser 16
FLORA_API int flora_aes_gcm_encrypt(
	const uint8_t* key, size_t key_len,
	const uint8_t* nonce, size_t nonce_len,
	const uint8_t* ad, size_t ad_len,
	const uint8_t* plaintext, size_t pt_len,
	uint8_t* ciphertext, size_t* ct_len,
	uint8_t* tag, size_t tag_len);

FLORA_API int flora_aes_gcm_decrypt(
	const uint8_t* key, size_t key_len,
	const uint8_t* nonce, size_t nonce_len,
	const uint8_t* ad, size_t ad_len,
	const uint8_t* ciphertext, size_t ct_len,
	const uint8_t* tag, size_t tag_len,
	uint8_t* plaintext, size_t* pt_len);

}
