import config


def check_conditions(face_res, hand_res):
    """Returns (conditions_ok, hint_text)."""
    if face_res is None:
        return False, "Starting..."

    n_faces = len(face_res.face_landmarks)
    if n_faces == 0:
        return False, "No face detected"
    if n_faces > 1:
        return False, "Multiple faces detected"


    blend = {c.category_name: c.score for c in face_res.face_blendshapes[0]}
    winking = (blend[config.WINK_EYE] > config.WINK_CLOSED
               and blend[config.OPEN_EYE] < config.WINK_OPEN)

    gesture_ok = False
    if hand_res is not None:
        matching = []
        for gestures, handed in zip(hand_res.gestures, hand_res.handedness):
            g = gestures[0]
            if g.category_name != config.REQUIRED_GESTURE:
                continue
            if g.score < config.GESTURE_MIN_SCORE:
                continue
            if config.REQUIRED_HAND and handed[0].category_name != config.REQUIRED_HAND:
                continue
            matching.append(g)
        gesture_ok = len(matching) == 1    # the other hand can show anything

    hint = f"Wink: {'OK' if winking else 'no'} | Gesture: {'OK' if gesture_ok else 'no'}"
    l = blend[config.WINK_EYE]
    r = blend[config.OPEN_EYE]
    hint = (f"Wink eye: {l:.2f} | Open eye: {r:.2f} | "
            f"Wink: {'OK' if winking else 'no'} | Gesture: {'OK' if gesture_ok else 'no'}")
    return (winking and gesture_ok), hint


class LockState:
    """Tracks hold timer and locked/unlocked status."""

    def __init__(self):
        self.hold_start = None
        self.unlocked_at = None

    @property
    def unlocked(self):
        return self.unlocked_at is not None

    def hold_progress(self, now):
        if self.hold_start is None:
            return None
        return min((now - self.hold_start) / config.HOLD_SECONDS, 1.0)

    def update(self, conditions_ok, now):
        if self.unlocked:
            if now - self.unlocked_at >= config.UNLOCKED_DURATION:
                self.reset()                      # auto relock
            return

        if not conditions_ok:
            self.hold_start = None
            return

        if self.hold_start is None:
            self.hold_start = now
        if now - self.hold_start >= config.HOLD_SECONDS:
            self.unlocked_at = now
            self.hold_start = None

    def reset(self):
        self.hold_start = None
        self.unlocked_at = None