#include "flora/c_api.h"
#include "flora/aes_gcm.hpp"
#include <stdexcept>
#include <vector>

using namespace flora;

extern "C" {

static int to_code(const std::exception&){ return -1; }

int flora_aes_gcm_encrypt(
	const uint8_t* key, size_t key_len,
	const uint8_t* nonce, size_t nonce_len,
	const uint8_t* ad, size_t ad_len,
	const uint8_t* plaintext, size_t pt_len,
	uint8_t* ciphertext, size_t* ct_len,
	uint8_t* tag, size_t tag_len){
	try{
		std::vector<uint8_t> k(key, key+key_len);
		std::vector<uint8_t> n(nonce, nonce+nonce_len);
		std::vector<uint8_t> a;
		if(ad && ad_len) a.assign(ad, ad+ad_len);
		std::vector<uint8_t> pt(plaintext, plaintext+pt_len);
		auto out = AesGcm::encrypt(k, n, pt, a);
		if(out.tag.size()!=tag_len) return -2;
		if(*ct_len < out.ciphertext.size()) return -3;
		std::copy(out.ciphertext.begin(), out.ciphertext.end(), ciphertext);
		*ct_len = out.ciphertext.size();
		std::copy(out.tag.begin(), out.tag.end(), tag);
		return 0;
	}catch(const std::exception& e){
		return to_code(e);
	}
}

int flora_aes_gcm_decrypt(
	const uint8_t* key, size_t key_len,
	const uint8_t* nonce, size_t nonce_len,
	const uint8_t* ad, size_t ad_len,
	const uint8_t* ciphertext, size_t ct_len,
	const uint8_t* tag, size_t tag_len,
	uint8_t* plaintext, size_t* pt_len){
	try{
		std::vector<uint8_t> k(key, key+key_len);
		std::vector<uint8_t> n(nonce, nonce+nonce_len);
		std::vector<uint8_t> a;
		if(ad && ad_len) a.assign(ad, ad+ad_len);
		std::vector<uint8_t> ct(ciphertext, ciphertext+ct_len);
		std::vector<uint8_t> tg(tag, tag+tag_len);
		auto out = AesGcm::decrypt(k, n, ct, tg, a);
		if(*pt_len < out.size()) return -3;
		std::copy(out.begin(), out.end(), plaintext);
		*pt_len = out.size();
		return 0;
	}catch(const std::exception& e){
		return to_code(e);
	}
}

}
