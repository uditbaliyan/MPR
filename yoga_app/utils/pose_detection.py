# yoga_app/utils/pose_detection.py
import mediapipe as mp
import numpy as np
import math

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils

    def calculate_angle(self, a, b, c):
        if not all([a, b, c]):
            return None
        
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle

    def is_tadasana(self,landmarks):
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        def aligned_vertical(left, right, tolerance=0.1):
            return abs(left.x - right.x) < tolerance

        def is_above(lower, upper):
            return upper.y < lower.y

        shoulder_angle = self.calculate_angle(left_shoulder, left_hip, left_knee)
        return (
                aligned_vertical(left_ankle, right_ankle) and
                aligned_vertical(left_knee, right_knee) and
                aligned_vertical(left_hip, right_hip) and
                aligned_vertical(left_shoulder, right_shoulder) and
                is_above(left_ankle, left_knee) and
                is_above(right_ankle, right_knee) and
                is_above(left_knee, left_hip) and
                is_above(right_knee, right_hip) and
                (160 < shoulder_angle < 200)  # Angle check
        )
    def is_padahastasana(self,landmarks):
        # Extracting landmarks
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # Check if both feet are straight (knees above ankles)
        feet_straight = left_knee.y < left_ankle.y and right_knee.y < right_ankle.y

        # Check if the shoulders are below the knees for proper forward bend
        body_bent_forward = left_shoulder.y > left_knee.y and right_shoulder.y > right_knee.y

        # Check if the shoulders are below the ankles to ensure the hands are reaching down
        hands_on_floor = left_shoulder.y < left_ankle.y and right_shoulder.y < right_ankle.y

        # Return true only if all conditions are met
        return feet_straight and body_bent_forward and hands_on_floor

    def get_pose_checks(self):
        return {
            "Tadasana": self.is_tadasana,
            "Padahastasana": self.is_padahastasana,
        }
