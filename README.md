**1. Project Overview**

This project implements LSB (Least Significant Bit) steganography for hiding and extracting secret text messages inside images.
The goal is to modify pixel values in a way that is visually undetectable but still encodes binary information.

You will:

Encode a secret message into an image

Decode a hidden message from a modified image

Compare the original and encoded images

Analyse the statistical impact (MSE, modified bits, heatmap)

Understand limitations of LSB steganography


**2. Principle of LSB Steganography**

An RGB image stores each pixel as three bytes:

R (8 bits) | G (8 bits) | B (8 bits)


The least significant bit (LSB) of each colour channel contributes very little to the visual appearance.
Changing only the last bit (e.g., 11001100 → 11001101) is almost invisible to the human eye.

To hide text:

Convert message to 8-bit ASCII binary

Append terminator 00000000

Replace each pixel's R/G/B LSB with one bit of the message

Continue until all bits are stored

To extract the message:

Read pixel LSBs in the same order

Group bits into bytes

Stop when 00000000 is found

Convert bytes back to text

**3. Encoding – How to Use encode_message()**

Python Code (Encode.py)
from PIL import Image

def message_to_bits(message):
    return ''.join(format(ord(c), '08b') for c in message) + "00000000"

def encode_message(input_image_path, output_image_path, message):
    img = Image.open(input_image_path).convert("RGB")
    width, height = img.size
    pixels = img.load()

    bits = message_to_bits(message)
    capacity = width * height * 3

    if len(bits) > capacity:
        raise ValueError("Message too large for this image.")

    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index >= len(bits):
                img.save(output_image_path)
                print("Encoding complete:", output_image_path)
                return

            r, g, b = pixels[x, y]

            if bit_index < len(bits):
                r = (r & ~1) | int(bits[bit_index]); bit_index += 1
            if bit_index < len(bits):
                g = (g & ~1) | int(bits[bit_index]); bit_index += 1
            if bit_index < len(bits):
                b = (b & ~1) | int(bits[bit_index]); bit_index += 1

            pixels[x, y] = (r, g, b)

    img.save(output_image_path)
    print("Encoding complete:", output_image_path)

if __name__ == "__main__":
    encode_message(
        r"C:\PATH\TO\original.png",
        r"C:\PATH\TO\encoded.png",
        "Hello Bob! This is the secret message."
    )
    Run the encoder:
python Encode.py


This produces a new file:

encoded.png


containing the hidden message.

**4. Decoding – How to Use decode_message()**

Python Code (Decode.py)
from PIL import Image

def decode_message(image_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    pixels = img.load()

    bits = ""

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    message = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if byte == "00000000":
            return message
        message += chr(int(byte, 2))

    return message

if __name__ == "__main__":
    msg = decode_message(r"C:\PATH\TO\encoded.png")
    print("Extracted message:", msg)

Run the decoder:
python Decode.py

**5. Image Analysis Tools**

Comparison & MSE
import numpy as np
from PIL import Image

def analyse_image(original, stego):
    orig = np.array(Image.open(original).convert("RGB"))
    mod  = np.array(Image.open(stego).convert("RGB"))

    diff = (orig != mod)
    modified_bits = diff.sum()

    mse = ((orig - mod) ** 2).mean()

    print("Modified bits:", modified_bits)
    print("MSE:", mse)

    return diff, mse

    Heatmap of Modified Pixels
import matplotlib.pyplot as plt

def show_heatmap(diff):
    heat = diff.sum(axis=2)
    plt.imshow(heat, cmap="hot")
    plt.title("Heatmap of Modified Pixels")
    plt.colorbar()
    plt.show()

Run analysis:
diff, mse = analyse_image("original.png", "encoded.png")
show_heatmap(diff)

**6. Limitations of LSB Steganography**

Steganography does not encrypt data.
Anyone who extracts the LSBs can read the message.

Attackers can detect hidden data using:

statistical analysis

chi-square LSB tests

visual/noise analysis

Lossy formats like JPEG break LSB encoding because compression alters pixel values.
Always use PNG, BMP, or TIFF.

**7. Deliverables**

This project includes:

Encode.py (encoding script)

Decode.py (decoding script)

Original image

Encoded image

Extracted message

Analysis script

README report (this file)
