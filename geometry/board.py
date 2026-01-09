import math

def distance_from_center(x, y, center_x, center_y):
    """
    Returns the distance between a point (x, y)
    and the board center (center_x, center_y).
    """
    dx = x - center_x
    dy = y - center_y
    return math.sqrt(dx * dx + dy * dy)