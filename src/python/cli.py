# 🌸 FLORA - CLI
# Comandos: encrypt, decrypt, status

import sys
import json
import os
import click
from pathlib import Path

from .flora_crypto import FloraCryptoSystem

DEFAULT_SESSION = "cli_default_session"

EXAMPLES = """
Examples:
  flora --help
  flora status
  flora encrypt --no-kyber --session demo --ad 414243 msg.txt msg.enc.json
  flora decrypt msg.enc.json msg.dec.txt
  
  # En PowerShell, varios comandos en una sola línea
  flora --help ; flora status
"""

@click.group(context_settings={"help_option_names": ["-h", "--help"]},
		   help="CLI de FLORA: cifrado híbrido con autodestrucción caótica.",
		   epilog=EXAMPLES)
def main():
	"""CLI de FLORA: cifrado híbrido con autodestrucción caótica."""
	pass


def _read_bytes(path: Path) -> bytes:
	return path.read_bytes()


def _write_bytes(path: Path, data: bytes) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_bytes(data)


@main.command(help="Encripta INFILE -> OUTFILE (JSON).", epilog="Ejemplo: flora encrypt --no-kyber --session demo --ad 414243 msg.txt msg.enc.json")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=False, help="Contraseña para derivar la clave maestra")
@click.option("--use-kyber/--no-kyber", default=True, help="Intentar usar Kyber KEM para clave de sesión")
@click.option("--session", default=DEFAULT_SESSION, help="ID de sesión")
@click.option("--ad", type=str, default=None, help="Datos asociados (hex opcional)")
@click.argument("infile", type=click.Path(exists=True, dir_okay=False))
@click.argument("outfile", type=click.Path(dir_okay=False))
def encrypt(password: str, use_kyber: bool, session: str, ad: str, infile: str, outfile: str):
	"""Encripta INFILE -> OUTFILE (hex JSON)."""
	flora = FloraCryptoSystem(use_kyber=use_kyber)
	# Generar un salt explícito para poder reconstruir la master_key en decrypt
	master_salt = os.urandom(32)
	master_key, _ = flora.generate_master_key(password, master_salt)
	plaintext = _read_bytes(Path(infile))
	assoc = bytes.fromhex(ad) if ad else None
	enc = flora.encrypt_message(plaintext, master_key, session, assoc)
	# Anexar master_salt al paquete para poder derivar la misma master_key en decrypt
	enc['master_salt'] = master_salt.hex()
	Path(outfile).write_text(json.dumps(enc, ensure_ascii=False, indent=2))
	click.echo("✅ Encriptado OK → " + outfile)


@main.command(help="Desencripta INFILE (JSON) -> OUTFILE (bytes).", epilog="Ejemplo: flora decrypt msg.enc.json msg.dec.txt")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=False, help="Contraseña para derivar la clave maestra")
@click.argument("infile", type=click.Path(exists=True, dir_okay=False))
@click.argument("outfile", type=click.Path(dir_okay=False))
def decrypt(password: str, infile: str, outfile: str):
	"""Desencripta INFILE (JSON) -> OUTFILE (bytes)."""
	flora = FloraCryptoSystem()
	enc = json.loads(Path(infile).read_text())
	# Recuperar master_salt desde el paquete
	master_salt_hex = enc.get('master_salt')
	if not master_salt_hex:
		click.echo("❌ Paquete inválido: falta master_salt", err=True)
		sys.exit(1)
	master_salt = bytes.fromhex(master_salt_hex)
	master_key, _ = flora.generate_master_key(password, master_salt)
	pt = flora.decrypt_message(enc, master_key)
	_write_bytes(Path(outfile), pt)
	click.echo("✅ Desencriptado OK → " + outfile)


@main.command(help="Muestra estado de sistema (demo).", epilog="Ejemplo: flora status")
def status():
	"""Muestra estado de sistema (demo)."""
	flora = FloraCryptoSystem()
	info = flora.get_system_status()
	click.echo(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
	main()
