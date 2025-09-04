# 🌸 FLORA - API REST (FastAPI)
# Endpoints: /encrypt, /decrypt, /status

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any, Dict
import os

from .flora_crypto import FloraCryptoSystem

API_KEY = os.getenv("FLORA_API_KEY", "flora-dev-key")

app = FastAPI(title="FLORA API", description="Cifrado híbrido con autodestrucción caótica", version="0.1.0-alpha")

# CORS (permite probar desde clientes web locales)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)


def api_key_auth(x_api_key: Optional[str] = Header(default=None), authorization: Optional[str] = Header(default=None)):
	"""Autenticación simple por API key.
	Acepta: X-API-Key: <key> o Authorization: Bearer <key>
	"""
	key = x_api_key
	if not key and authorization and authorization.lower().startswith("bearer "):
		key = authorization.split(" ", 1)[1].strip()
	if key != API_KEY:
		raise HTTPException(status_code=401, detail="Unauthorized")
	return True


class EncryptRequest(BaseModel):
	password: str
	message: str  # texto plano (se codifica utf-8)
	session_id: Optional[str] = "api_default_session"
	associated_data_hex: Optional[str] = None
	use_kyber: bool = True


class DecryptRequest(BaseModel):
	password: str
	bundle: Dict[str, Any]


@app.post("/encrypt", dependencies=[Depends(api_key_auth)])
async def encrypt(req: EncryptRequest):
	try:
		flora = FloraCryptoSystem(use_kyber=req.use_kyber)
		master_salt = os.urandom(32)
		master_key, _ = flora.generate_master_key(req.password, master_salt)
		ad = bytes.fromhex(req.associated_data_hex) if req.associated_data_hex else None
		enc = flora.encrypt_message(req.message.encode("utf-8"), master_key, req.session_id, ad)
		enc['master_salt'] = master_salt.hex()
		return enc
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))


@app.post("/decrypt", dependencies=[Depends(api_key_auth)])
async def decrypt(req: DecryptRequest):
	try:
		flora = FloraCryptoSystem()
		master_salt_hex = req.bundle.get('master_salt')
		if not master_salt_hex:
			raise HTTPException(status_code=400, detail="Bundle inválido: falta master_salt")
		master_salt = bytes.fromhex(master_salt_hex)
		master_key, _ = flora.generate_master_key(req.password, master_salt)
		pt = flora.decrypt_message(req.bundle, master_key)
		return {"plaintext": pt.decode("utf-8", errors="replace")}
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))


@app.get("/status", dependencies=[Depends(api_key_auth)])
async def status():
	flora = FloraCryptoSystem()
	return flora.get_system_status()
