from pathlib import Path

BASE_DIR = Path(__file__).parent

# Models (paths work no matter where you run the script from)
FACE_MODEL = str(BASE_DIR / "Models" / "face_landmarker.task")
GESTURE_MODEL = str(BASE_DIR / "Models" / "gesture_recognizer.task")

# Unlock rules
REQUIRED_GESTURE = "Victory"   # Thumb_Up, Open_Palm, Closed_Fist, Pointing_Up...
REQUIRED_HAND = "Right"           # None = either hand, or "Left" / "Right"
HOLD_SECONDS = 2.0
UNLOCKED_DURATION = 5.0        # seconds before it relocks

# Thresholds
WINK_CLOSED = 0.3              # blink score above this = eye closed
WINK_OPEN = 0.3                # blink score below this = eye open
GESTURE_MIN_SCORE = 0.6
WINK_EYE = "eyeBlinkLeft"      # swap these two if left/right is reversed
OPEN_EYE = "eyeBlinkRight"

# Colors (BGR)
RED = (0, 0, 255)
GREEN = (0, 200, 0)
YELLOW = (0, 255, 255)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)

WINDOW_NAME = "AUS - Autonomous Unlock System"