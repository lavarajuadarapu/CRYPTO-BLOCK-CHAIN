from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def generate_heatmap(original_path, stego_path, output_path):
    """Generate an amplified LSB modification heatmap."""

    # Load images
    img1 = np.array(Image.open(original_path).convert("RGB"), dtype=np.int32)
    img2 = np.array(Image.open(stego_path).convert("RGB"), dtype=np.int32)

    # Compare LSB bits
    diff = (img1 & 1) != (img2 & 1)
    heatmap = np.sum(diff, axis=2)  # values 0–3

    # Amplify small LSB changes so they are visible
    enhanced = heatmap * 50

    # Draw heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(enhanced, cmap="hot", interpolation="nearest")
    plt.title("Enhanced Heatmap (Amplified LSB Differences)")
    plt.colorbar(label="Amplified Modified Channels")
    plt.axis("off")
    plt.tight_layout()

    # Save output
    plt.savefig(output_path, dpi=200)
    plt.close()

    print("[OK] Heatmap saved at:", output_path)


# -----------------------------------------------------
# SAME PATH FOR ALL FILES - Do NOT change these paths
# -----------------------------------------------------
generate_heatmap(
    "C:/Users/Lavar/Downloads/new.png",
    "C:/Users/Lavar/Downloads/encoded.png",
    "C:/Users/Lavar/Downloads/heatmap.png"
)
