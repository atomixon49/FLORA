use aes_gcm::aead::{Aead, KeyInit, OsRng};
use aes_gcm::{Aes256Gcm, Nonce}; // Or Aes128Gcm, Aes192Gcm

pub struct AesGcmResult {
	pub nonce: Vec<u8>,
	pub ciphertext: Vec<u8>,
}

pub fn aes_gcm_encrypt(key: &[u8], plaintext: &[u8], associated_data: &[u8]) -> Result<AesGcmResult, String> {
	let cipher = match key.len() {
		32 => Aes256Gcm::new_from_slice(key).map_err(|e| e.to_string())?,
		_ => return Err("key must be 32 bytes for Aes256Gcm".into()),
	};
	let nonce_bytes: [u8; 12] = rand::random();
	let nonce = Nonce::from_slice(&nonce_bytes);
	let ct = cipher
		.encrypt(nonce, aes_gcm::aead::Payload { msg: plaintext, aad: associated_data })
		.map_err(|e| e.to_string())?;
	Ok(AesGcmResult { nonce: nonce_bytes.to_vec(), ciphertext: ct })
}

pub fn aes_gcm_decrypt(key: &[u8], nonce: &[u8], ciphertext: &[u8], associated_data: &[u8]) -> Result<Vec<u8>, String> {
	let cipher = match key.len() {
		32 => Aes256Gcm::new_from_slice(key).map_err(|e| e.to_string())?,
		_ => return Err("key must be 32 bytes for Aes256Gcm".into()),
	};
	if nonce.len() != 12 { return Err("nonce must be 12 bytes".into()); }
	let nonce = Nonce::from_slice(nonce);
	let pt = cipher
		.decrypt(nonce, aes_gcm::aead::Payload { msg: ciphertext, aad: associated_data })
		.map_err(|e| e.to_string())?;
	Ok(pt)
}
