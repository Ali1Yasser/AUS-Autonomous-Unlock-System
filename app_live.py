#These imports connect the main file to everything else.
#config, ui, Detectors, LockState, and check_conditions are the pieces it uses.
import time

import cv2

import config
import ui
from detectors import Detectors
from lock_logic import LockState, check_conditions


def main():
    detectors = Detectors()
    state = LockState()
    cap = cv2.VideoCapture(0)
    start = time.time()

    try:
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break

            detectors.send(frame, int((time.time() - start) * 1000))
            face_res, hand_res = detectors.latest()

            conditions_ok, hint = check_conditions(face_res, hand_res)
            now = time.time()
            state.update(conditions_ok, now)

            display = cv2.flip(frame, 1)          # mirror only for display
            ui.draw(display, state, conditions_ok, hint, now)
            cv2.imshow(config.WINDOW_NAME, display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("r"):
                state.reset()
    finally:
        cap.release()
        cv2.destroyAllWindows()
        detectors.close()


if __name__ == "__main__":
    main()