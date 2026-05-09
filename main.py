# ─────────────────────────────────────────────
#  main.py  —  entry point
#  Run:  python main.py
#  Stop: press  Q  in the preview window, or
#        move mouse to top-left corner of screen
# ─────────────────────────────────────────────

import time
import cv2

from core.hand_detector      import HandDetector
from core.gesture_classifier import GestureClassifier, Gesture
from core.mouse_controller   import MouseController
from core.utils              import draw_text
from config.settings import (
    CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT,
    SHOW_FPS, SHOW_GESTURE_LABEL,
)

# ── Gesture label colours for the overlay ─────────────────────────────────────
GESTURE_COLORS = {
    Gesture.NONE        : (180, 180, 180),
    Gesture.MOVE        : (0,   255,   0),
    Gesture.LEFT_CLICK  : (0,   200, 255),
    Gesture.RIGHT_CLICK : (255, 120,   0),
    Gesture.SCROLL_UP   : (255, 255,   0),
    Gesture.SCROLL_DOWN : (200,   0, 255),
}



def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        print("[ERROR] Cannot open camera. Check CAMERA_INDEX in config/settings.py")
        return

    detector    = HandDetector()
    classifier  = GestureClassifier()
    controller  = MouseController()

    cv2.namedWindow("Gesture Mouse  |  Q to quit", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Gesture Mouse  |  Q to quit", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    prev_time = time.time()

    print("[INFO] Gesture Mouse started.  Press Q to quit.")
    print("[INFO] Move mouse to TOP-LEFT corner of screen to emergency-stop.")
    frame_count = 0
    while True:
        frame_count += 1
        # if frame_count % 2 != 0:
        #   continue
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Empty frame — retrying…")
            continue

        # Flip horizontally so it acts like a mirror
        frame = cv2.flip(frame, 1)

        # ── Detection ─────────────────────────────────────────────────────
        frame, landmarks = detector.find_hands(frame)

        # ── Classification ────────────────────────────────────────────────
        gesture = classifier.classify(landmarks)

        # ── Control ───────────────────────────────────────────────────────
        controller.update(gesture, landmarks)

        if controller._mode == "VOLUME":
            vol_per = controller._volume_controller.current_vol_per

            # 🔷 Volume Bar UI
            bar_top = 150
            bar_bottom = 400

            # map % → bar position
            bar_pos = int(bar_bottom - (vol_per / 100) * (bar_bottom - bar_top))

            # outer box
            cv2.rectangle(frame, (50, bar_top), (85, bar_bottom), (255, 0, 0), 2)

            # filled bar
            cv2.rectangle(frame, (50, bar_pos), (85, bar_bottom), (255, 0, 0), cv2.FILLED)

            # percentage text
            draw_text(frame, f"{vol_per}%", (40, 430), (255, 0, 0), scale=1.0, thickness=2)

        # ── Overlay: gesture label ─────────────────────────────────────────
        if SHOW_GESTURE_LABEL:
            label = gesture.name.replace("_", " ")
            color = GESTURE_COLORS.get(gesture, (255, 255, 255))
            draw_text(frame, label, (10, 40), color=color, scale=1.0, thickness=2)

        draw_text(frame, f"MODE: {controller._mode}", (10, 80), (255, 0, 255))
        

        # ── Overlay: FPS ───────────────────────────────────────────────────
        if SHOW_FPS:
            now       = time.time()
            fps       = 1.0 / max(now - prev_time, 1e-9)
            prev_time = now
            draw_text(frame, f"FPS: {fps:.0f}", (10, FRAME_HEIGHT - 15),
                      color=(200, 200, 200), scale=0.6, thickness=1)

        # ── Overlay: active zone rectangle ─────────────────────────────────
        from config.settings import FRAME_REDUCTION as R
        cv2.rectangle(frame,
                      (R, R),
                      (FRAME_WIDTH - R, FRAME_HEIGHT - R),
                      (50, 50, 200), 1)

        # ── Show ───────────────────────────────────────────────────────────
        cv2.imshow("Gesture Mouse  |  Q to quit", frame)
        cv2.setWindowProperty("Gesture Mouse  |  Q to quit", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # ── Cleanup ───────────────────────────────────────────────────────────
    detector.close()
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Gesture Mouse stopped.")


if __name__ == "__main__":
    main()