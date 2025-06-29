import os, sys
from PIL import Image
import numpy as np
import random

def encrypt_image(in_path, out_path, key):
    img = Image.open(in_path).convert('RGB')
    w, h = img.size
    pixels = list(img.getdata())

    # Shuffle using key
    rng = random.Random(key)
    indices = list(range(len(pixels)))
    rng.shuffle(indices)

    # Reorder + XOR
    encrypted = []
    for idx in indices:
        r, g, b = pixels[idx]
        r ^= key & 0xFF
        g ^= (key >> 8) & 0xFF
        b ^= (key >> 16) & 0xFF
        encrypted.append((r, g, b))

    out = Image.new('RGB', (w, h))
    out.putdata(encrypted)
    out.save(out_path)
    print(f"Encrypted → {out_path}")

def decrypt_image(in_path, out_path, key):
    img = Image.open(in_path).convert('RGB')
    w, h = img.size
    pixels = list(img.getdata())

    # Reverse XOR
    de_xored = []
    for r, g, b in pixels:
        r ^= key & 0xFF
        g ^= (key >> 8) & 0xFF
        b ^= (key >> 16) & 0xFF
        de_xored.append((r, g, b))

    # Unshuffle
    rng = random.Random(key)
    indices = list(range(len(de_xored)))
    rng.shuffle(indices)
    original = [None] * len(de_xored)
    for i, idx in enumerate(indices):
        original[idx] = de_xored[i]

    out = Image.new('RGB', (w, h))
    out.putdata(original)
    out.save(out_path)
    print(f"Decrypted → {out_path}")

if __name__ == '__main__':
    if len(sys.argv) != 5 or sys.argv[1] not in ('enc','dec'):
        print("Usage: python3 tool.py [enc/dec] input.png output.png key_int")
        sys.exit(1)
    cmd, inp, outp, key = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    (encrypt_image if cmd=='enc' else decrypt_image)(inp, outp, key)
