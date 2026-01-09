import math
import json
import os


class Dartboard:
    def __init__(self, center_x, center_y, radius):
        self.cx = center_x
        self.cy = center_y
        self.radius = radius

        # Load ring calibration config
        config_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config",
            "rings.json"
        )

        with open(config_path, "r") as f:
            cfg = json.load(f)

        R = radius  # outer double edge radius in pixels

        self.inner_bull = (cfg["inner_bull_pct"] / 100.0) * R
        self.outer_bull = (cfg["outer_bull_pct"] / 100.0) * R

        self.triple_inner = (cfg["triple_inner_pct"] / 100.0) * R
        self.triple_outer = (cfg["triple_outer_pct"] / 100.0) * R

        self.double_inner = (cfg["double_inner_pct"] / 100.0) * R
        self.double_outer = (cfg["double_outer_pct"] / 100.0) * R

    def distance_from_center(self, x, y):
        dx = x - self.cx
        dy = y - self.cy
        return math.sqrt(dx * dx + dy * dy)

    def ring_for_point(self, x, y):
        d = self.distance_from_center(x, y)

        if d <= self.inner_bull:
            return "INNER BULL"
        elif d <= self.outer_bull:
            return "OUTER BULL"
        elif self.triple_inner <= d <= self.triple_outer:
            return "TRIPLE"
        elif self.double_inner <= d <= self.double_outer:
            return "DOUBLE"
        elif d <= self.radius:
            return "SINGLE"
        else:
            return "MISS"
