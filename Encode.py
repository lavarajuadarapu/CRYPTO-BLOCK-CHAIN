from PIL import Image
import numpy as np

TERMINATOR = "00000000"


def encode_message(input_image_path, message, output_image_path):
    """Embed a text message inside an image using LSB steganography."""

    img = Image.open(input_image_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8)
    h, w, ch = arr.shape

    bits = "".join(f"{ord(c):08b}" for c in message) + TERMINATOR

    capacity = h * w * 3
    if len(bits) > capacity:
        raise ValueError("Message too large for this image!")

    flat = arr.flatten()
    for i, bit in enumerate(bits):
        flat[i] = (flat[i] & 0xFE) | int(bit)

    new_arr = flat.reshape((h, w, ch))
    out_img = Image.fromarray(new_arr)

    out_img.save(output_image_path)
    print("[OK] Message encoded into", output_image_path)


# -------------------------------------------
# SAME PATH FOR ALL FILES
# -------------------------------------------
input_path = "C:/Users/Lavar/Downloads/new.png"
output_path = "C:/Users/Lavar/Downloads/encoded.png"
secret_message = "Hello from Steganography!"

encode_message(input_path, secret_message, output_path)
