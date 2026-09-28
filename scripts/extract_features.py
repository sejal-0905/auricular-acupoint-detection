"""
Once YOLO gives you (x, y) locations for the 8 points on a photo, this script
crops a small patch around each point and calculates simple numbers describing
that patch: average color, redness, and texture roughness.

Usage:
    python extract_features.py --image path/to/photo.jpg --points_json path/to/points.json
"""

import cv2
import numpy as np
import argparse
import json


def extract_patch_features(image, x, y, patch_size=15):
    h, w = image.shape[:2]
    x, y = int(x), int(y)
    x1, x2 = max(0, x - patch_size), min(w, x + patch_size)
    y1, y2 = max(0, y - patch_size), min(h, y + patch_size)
    patch = image[y1:y2, x1:x2]
    if patch.size == 0:
        return None

    patch_rgb = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB)
    patch_hsv = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)
    patch_gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)

    return {
        "avg_red": float(np.mean(patch_rgb[:, :, 0])),
        "avg_green": float(np.mean(patch_rgb[:, :, 1])),
        "avg_blue": float(np.mean(patch_rgb[:, :, 2])),
        "avg_hue": float(np.mean(patch_hsv[:, :, 0])),
        "avg_saturation": float(np.mean(patch_hsv[:, :, 1])),
        "avg_brightness": float(np.mean(patch_hsv[:, :, 2])),
        "texture_roughness": float(np.std(patch_gray)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--points_json", required=True,
                         help="JSON file with {point_name: [x, y]} - from your YOLO predictions")
    args = parser.parse_args()

    image = cv2.imread(args.image)
    if image is None:
        print(f"Could not load image: {args.image}")
        return

    with open(args.points_json) as f:
        points = json.load(f)

    all_features = {}
    for point_name, (x, y) in points.items():
        feats = extract_patch_features(image, x, y)
        all_features[point_name] = feats
        print(f"{point_name}: {feats}")

    out_path = args.image.rsplit(".", 1)[0] + "_features.json"
    with open(out_path, "w") as f:
        json.dump(all_features, f, indent=2)
    print(f"\nSaved features to {out_path}")


if __name__ == "__main__":
    main()
