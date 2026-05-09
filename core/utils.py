# ─────────────────────────────────────────────
#  core/utils.py
#  Cursor smoothing + misc helpers
# ─────────────────────────────────────────────

from collections import deque
from config.settings import SMOOTHING_FACTOR


class SmoothCursor:
    """
    Simple moving-average filter for (x, y) cursor positions.
    Keeps a rolling window of the last N positions and returns
    their mean — removes jitter without adding much lag.

    Usage
    -----
        smoother = SmoothCursor()
        smooth_x, smooth_y = smoother.update(raw_x, raw_y)
    """

    def __init__(self, factor: int = SMOOTHING_FACTOR):
        self._xs = deque(maxlen=factor)
        self._ys = deque(maxlen=factor)

    def update(self, x: float, y: float) -> tuple[float, float]:
        self._xs.append(x)
        self._ys.append(y)
        return (
            sum(self._xs) / len(self._xs),
            sum(self._ys) / len(self._ys),
        )

    def reset(self):
        self._xs.clear()
        self._ys.clear()


def map_to_screen(
    lm_x: float,
    lm_y: float,
    frame_w: int,
    frame_h: int,
    screen_w: int,
    screen_h: int,
    reduction: int,
) -> tuple[int, int]:
    """
    Map a normalised landmark position (0-1) inside the
    reduced active frame region to full screen coordinates.

    Parameters
    ----------
    lm_x, lm_y  : normalised landmark x, y  (0.0 – 1.0)
    frame_w/h    : camera frame pixel size
    screen_w/h   : OS screen pixel size
    reduction    : pixels to ignore on each side of the frame
                   (creates a comfortable movement dead-zone at the edges)

    Returns
    -------
    (screen_x, screen_y) clamped to screen bounds
    """
    import numpy as np

    # Convert norm → pixel inside frame
    px = lm_x * frame_w
    py = lm_y * frame_h

    # Map the reduced active zone onto the full screen
    sx = np.interp(px, [reduction, frame_w - reduction], [0, screen_w])
    sy = np.interp(py, [reduction, frame_h - reduction], [0, screen_h])

    # Clamp to screen edges
    sx = int(max(0, min(screen_w - 1, sx)))
    sy = int(max(0, min(screen_h - 1, sy)))

    return sx, sy


def draw_text(
    frame,
    text: str,
    pos: tuple[int, int],
    color=(0, 255, 0),
    scale: float = 0.8,
    thickness: int = 2,
):
    """Convenience wrapper around cv2.putText."""
    import cv2
    cv2.putText(
        frame, text, pos,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale, color, thickness,
        cv2.LINE_AA,
    )