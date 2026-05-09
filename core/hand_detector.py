# ─────────────────────────────────────────────
#  core/hand_detector.py
#  Wraps MediaPipe 0.10.x Tasks API (HandLandmarker).
# ─────────────────────────────────────────────

import os
import urllib.request
import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

from config.settings import (
    MAX_HANDS,
    DETECTION_CONFIDENCE,
    TRACKING_CONFIDENCE,
    SHOW_LANDMARKS,
)

# ── Auto-download the .task model file if not present ─────────────────────────
MODEL_PATH = "hand_landmarker.task"
MODEL_URL  = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
)

if not os.path.exists(MODEL_PATH):
    print(f"[INFO] Downloading MediaPipe hand model to {MODEL_PATH} ...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("[INFO] Download complete.")

# ── Landmark connections (21 points, same as always) ─────────────────────────
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),         # thumb
    (0,5),(5,6),(6,7),(7,8),         # index
    (0,9),(9,10),(10,11),(11,12),    # middle
    (0,13),(13,14),(14,15),(15,16),  # ring
    (0,17),(17,18),(18,19),(19,20),  # pinky
    (5,9),(9,13),(13,17),            # palm
]


def _draw_landmarks(frame, hand_landmarks_list, frame_w, frame_h):
    """
    Draw landmarks and connections directly with cv2.
    Works with MediaPipe 0.10.x — no mediapipe.framework needed.
    """
    for hand_lms in hand_landmarks_list:
        # Convert normalised coords → pixel coords
        pts = [
            (int(lm.x * frame_w), int(lm.y * frame_h))
            for lm in hand_lms
        ]

        # Draw connections
        for a, b in HAND_CONNECTIONS:
            cv2.line(frame, pts[a], pts[b], (0, 200, 0), 2)

        # Draw landmark dots
        for x, y in pts:
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            cv2.circle(frame, (x, y), 5, (255, 255, 255), 1)


class HandDetector:
    """
    Detects one hand in a BGR frame and returns
    normalised landmarks + annotated frame.
    """

    # Landmark indices — named for readability
    WRIST       = 0
    THUMB_TIP   = 4
    INDEX_MCP   = 5
    INDEX_TIP   = 8
    MIDDLE_MCP  = 9
    MIDDLE_TIP  = 12
    RING_MCP    = 13
    RING_TIP    = 16
    PINKY_MCP   = 17
    PINKY_TIP   = 20

    def __init__(self):
        base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
        options = mp_vision.HandLandmarkerOptions(
            base_options                  = base_options,
            running_mode                  = mp_vision.RunningMode.VIDEO,
            num_hands                     = MAX_HANDS,
            min_hand_detection_confidence = DETECTION_CONFIDENCE,
            min_hand_presence_confidence  = DETECTION_CONFIDENCE,
            min_tracking_confidence       = TRACKING_CONFIDENCE,
        )
        self._detector = mp_vision.HandLandmarker.create_from_options(options)

    def find_hands(self, frame) -> tuple:
        """
        Process a BGR frame.

        Returns
        -------
        frame     : annotated BGR frame
        landmarks : list of 21 dicts {'id', 'x', 'y', 'z'} — empty if no hand
        """
        h, w = frame.shape[:2]
        rgb      = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        timestamp = int(time.time() * 1000)
        result = self._detector.detect_for_video(mp_image, timestamp)

        landmarks = []

        if result.hand_landmarks:
            hand_lms = result.hand_landmarks[0]   # first hand only

            if SHOW_LANDMARKS:
                _draw_landmarks(frame, result.hand_landmarks, w, h)

            for idx, lm in enumerate(hand_lms):
                landmarks.append({
                    "id": idx,
                    "x":  lm.x,
                    "y":  lm.y,
                    "z":  lm.z,
                })

        return frame, landmarks

    def close(self):
        self._detector.close()