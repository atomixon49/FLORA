#include "flora/aes_gcm.hpp"
#include <openssl/evp.h>
#include <stdexcept>

using namespace std;

namespace flora {

static void ensure_ok(int ok, const char* msg){
	if(!ok) throw runtime_error(msg);
}

AesGcmCiphertext AesGcm::encrypt(const vector<uint8_t>& key,
								  const vector<uint8_t>& nonce,
								  const vector<uint8_t>& plaintext,
								  const vector<uint8_t>& associated_data){
	if(nonce.size()!=12) throw runtime_error("AES-GCM nonce must be 12 bytes");
	const EVP_CIPHER* cipher = nullptr;
	switch(key.size()){
		case 16: cipher = EVP_aes_128_gcm(); break;
		case 24: cipher = EVP_aes_192_gcm(); break;
		case 32: cipher = EVP_aes_256_gcm(); break;
		default: throw runtime_error("AES-GCM key must be 16, 24 or 32 bytes");
	}
	EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
	if(!ctx) throw runtime_error("EVP_CIPHER_CTX_new failed");
	AesGcmCiphertext out;
	out.nonce = nonce;
	int len=0;
	ensure_ok(EVP_EncryptInit_ex(ctx, cipher, nullptr, nullptr, nullptr)==1, "EncryptInit failed");
	ensure_ok(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, (int)nonce.size(), nullptr)==1, "set ivlen failed");
	ensure_ok(EVP_EncryptInit_ex(ctx, nullptr, nullptr, key.data(), nonce.data())==1, "key/iv init failed");
	if(!associated_data.empty()){
		ensure_ok(EVP_EncryptUpdate(ctx, nullptr, &len, associated_data.data(), (int)associated_data.size())==1, "aad failed");
	}
	out.ciphertext.resize(plaintext.size());
	ensure_ok(EVP_EncryptUpdate(ctx, out.ciphertext.data(), &len, plaintext.data(), (int)plaintext.size())==1, "enc update failed");
	int ciphertext_len = len;
	ensure_ok(EVP_EncryptFinal_ex(ctx, out.ciphertext.data()+ciphertext_len, &len)==1, "enc final failed");
	ciphertext_len += len;
	out.ciphertext.resize(ciphertext_len);
	out.tag.resize(16);
	ensure_ok(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, 16, out.tag.data())==1, "get tag failed");
	EVP_CIPHER_CTX_free(ctx);
	return out;
}

vector<uint8_t> AesGcm::decrypt(const vector<uint8_t>& key,
								 const vector<uint8_t>& nonce,
								 const vector<uint8_t>& ciphertext,
								 const vector<uint8_t>& tag,
								 const vector<uint8_t>& associated_data){
	if(nonce.size()!=12) throw runtime_error("AES-GCM nonce must be 12 bytes");
	if(tag.size()!=16) throw runtime_error("AES-GCM tag must be 16 bytes");
	const EVP_CIPHER* cipher = nullptr;
	switch(key.size()){
		case 16: cipher = EVP_aes_128_gcm(); break;
		case 24: cipher = EVP_aes_192_gcm(); break;
		case 32: cipher = EVP_aes_256_gcm(); break;
		default: throw runtime_error("AES-GCM key must be 16, 24 or 32 bytes");
	}
	EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
	if(!ctx) throw runtime_error("EVP_CIPHER_CTX_new failed");
	int len=0, p_len=0;
	ensure_ok(EVP_DecryptInit_ex(ctx, cipher, nullptr, nullptr, nullptr)==1, "DecryptInit failed");
	ensure_ok(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, (int)nonce.size(), nullptr)==1, "set ivlen failed");
	ensure_ok(EVP_DecryptInit_ex(ctx, nullptr, nullptr, key.data(), nonce.data())==1, "key/iv init failed");
	if(!associated_data.empty()){
		ensure_ok(EVP_DecryptUpdate(ctx, nullptr, &len, associated_data.data(), (int)associated_data.size())==1, "aad failed");
	}
	vector<uint8_t> plaintext(ciphertext.size());
	ensure_ok(EVP_DecryptUpdate(ctx, plaintext.data(), &len, ciphertext.data(), (int)ciphertext.size())==1, "dec update failed");
	p_len = len;
	ensure_ok(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG, (int)tag.size(), (void*)tag.data())==1, "set tag failed");
	int ret = EVP_DecryptFinal_ex(ctx, plaintext.data()+p_len, &len);
	EVP_CIPHER_CTX_free(ctx);
	if(ret<=0) throw runtime_error("GCM tag verification failed");
	p_len += len;
	plaintext.resize(p_len);
	return plaintext;
}

} // namespace flora




