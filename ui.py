import cv2

import config


def _banner(frame, text, color):
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (w, 70), color, -1)
    size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.6, 4)[0]
    cv2.putText(frame, text, ((w - size[0]) // 2, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.6, config.WHITE, 4)


def _text(frame, text, y, color=config.WHITE):
    cv2.putText(frame, text, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)


def draw(frame, state, conditions_ok, hint, now):
    """Draws the whole overlay on a (already mirrored) frame."""
    if state.unlocked:
        _banner(frame, "UNLOCKED", config.GREEN)
        return

    _banner(frame, "LOCKED", config.RED)
    _text(frame, hint, 100, config.YELLOW if conditions_ok else config.WHITE)

    progress = state.hold_progress(now)
    if progress is not None:
        cv2.rectangle(frame, (20, 120), (320, 145), config.GRAY, 2)
        cv2.rectangle(frame, (20, 120), (20 + int(300 * progress), 145),
                      config.YELLOW, -1)