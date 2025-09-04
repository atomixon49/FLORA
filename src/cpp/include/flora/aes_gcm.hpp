#pragma once

#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

namespace flora {

struct AesGcmCiphertext {
	std::vector<uint8_t> nonce;     // 12 bytes
	std::vector<uint8_t> ciphertext;
	std::vector<uint8_t> tag;       // 16 bytes
};

class AesGcm {
public:
	// key: 16/24/32 bytes; nonce 12 bytes; ad (opcional)
	static AesGcmCiphertext encrypt(const std::vector<uint8_t>& key,
									 const std::vector<uint8_t>& nonce,
									 const std::vector<uint8_t>& plaintext,
									 const std::vector<uint8_t>& associated_data = {});

	static std::vector<uint8_t> decrypt(const std::vector<uint8_t>& key,
									 const std::vector<uint8_t>& nonce,
									 const std::vector<uint8_t>& ciphertext,
									 const std::vector<uint8_t>& tag,
									 const std::vector<uint8_t>& associated_data = {});
};

} // namespace flora



