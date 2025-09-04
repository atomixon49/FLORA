use flora_rs::{aes_gcm_encrypt, aes_gcm_decrypt};

fn main() {
	let key = vec![0x11u8; 32];
	let ad = b"ABC".to_vec();
	let msg = b"Hola FLORA desde Rust".to_vec();
	let enc = aes_gcm_encrypt(&key, &msg, &ad).expect("encrypt");
	let dec = aes_gcm_decrypt(&key, &enc.nonce, &enc.ciphertext, &ad).expect("decrypt");
	println!("{}", String::from_utf8_lossy(&dec));
}
