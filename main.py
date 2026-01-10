import os
import cv2
import numpy as np
from geometry.board import Dartboard

# =========================
# Paths
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "assets", "test_images", "board.jpeg")

OUT_DIR = os.path.join(BASE_DIR, "assets", "test_images", "out")
os.makedirs(OUT_DIR, exist_ok=True)

# =========================
# Load image
# =========================
image = cv2.imread(IMAGE_PATH)
if image is None:
    raise FileNotFoundError(f"Could not load image at {IMAGE_PATH}")

# =========================
# Perspective warp (locked)
# =========================
OUTPUT_SIZE = 800

# Set this to False if your calibration points were taken on the ORIGINAL (full-res) image
POINTS_ARE_FROM_RESIZED_DISPLAY = True
MAX_DISPLAY_SIZE = 900

# Outer double edge calibration points (your values)
TOP = (291, 197)
RIGHT = (505, 414)
BOTTOM = (291, 623)
LEFT = (78, 414)

h0, w0 = image.shape[:2]
scale = min(MAX_DISPLAY_SIZE / w0, MAX_DISPLAY_SIZE / h0, 1.0)


def unscale_point(pt):
    if (not POINTS_ARE_FROM_RESIZED_DISPLAY) or scale == 1.0:
        return pt
    x, y = pt
    return (int(round(x / scale)), int(round(y / scale)))


top = unscale_point(TOP)
right = unscale_point(RIGHT)
bottom = unscale_point(BOTTOM)
left = unscale_point(LEFT)

src = np.array([top, right, bottom, left], dtype=np.float32)

cx = OUTPUT_SIZE // 2
cy = OUTPUT_SIZE // 2
dst = np.array(
    [
        (cx, 0),
        (OUTPUT_SIZE, cy),
        (cx, OUTPUT_SIZE),
        (0, cy),
    ],
    dtype=np.float32,
)

H = cv2.getPerspectiveTransform(src, dst)
warped = cv2.warpPerspective(image, H, (OUTPUT_SIZE, OUTPUT_SIZE))

# Save warped image (so you can preview it in VS Code)
warped_path = os.path.join(OUT_DIR, f"warped_{OUTPUT_SIZE}.png")
cv2.imwrite(warped_path, warped)
print("✅ Saved:", warped_path)

# =========================
# Board model (warped space)
# =========================
h, w = warped.shape[:2]
center_x, center_y = w // 2, h // 2
radius = min(center_x, center_y)

board = Dartboard(center_x, center_y, radius)

# =========================
# Draw overlays (rings + wedge lines)
# =========================
overlay = warped.copy()

# Center dot (blue)
cv2.circle(overlay, (center_x, center_y), 6, (255, 0, 0), -1)

# Rings
for r in (
    board.inner_bull,
    board.outer_bull,
    board.triple_inner,
    board.triple_outer,
    board.double_inner,
    board.double_outer,
):
    cv2.circle(overlay, (center_x, center_y), int(r), (255, 255, 255), 1)

# Wedge boundary lines (20)
for i in range(20):
    theta = (2 * np.pi / 20) * i + board.angle_offset_radians
    x2 = int(center_x + radius * np.sin(theta))
    y2 = int(center_y - radius * np.cos(theta))
    cv2.line(overlay, (center_x, center_y), (x2, y2), (255, 255, 255), 1)

overlay_path = os.path.join(OUT_DIR, f"overlay_{OUTPUT_SIZE}.png")
cv2.imwrite(overlay_path, overlay)
print("✅ Saved:", overlay_path)

# =========================
# Quick non-GUI test points (prints expected codes)
# =========================
tests = [
    (
        "TOP wedge, single",
        (center_x, int(center_y - (board.triple_inner - 5))),
    ),
    (
        "RIGHT wedge, single",
        (int(center_x + (board.triple_inner - 5)), center_y),
    ),
    (
        "BOTTOM wedge, single",
        (center_x, int(center_y + (board.triple_inner - 5))),
    ),
    (
        "LEFT wedge, single",
        (int(center_x - (board.triple_inner - 5)), center_y),
    ),
]

print("\n=== Angle→Number sanity checks ===")
for name, (x, y) in tests:
    res = board.dart_result_for_point(x, y)
    print(f"{name:22s} at ({x},{y}) -> {res['code']} ({res['points']} pts)")
print("==================================\n")

print("Open the saved PNGs in VS Code:")
print(" -", warped_path)
print(" -", overlay_path)