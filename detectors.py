import threading

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

import config


class Detectors:
    """Owns both models and keeps the latest result from each."""

    def __init__(self):
        self._lock = threading.Lock()
        self._face_result = None
        self._hand_result = None

        base = mp_python.BaseOptions
        mode = vision.RunningMode.LIVE_STREAM

        self._face = vision.FaceLandmarker.create_from_options(
            vision.FaceLandmarkerOptions(
                base_options=base(model_asset_path=config.FACE_MODEL),
                running_mode=mode,
                num_faces=2,                      # 2 so we can reject multiple faces
                output_face_blendshapes=True,
                result_callback=self._on_face,
            )
        )
        self._gesture = vision.GestureRecognizer.create_from_options(
            vision.GestureRecognizerOptions(
                base_options=base(model_asset_path=config.GESTURE_MODEL),
                running_mode=mode,
                num_hands=2,
                result_callback=self._on_hands,
            )
        )

    # callbacks run on background threads
    def _on_face(self, result, image, timestamp_ms):
        with self._lock:
            self._face_result = result

    def _on_hands(self, result, image, timestamp_ms):
        with self._lock:
            self._hand_result = result

    def send(self, bgr_frame, timestamp_ms):
        import cv2
        rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        self._face.detect_async(mp_image, timestamp_ms)
        self._gesture.recognize_async(mp_image, timestamp_ms)

    def latest(self):
        with self._lock:
            return self._face_result, self._hand_result

    def close(self):
        self._face.close()
        self._gesture.close()