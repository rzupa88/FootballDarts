import os
import cv2
import numpy as np
from geometry.board import Dartboard

# =========================
# Paths
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "assets", "test_images", "board.jpeg")

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

# IMPORTANT:
# Set this to False if the coordinates below were taken
# from the ORIGINAL image (not a resized display window)
POINTS_ARE_FROM_RESIZED_DISPLAY = True
MAX_DISPLAY_SIZE = 900

# Outer double edge calibration points (your values)
TOP    = (291, 197)
RIGHT  = (505, 414)
BOTTOM = (291, 623)
LEFT   = (78,  414)

h0, w0 = image.shape[:2]
scale = min(MAX_DISPLAY_SIZE / w0, MAX_DISPLAY_SIZE / h0, 1.0)

def unscale_point(pt):
    if not POINTS_ARE_FROM_RESIZED_DISPLAY or scale == 1.0:
        return pt
    x, y = pt
    return (int(round(x / scale)), int(round(y / scale)))

top    = unscale_point(TOP)
right  = unscale_point(RIGHT)
bottom = unscale_point(BOTTOM)
left   = unscale_point(LEFT)

src = np.array([top, right, bottom, left], dtype=np.float32)

cx = OUTPUT_SIZE // 2
cy = OUTPUT_SIZE // 2
dst = np.array([
    (cx, 0),
    (OUTPUT_SIZE, cy),
    (cx, OUTPUT_SIZE),
    (0, cy)
], dtype=np.float32)

H = cv2.getPerspectiveTransform(src, dst)
image = cv2.warpPerspective(image, H, (OUTPUT_SIZE, OUTPUT_SIZE))

# =========================
# Board model (warped space)
# =========================
h, w = image.shape[:2]
center_x, center_y = w // 2, h // 2
radius = min(center_x, center_y)

board = Dartboard(center_x, center_y, radius)

# =========================
# Mouse handling
# =========================
def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        ring = board.ring_for_point(x, y)
        print(f"Clicked at ({x}, {y}) → {ring}")

# =========================
# Draw overlays
# =========================
overlay = image.copy()

# Center dot (blue)
cv2.circle(overlay, (center_x, center_y), 6, (255, 0, 0), -1)

# Ring overlays
for r in [
    board.inner_bull,
    board.outer_bull,
    board.triple_inner,
    board.triple_outer,
    board.double_inner,
    board.double_outer
]:
    cv2.circle(overlay, (center_x, center_y), int(r), (255, 255, 255), 1)

# =========================
# Display
# =========================
window_name = "DartCam - Warped Board (800x800)"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.imshow(window_name, overlay)
cv2.setMouseCallback(window_name, on_mouse_click)

cv2.waitKey(0)
cv2.destroyAllWindows()
