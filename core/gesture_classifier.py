# core/gesture_classifier.py

import math
from enum import Enum, auto

from config.settings import CLICK_THRESHOLD, SCROLL_THRESHOLD

class Gesture(Enum):
    SCREENSHOT = auto()
    NONE = auto()
    MOVE = auto()
    LEFT_CLICK = auto()
    RIGHT_CLICK = auto()
    SCROLL_UP = auto()    # index + middle fully straight up
    SCROLL_DOWN = auto()  # index + middle half-curled (tips close to PIP joints)
    DRAG = auto()

# Landmark indices
WRIST = 0
THUMB_TIP = 4
INDEX_MCP = 5
INDEX_PIP = 6      # middle joint of index
INDEX_DIP = 7      # upper joint of index
INDEX_TIP = 8    
MIDDLE_MCP = 9     
MIDDLE_PIP = 10    # middle joint of middle finger
MIDDLE_DIP = 11    # upper joint of middle finger
MIDDLE_TIP = 12    # tip of middle finger (used for scroll detection)
RING_MCP = 13
RING_TIP = 16
PINKY_MCP = 17
PINKY_TIP = 20


def _dist(lm, a, b):
    dx = (lm[a]["x"] - lm[b]["x"]) * 1000
    dy = (lm[a]["y"] - lm[b]["y"]) * 1000
    return math.hypot(dx, dy)


def _finger_open(lm, tip, mcp):
    return lm[tip]["y"] < lm[mcp]["y"]


def _thumb_open(lm):
    return _dist(lm, THUMB_TIP, INDEX_MCP) > 60


def _finger_fully_extended(lm, tip, pip, mcp):
    """Tip above PIP above MCP - finger fully straight."""
    return lm[tip]["y"] < lm[pip]["y"] and lm[pip]["y"] < lm[mcp]["y"]


def _finger_half_curled(lm, tip, pip, dip, mcp):
    """
    Half-curl detection:
    - Finger is open enough to be above MCP (not fully closed)
    - But tip has dropped close to or below the DIP joint
      meaning the top two segments are curling inward
    - PIP is still above MCP (base of finger still raised)
    """
    base_raised = lm[pip]["y"] < lm[mcp]["y"]       # finger not fully closed
    tip_curled = lm[tip]["y"] >= lm[dip]["y"] - 0.01  # tip dropped to/below DIP level
    return base_raised and tip_curled


class GestureClassifier:
    def classify(self, landmarks) -> Gesture:
        if len(landmarks) != 21:
            return Gesture.NONE

        lm = landmarks

        thumb_open = _thumb_open(lm)
        index_open = _finger_open(lm, INDEX_TIP, INDEX_MCP)
        middle_open = _finger_open(lm, MIDDLE_TIP, MIDDLE_MCP)
        ring_open = _finger_open(lm, RING_TIP, RING_MCP)
        pinky_open = _finger_open(lm, PINKY_TIP, PINKY_MCP)

        index_extended = _finger_fully_extended(lm, INDEX_TIP, INDEX_PIP, INDEX_MCP)
        middle_extended = _finger_fully_extended(lm, MIDDLE_TIP, MIDDLE_PIP, MIDDLE_MCP)

        index_halfcurl = _finger_half_curled(lm, INDEX_TIP, INDEX_PIP, INDEX_DIP, INDEX_MCP)
        middle_halfcurl = _finger_half_curled(lm, MIDDLE_TIP, MIDDLE_PIP, MIDDLE_DIP, MIDDLE_MCP)
        ring_halfcurl = _finger_half_curled(lm, RING_TIP, RING_MCP, RING_TIP, RING_MCP)
        pinky_halfcurl = _finger_half_curled(lm, PINKY_TIP, PINKY_MCP, PINKY_TIP, PINKY_MCP)

        thumb_index_dist = _dist(lm, THUMB_TIP, INDEX_TIP)
        thumb_middle_dist = _dist(lm, THUMB_TIP, MIDDLE_TIP)
        thumb_ring_dist = _dist(lm, THUMB_TIP, RING_TIP)
        thumb_pinky_dist = _dist(lm, THUMB_TIP, PINKY_TIP)

        touching_ring = thumb_ring_dist < CLICK_THRESHOLD
        touching_index = thumb_index_dist < CLICK_THRESHOLD
        touching_middle = thumb_middle_dist < CLICK_THRESHOLD

  
        # ── DRAG (Thumb + Ring) ─────────────────────────────
        if touching_ring and not touching_middle and not touching_index and pinky_open:
            return Gesture.DRAG
        
        if touching_index and not touching_middle:
            return Gesture.RIGHT_CLICK

        if touching_middle and not touching_index:
            return Gesture.LEFT_CLICK

        if index_extended and middle_extended and not ring_open and not pinky_open:
            return Gesture.SCROLL_UP

        if index_halfcurl and middle_halfcurl and not ring_open and not pinky_open:
            return Gesture.SCROLL_DOWN

        if thumb_open and pinky_open and not index_open and not middle_open and not ring_open:
            return Gesture.SCREENSHOT
        
        
        if index_open and thumb_open and not middle_open and not ring_open and not pinky_open:
            return Gesture.MOVE

        return Gesture.NONE
