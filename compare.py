from PIL import Image
import numpy as np


def compare_images(original_path, stego_path):
    """Compare two images and return modified LSB bits + MSE."""

    img1 = np.array(Image.open(original_path).convert("RGB"), dtype=np.int32)
    img2 = np.array(Image.open(stego_path).convert("RGB"), dtype=np.int32)

    if img1.shape != img2.shape:
        raise ValueError("Images must have the same dimensions.")

    diff_lsb = (img1 & 1) != (img2 & 1)
    modified_bits = int(np.sum(diff_lsb))
    total_bits = img1.size

    mse = float(np.mean((img1 - img2) ** 2))

    return {
        "modified_bits": modified_bits,
        "total_bits": total_bits,
        "mse": mse
    }


# -------------------------------------------
# SAME PATH FOR ALL FILES
# -------------------------------------------
original = "C:/Users/Lavar/Downloads/new.png"
encoded = "C:/Users/Lavar/Downloads/encoded.png"

result = compare_images(original, encoded)

print("\n--- IMAGE COMPARISON RESULTS ---")
print("Modified LSB bits:", result["modified_bits"])
print("Total bits:", result["total_bits"])
print("MSE:", result["mse"])
