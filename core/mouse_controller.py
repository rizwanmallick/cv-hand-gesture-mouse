# ─────────────────────────────────────────────
#  core/mouse_controller.py
# ─────────────────────────────────────────────
import pyautogui
import time
import winsound

from core.gesture_classifier import Gesture
from core.utils import SmoothCursor, map_to_screen
from core.volume_controller import VolumeController  # 

from config.settings import (
    FRAME_WIDTH, FRAME_HEIGHT,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    FRAME_REDUCTION,
    SCROLL_AMOUNT,
    CLICK_COOLDOWN,
    SCROLL_COOLDOWN,
)


pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


class MouseController:

    def __init__(self):
        self._smoother = SmoothCursor()
        self._click_cooldown = 0
        self._scroll_cooldown = 0
        self._last_gesture = Gesture.NONE

        # Drag state
        self._dragging = False

        # ── MODE SYSTEM ─────────────────────────
        self._mode = "MOUSE"
        self._volume_controller = VolumeController()

        # ── MODE SWITCH (HOLD) ─────────────────
        self._mode_switch_start = None
        self._mode_switch_triggered = False
        self._MODE_HOLD_TIME = 3  # seconds
        self._last_length = 0
        self._last_volume = 0
        self._media_cooldown = 0

    # ─────────────────────────────────────────────
    #  (for mode switch)
    # ─────────────────────────────────────────────
    def _is_fist(self, landmarks):
             if len(landmarks) != 21:
               return False

    # fingertip indices
             tips = [8, 12, 16, 20]

    # MCP joints
             mcps = [5, 9, 13, 17]

    # If ANY finger is open → not fist
             for tip, mcp in zip(tips, mcps):
               if landmarks[tip]["y"] < landmarks[mcp]["y"]:
                  return False

             return True
    
    def _is_play_pause_gesture(self, landmarks):
        if len(landmarks) != 21:
            return False

        # tips and base joints
        tips = [8, 12, 16, 20]
        mcps = [5, 9, 13, 17]

        fingers = []

        for tip, mcp in zip(tips, mcps):
            if landmarks[tip]["y"] < landmarks[mcp]["y"]:
                fingers.append(1)  # open
            else:
                fingers.append(0)  # closed

        #  only index and middle open
        return fingers == [1, 1, 0, 0]
    
    # ─────────────────────────────────────────────
    # Main update loop
    # ─────────────────────────────────────────────
    def update(self, gesture: Gesture, landmarks: list):

        current_time = time.time()

        # ── MODE SWITCH (HOLD PALM 3 SEC) ─────────────
        if self._is_fist(landmarks):

            if self._mode_switch_start is None:
                self._mode_switch_start = current_time

            elapsed = current_time - self._mode_switch_start

            if elapsed >= self._MODE_HOLD_TIME and not self._mode_switch_triggered:
                self._mode = "VOLUME" if self._mode == "MOUSE" else "MOUSE"
                print(f"[INFO] Mode changed to: {self._mode}")

                winsound.Beep(1000, 200)  # feedback beep

                self._mode_switch_triggered = True
                time.sleep(0.3)

        else:
            self._mode_switch_start = None
            self._mode_switch_triggered = False

        # 🚫 Block everything while holding palm
        if self._is_fist(landmarks):
            return

        # ── VOLUME MODE ─────────────────────────
        if self._mode == "VOLUME":
            
            # ── MEDIA CONTROL ─────────────────────────
            if self._media_cooldown > 0:
                self._media_cooldown -= 1

            if self._is_play_pause_gesture(landmarks):
                if self._media_cooldown == 0:
                    pyautogui.press("playpause")   # works for YouTube, VLC, etc.
                    print("[INFO] Play/Pause toggled")

                    self._media_cooldown = 20  # prevent repeat
                return
            
            if len(landmarks) == 21:

        # 👉 1. Get thumb-index distance (activation)
                x1 = landmarks[4]["x"]
                y1 = landmarks[4]["y"]

                x2 = landmarks[8]["x"]
                y2 = landmarks[8]["y"]

                dx = (x2 - x1) * FRAME_WIDTH
                dy = (y2 - y1) * FRAME_HEIGHT
                pinch_dist = (dx**2 + dy**2) ** 0.5

                # 👉 2. PINCH = ACTIVATE CONTROL
                if pinch_dist < 60:

                    # 👉 Use INDEX FINGER Y for volume
                    lm_y = landmarks[8]["y"]

                    # Convert to screen-like range
                    vol_per = int((1 - lm_y) * 100)   # invert (top = high volume)

                    # Clamp
                    vol_per = max(0, min(100, vol_per))

                    # Smooth small noise
                    if abs(vol_per - self._last_volume) > 2:
                        self._volume_controller.set_volume_by_percent(vol_per)
                        self._last_volume = vol_per

                else:
                    # 👉 RELEASE = LOCK VOLUME
                    pass

            return        

        # ── Cooldowns ─────────────────────────
        if self._click_cooldown > 0:
            self._click_cooldown -= 1
        if self._scroll_cooldown > 0:
            self._scroll_cooldown -= 1

        # ── MOVE + DRAG (cursor always moves) ─────────
        if gesture in (Gesture.MOVE, Gesture.DRAG):

            lm_x = landmarks[8]["x"]
            lm_y = landmarks[8]["y"]

            sx, sy = map_to_screen(
                lm_x, lm_y,
                FRAME_WIDTH, FRAME_HEIGHT,
                SCREEN_WIDTH, SCREEN_HEIGHT,
                FRAME_REDUCTION,
            )

            smooth_x, smooth_y = self._smoother.update(sx, sy)
            pyautogui.moveTo(int(smooth_x), int(smooth_y))

        # ── DRAG (button control only) ─────────
        if gesture == Gesture.DRAG:
            if not self._dragging:
                pyautogui.mouseDown()
                self._dragging = True
        else:
            if self._dragging:
                pyautogui.mouseUp()
                self._dragging = False

        # ── RIGHT CLICK ────────────────────────
        if gesture == Gesture.RIGHT_CLICK:
            if self._click_cooldown == 0:
                pyautogui.rightClick()
                self._click_cooldown = CLICK_COOLDOWN

        # ── LEFT CLICK ─────────────────────────
        elif gesture == Gesture.LEFT_CLICK:
            if self._click_cooldown == 0:
                pyautogui.click()
                self._click_cooldown = CLICK_COOLDOWN

        # ── SCROLL UP ──────────────────────────
        elif gesture == Gesture.SCROLL_UP:
            if self._scroll_cooldown == 0:
                pyautogui.scroll(SCROLL_AMOUNT)
                self._scroll_cooldown = SCROLL_COOLDOWN

        # ── SCROLL DOWN ────────────────────────
        elif gesture == Gesture.SCROLL_DOWN:
            if self._scroll_cooldown == 0:
                pyautogui.scroll(-SCROLL_AMOUNT)
                self._scroll_cooldown = SCROLL_COOLDOWN

        # ── SCREENSHOT ─────────────────────────
        elif gesture == Gesture.SCREENSHOT:
            if self._click_cooldown == 0:
                time.sleep(0.3)
                filename = f"screenshot_{int(time.time())}.png"
                pyautogui.screenshot(filename)
                winsound.Beep(1000, 200)
                print(f"[INFO] Screenshot saved: {filename}")
                self._click_cooldown = CLICK_COOLDOWN

        # ── RESET ────────────────────────────
        if gesture not in (Gesture.MOVE, Gesture.DRAG):
            if self._last_gesture in (Gesture.MOVE, Gesture.DRAG):
                self._smoother.reset()

        self._last_gesture = gesture