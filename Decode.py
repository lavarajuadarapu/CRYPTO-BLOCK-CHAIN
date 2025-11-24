from PIL import Image
import numpy as np

TERMINATOR = "00000000"


def decode_message(stego_image_path):
    """Extract the hidden message from an LSB-stego image."""

    img = Image.open(stego_image_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8)
    flat = arr.flatten()

    bits = "".join(str(v & 1) for v in flat)

    idx = bits.find(TERMINATOR)
    if idx == -1:
        raise ValueError("No terminator found — message corrupted!")

    bits = bits[:idx]

    message = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        message += chr(int(byte, 2))

    return message


# -------------------------------------------
# SAME PATH FOR ALL FILES
# -------------------------------------------
encoded_path = "C:/Users/Lavar/Downloads/encoded.png"

msg = decode_message(encoded_path)
print("[DECODED MESSAGE]:", msg)
