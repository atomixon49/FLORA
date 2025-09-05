#include "flora/aes_gcm.hpp"
#include <iostream>
#include <random>

using namespace std;
using namespace flora;

int main(){
	vector<uint8_t> key(32, 0x11);
	vector<uint8_t> nonce(12, 0x22);
	string msg = "Hola FLORA desde C++";
	vector<uint8_t> pt(msg.begin(), msg.end());
	vector<uint8_t> ad = { 'A','B','C' };

	auto ct = AesGcm::encrypt(key, nonce, pt, ad);
	auto dec = AesGcm::decrypt(key, ct.nonce, ct.ciphertext, ct.tag, ad);
	cout << string(dec.begin(), dec.end()) << endl;
	return 0;
}




