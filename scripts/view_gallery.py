"""Sequential viewer for visualization PNGs.

Usage (Windows-friendly):
    uv run scripts/view_gallery.py

It will open each PNG under visualizations/ using matplotlib. Close the
window (click the red X or press Alt+F4) to advance to the next image.
"""

import glob
import os
import sys

import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def find_images():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    viz_dir = os.path.join(repo_root, "visualizations")
    patterns = ["*.png", "*.jpg", "*.jpeg"]
    images = []
    for pattern in patterns:
        images.extend(glob.glob(os.path.join(viz_dir, pattern)))
    return sorted(images)


def main():
    images = find_images()
    if not images:
        print("[view_gallery] No images found under visualizations/.")
        sys.exit(0)

    print("[view_gallery] Found", len(images), "images. Close each window to advance.")

    for img_path in images:
        img = mpimg.imread(img_path)
        plt.imshow(img)
        plt.axis("off")
        plt.title(os.path.basename(img_path))
        plt.show()

    print("[view_gallery] Done.")


if __name__ == "__main__":
    main() 