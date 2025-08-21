#!/usr/bin/env python3
"""
USB Steganography Toolkit — Layered
- Always encrypts (prompts if -p is omitted)
- Layer 1: AES-256 ZIP (pyzipper) compress + encrypt
- Layer 2: Fernet encryption (PBKDF2-HMAC-SHA256 -> AES + HMAC)
- Layer 3: PNG LSB steganography (1 LSB per RGB channel)
"""
import argparse, sys, struct, base64, os, io, getpass
from typing import Tuple, Optional
from PIL import Image
import pyzipper
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

MAGIC = b"STG1"
FLAG_ENCRYPTED = 0x01
FLAG_ZIPPED    = 0x02
HEADER_STRUCT = "!4sB I"             # magic (4s), flags (B), length (uint32)
HEADER_SIZE   = struct.calcsize(HEADER_STRUCT)
SALT_SIZE     = 16
ZIP_ENTRY_NAME = "payload.bin"

def _derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=200_000)
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))

def _bytes_to_bits(data: bytes):
    for byte in data:
        for i in range(7, -1, -1):
            yield (byte >> i) & 1

def _bits_to_bytes(bits):
    out, cur, count = bytearray(), 0, 0
    for b in bits:
        cur = (cur << 1) | (b & 1)
        count += 1
        if count == 8:
            out.append(cur); cur = 0; count = 0
    return bytes(out)

def _img_to_channels(img: Image.Image):
    if img.mode not in ("RGB","RGBA"):
        img = img.convert("RGB")
    if img.mode == "RGBA":
        img = img.convert("RGB")
    pixels = list(img.getdata())
    flat = []
    for r,g,b in pixels:
        flat.extend([r,g,b])
    return img, flat

def _channels_to_img(channels, size: Tuple[int,int]) -> Image.Image:
    it = iter(channels)
    pixels = list(zip(it, it, it))
    out = Image.new("RGB", size)
    out.putdata(pixels)
    return out

def capacity_bytes(img: Image.Image) -> int:
    w, h = img.size
    return (w * h * 3) // 8

def _zip_encrypt(data: bytes, passphrase: str) -> bytes:
    """AES-256 zip (compress+encrypt) using pyzipper."""
    import io, pyzipper
    buf = io.BytesIO()
    with pyzipper.AESZipFile(buf, mode='w', compression=pyzipper.ZIP_DEFLATED) as zf:
        zf.setpassword(passphrase.encode('utf-8'))
        zf.setencryption(pyzipper.WZ_AES, nbits=256)
        zf.writestr(ZIP_ENTRY_NAME, data)
    return buf.getvalue()

def _zip_decrypt(zbytes: bytes, passphrase: str) -> bytes:
    buf = io.BytesIO(zbytes)
    with pyzipper.AESZipFile(buf, 'r') as zf:
        zf.setpassword(passphrase.encode('utf-8'))
        return zf.read(ZIP_ENTRY_NAME)

def _ensure_passphrase(p: Optional[str], prompt: str) -> str:
    if p:
        return p
    pw = getpass.getpass(prompt)
    if not pw:
        raise RuntimeError("Empty passphrase not allowed.")
    return pw

def embed(input_png: str, output_png: str, data: bytes, passphrase: Optional[str] = None):
    passphrase = _ensure_passphrase(passphrase, "Enter passphrase to encrypt: ")

    # Layer 1: AES-256 ZIP
    zipped = _zip_encrypt(data, passphrase)

    # Layer 2: Fernet
    salt = os.urandom(SALT_SIZE)
    key  = _derive_key(passphrase, salt)
    f    = Fernet(key)
    encrypted = f.encrypt(zipped)

    flags = FLAG_ENCRYPTED | FLAG_ZIPPED
    header = struct.pack(HEADER_STRUCT, MAGIC, flags, len(encrypted))
    payload = header + salt + encrypted

    # Layer 3: PNG LSB
    img = Image.open(input_png)
    img, chans = _img_to_channels(img)
    cap = capacity_bytes(img)
    if len(payload) > cap:
        raise ValueError(f"Payload ({len(payload)}) exceeds image capacity ({cap}). Use a larger image.")
    bits = list(_bytes_to_bits(payload))
    out = chans[:]
    for i, bit in enumerate(bits):
        out[i] = (out[i] & 0xFE) | bit
    out_img = _channels_to_img(out, img.size)
    out_img.save(output_png, "PNG")

