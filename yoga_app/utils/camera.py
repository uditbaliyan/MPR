# yoga_app/utils/camera.py
import cv2
from threading import Lock
import mediapipe as mp
from yoga_app.config import Config
from yoga_app.utils.pose_detection import PoseDetector

class Camera:
    def __init__(self):
        self.lock = Lock()
        self.detector = PoseDetector()

    def generate_frames(self):
        with self.lock:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("Error: Could not open camera")
                return
            
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
            
            with self.detector.mp_pose.Pose(
                min_detection_confidence=Config.MIN_DETECTION_CONFIDENCE,
                min_tracking_confidence=Config.MIN_TRACKING_CONFIDENCE,
                model_complexity=Config.MODEL_COMPLEXITY
            ) as pose:
                while True:
                    success, frame = cap.read()
                    if not success:
                        break

                    frame = cv2.flip(frame, 1)
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    rgb_frame.flags.writeable = False
                    results = pose.process(rgb_frame)
                    rgb_frame.flags.writeable = True

                    if results.pose_landmarks:
                        self.detector.mp_drawing.draw_landmarks(
                            frame,
                            results.pose_landmarks,
                            self.detector.mp_pose.POSE_CONNECTIONS,
                            self.detector.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                            self.detector.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                        )

                        detected_poses = [
                            pose_name for pose_name, check_func in self.detector.get_pose_checks().items()
                            if check_func(results.pose_landmarks.landmark)
                        ]

                        pose_text = "Detected: " + ", ".join(detected_poses) if detected_poses else "No pose detected"
                        cv2.putText(
                            frame,
                            pose_text,
                            (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0) if detected_poses else (0, 0, 255),
                            2
                        )

                    try:
                        ret, buffer = cv2.imencode('.jpg', frame)
                        if not ret:
                            continue
                        frame_bytes = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                    except Exception as e:
                        print(f"Error encoding frame: {e}")
                        continue

            cap.release()