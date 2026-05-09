# ─────────────────────────────────────────────
#  config/settings.py  —  all tunable values
# ─────────────────────────────────────────────

import pyautogui

# ── Camera ────────────────────────────────────
CAMERA_INDEX        = 0          # 0 = default webcam
FRAME_WIDTH         = 640
FRAME_HEIGHT        = 480

# ── MediaPipe ─────────────────────────────────
MAX_HANDS           = 1          # track only one hand
DETECTION_CONFIDENCE  = 0.8
TRACKING_CONFIDENCE   = 0.8

# ── Screen ────────────────────────────────────
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# ── Cursor movement ───────────────────────────
# The hand doesn't need to reach the full frame edge.
# We reduce the active region so small hand movements
# cover the whole screen comfortably.
FRAME_REDUCTION     = 30         # pixels to crop on each edge
SMOOTHING_FACTOR    = 3        # higher = smoother but more laggy (3–9)


# ── Gesture thresholds ────────────────────────
# Euclidean distance (in normalised 0-1 coords × 1000)
# below which two fingertips are considered "touching"
CLICK_THRESHOLD     = 40         # for left / right click detection
SCROLL_THRESHOLD    = 30         # for scroll gesture detection

# ── Scroll speed ─────────────────────────────
SCROLL_AMOUNT       = 25        # lines per recognised scroll gesture

# ── Gesture cooldown ─────────────────────────
# Minimum frames between two consecutive click / scroll events.
# Prevents accidental double-fires.
CLICK_COOLDOWN      = 15         # frames
SCROLL_COOLDOWN     = 2         # frames

# ── Debug overlay ────────────────────────────
SHOW_FPS            = True
SHOW_LANDMARKS      = True
SHOW_GESTURE_LABEL  = True