def extract(stego_png: str, passphrase: Optional[str] = None) -> bytes:
    passphrase = _ensure_passphrase(passphrase, "Enter passphrase to decrypt: ")

    img = Image.open(stego_png)
    img, chans = _img_to_channels(img)

    header_bits = (ch & 1 for ch in chans[:HEADER_SIZE*8])
    header_bytes = _bits_to_bytes(header_bits)
    magic, flags, length = struct.unpack(HEADER_STRUCT, header_bytes)
    if magic != MAGIC:
        raise ValueError("Not a valid stego image.")

    off = HEADER_SIZE*8
    salt_bits = (ch & 1 for ch in chans[off : off + SALT_SIZE*8])
    salt = _bits_to_bytes(salt_bits)
    off += SALT_SIZE*8

    enc_bits = (ch & 1 for ch in chans[off : off + length*8])
    encrypted = _bits_to_bytes(enc_bits)

    key = _derive_key(passphrase, salt)
    f   = Fernet(key)
    zipped = f.decrypt(encrypted)

    if flags & FLAG_ZIPPED:
        return _zip_decrypt(zipped, passphrase)
    return zipped

def main():
    ap = argparse.ArgumentParser(description="Layered Stego (AES-ZIP + Fernet + LSB)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_e = sub.add_parser("embed", help="Embed a message/file into a PNG (always encrypted)")
    ap_e.add_argument("-i","--input", required=True, help="Cover image (PNG)")
    ap_e.add_argument("-o","--output", required=True, help="Output stego image (PNG)")
    gx = ap_e.add_mutually_exclusive_group(required=True)
    gx.add_argument("-m","--message", help="Plain text message to hide")
    gx.add_argument("-f","--file", help="Path to file to hide")
    ap_e.add_argument("-p","--passphrase", help="Passphrase (if omitted, you will be prompted)")
    ap_e.add_argument("--force", action="store_true", help="Overwrite output if exists")

    ap_x = sub.add_parser("extract", help="Extract hidden payload from a PNG")
    ap_x.add_argument("-i","--input", required=True, help="Stego image (PNG)")
    ap_x.add_argument("-o","--output", help="Where to write extracted bytes (if omitted, prints text if UTF-8)")
    ap_x.add_argument("-p","--passphrase", help="Passphrase (if omitted, you will be prompted)")

    args = ap.parse_args()

    if args.cmd == "embed":
        if not args.input.lower().endswith(".png") or not args.output.lower().endswith(".png"):
            print("Use PNG files for reliable results.", file=sys.stderr)
        if os.path.exists(args.output) and not args.force:
            print(f"Refusing to overwrite {args.output}. Use --force to overwrite.", file=sys.stderr)
            sys.exit(1)
        if args.message is not None:
            payload = args.message.encode("utf-8")
        else:
            with open(args.file, "rb") as f:
                payload = f.read()
        try:
            embed(args.input, args.output, payload, args.passphrase)
        except Exception as e:
            print(f"Embed failed: {e}", file=sys.stderr); sys.exit(2)
        print(f"✅ Embedded payload into {args.output}")

    elif args.cmd == "extract":
        try:
            data = extract(args.input, args.passphrase)
        except Exception as e:
            print(f"Extract failed: {e}", file=sys.stderr); sys.exit(3)
        if args.output:
            with open(args.output, "wb") as f:
                f.write(data)
            print(f"✅ Wrote {len(data)} bytes to {args.output}")
        else:
            try:
                print(data.decode("utf-8"))
            except UnicodeDecodeError:
                print(f"[binary payload] {len(data)} bytes")
                print(data[:64].hex() + ("..." if len(data) > 64 else ""))

if __name__ == "__main__":
    main()
