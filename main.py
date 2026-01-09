import cv2
from geometry.board import distance_from_center

# Load dartboard image
image = cv2.imread("assets/test_images/board.jpg")
if image is None:
    raise FileNotFoundError("Could not load assets/test_images/board.jpg")

# Get image center
h, w = image.shape[:2]
center_x, center_y = w // 2, h // 2

def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        dist = distance_from_center(x, y, center_x, center_y)
        print(f"Clicked at ({x}, {y}) | Distance from center: {int(dist)}")

# Draw center marker
cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)

# Show window and listen for clicks
window_name = "DartCam - Geometry Test"
cv2.imshow(window_name, image)
cv2.setMouseCallback(window_name, on_mouse_click)

cv2.waitKey(0)
cv2.destroyAllWindows()
