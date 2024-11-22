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

    def is_trikonasana(self, landmarks):
        # Get key landmarks
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        
        # Calculate angles
        hip_angle = self.calculate_angle(left_shoulder, left_hip, left_ankle)
        body_side_tilt = abs(left_hip.x - right_hip.x)
        
        # Check for wide leg stance
        leg_width = abs(left_ankle.x - right_ankle.x)
        
        # Check for side bend
        body_bent_sideways = (
            abs(left_shoulder.y - right_shoulder.y) > 0.1 and 
            abs(left_hip.y - right_hip.y) > 0.1
        )
        
        return (
            body_side_tilt > 0.2 and  # Legs are spread
            body_bent_sideways and  # Body is bent sideways
            (70 < hip_angle < 110)  # Moderate angle suggesting side bend
        )

    def is_virabhadrasana_i(self, landmarks):
        # Get key landmarks
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # Calculate knee angle to check lunge depth
        knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        
        # Check for forward lunge position
        is_lunged = (
            left_knee.y > left_hip.y and  # Front knee bent
            left_ankle.y > left_hip.y and  # Front foot forward
            knee_angle < 120  # Deep enough lunge
        )
        
        # Check for raised arms (optional, can be modified)
        arms_raised = (
            left_shoulder.y < left_hip.y and 
            right_shoulder.y < right_hip.y
        )
        
        return is_lunged and arms_raised

    def is_vrksasana(self, landmarks):
        # Get key landmarks
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # Check if one leg is lifted
        def is_leg_lifted(ankle, knee, hip):
            return ankle.y > knee.y and knee.y > hip.y

        # Check body alignment
        def is_body_straight(left, right):
            return abs(left.x - right.x) < 0.1

        # Check for one leg standing
        left_leg_lifted = is_leg_lifted(left_ankle, left_knee, left_hip)
        right_leg_lifted = is_leg_lifted(right_ankle, right_knee, right_hip)
        
        # Ensure body remains mostly vertical
        body_vertical = is_body_straight(left_shoulder, right_shoulder) and is_body_straight(left_hip, right_hip)
        
        return (left_leg_lifted or right_leg_lifted) and body_vertical

    def is_bhujangasana(self, landmarks):
        # New logic for Bhujangasana (Cobra Pose)
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        
        body_stretched = (
            left_shoulder.y < left_hip.y and
            right_shoulder.y < right_hip.y
        )
        return body_stretched

    def is_dandasana(self, landmarks):
        # New logic for Dandasana (Staff Pose)
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        is_straight = (
            left_ankle.x > left_hip.x and
            right_ankle.x > right_hip.x
        )
        return is_straight

    def is_adho_mukha_svanasana(self, landmarks):
        """
        Check if the person is in Downward-Facing Dog (Adho Mukha Svanasana) pose.

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Adho Mukha Svanasana, otherwise False.
        """
        # Extract key landmarks
        left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]

        # Helper functions for clarity
        def hips_are_highest():
            return (
                left_hip.y < left_shoulder.y and
                right_hip.y < right_shoulder.y and
                left_hip.y < left_ankle.y and
                right_hip.y < right_ankle.y
            )

        def arms_are_straight():
            return (
                self.calculate_angle(left_shoulder, left_elbow, left_wrist) > 160 and
                self.calculate_angle(right_shoulder, right_elbow, right_wrist) > 160
            )

        def legs_are_straight():
            return (
                self.calculate_angle(left_hip, left_knee, left_ankle) > 160 and
                self.calculate_angle(right_hip, right_knee, right_ankle) > 160
            )

        def body_forms_v_shape():
            return (
                self.calculate_angle(left_wrist, left_hip, left_ankle) > 30 and
                self.calculate_angle(right_wrist, right_hip, right_ankle) > 30
            )

        # Combine all conditions
        return hips_are_highest() and arms_are_straight() and legs_are_straight() and body_forms_v_shape()

    def is_balasana(self, landmarks):
        """
        Check if the person is in Child's Pose (Balasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Balasana, otherwise False.
        """
        # Function to calculate the Euclidean distance between two points
        def calculate_distance(point1, point2):
            """
            Calculate the Euclidean distance between two points.

            Parameters:
                point1, point2: Objects with x, y, z coordinates.

            Returns:
                float: The distance between the points.
            """
            return ((point1.x - point2.x) ** 2 + 
                    (point1.y - point2.y) ** 2 + 
                    (point1.z - point2.z) ** 2) ** 0.5

        # Extract key landmarks
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        nose = landmarks[self.mp_pose.PoseLandmark.NOSE.value]

        # Conditions to check:
        # 1. Knees should be bent and close to the ground
        knees_on_ground = (
            left_knee.y > left_ankle.y and
            right_knee.y > right_ankle.y and
            abs(left_knee.y - right_knee.y) < 0.1  # Knees aligned horizontally
        )

        # 2. Hips should be close to the heels
        hips_near_heels = (
            calculate_distance(left_hip, left_ankle) < 0.2 and
            calculate_distance(right_hip, right_ankle) < 0.2
        )

        # 3. Torso should be bent forward with nose close to the ground
        torso_bent_forward = (
            calculate_distance(nose, left_knee) < 0.2 or
            calculate_distance(nose, right_knee) < 0.2
        )

        # 4. Arms can be stretched forward or resting alongside the body
        arms_forward = (
            left_shoulder.y < left_hip.y and
            right_shoulder.y < right_hip.y
        )

        return knees_on_ground and hips_near_heels and torso_bent_forward and arms_forward


    def is_setu_bandhasana(self, landmarks):
        """
        Check if the person is in Bridge Pose (Setu Bandhasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Setu Bandhasana, otherwise False.
        """
        # Extract key landmarks
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        shoulders = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        ]

        # Conditions to check:
        # 1. Knees should be bent
        knees_bent = (
            left_knee.y < left_ankle.y and
            right_knee.y < right_ankle.y
        )

        # 2. Hips should be lifted significantly above the ground
        hips_lifted = (
            left_hip.y < left_knee.y and
            right_hip.y < right_knee.y
        )

        # 3. Shoulders should remain on the ground
        shoulders_on_ground = all(shoulder.y > left_hip.y for shoulder in shoulders)

        return knees_bent and hips_lifted and shoulders_on_ground


    def is_cat_cow_pose(self, landmarks):
        """
        Check if the person is transitioning between Cat and Cow Pose.

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            str: "Cat Pose", "Cow Pose", or "Neither" based on the detected posture.
        """
        # Extract key landmarks
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        nose = landmarks[self.mp_pose.PoseLandmark.NOSE.value]

        # Calculate average shoulder and hip positions
        avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        avg_hip_y = (left_hip.y + right_hip.y) / 2

        # Conditions for Cat Pose:
        is_cat_pose = (
            avg_shoulder_y < avg_hip_y and  # Shoulders above hips
            nose.y > avg_shoulder_y  # Head tucked down
        )

        # Conditions for Cow Pose:
        is_cow_pose = (
            avg_shoulder_y > avg_hip_y and  # Shoulders below hips
            nose.y < avg_shoulder_y  # Head lifted
        )

        if is_cat_pose:
            return "Cat Pose"
        elif is_cow_pose:
            return "Cow Pose"
        else:
            return "Neither"

    def is_phalakasana(self, landmarks):
        """
        Check if the person is in Plank Pose (Phalakasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Phalakasana, otherwise False.
        """
        # Extract key landmarks
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        # Calculate average positions
        avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        avg_hip_y = (left_hip.y + right_hip.y) / 2
        avg_ankle_y = (left_ankle.y + right_ankle.y) / 2

        # Conditions to check:
        # 1. Shoulders, hips, and ankles should form a straight line
        alignment = abs(avg_shoulder_y - avg_hip_y) < 0.05 and abs(avg_hip_y - avg_ankle_y) < 0.05

        return alignment


    def is_dhanurasana(self, landmarks):
        """
        Check if the person is in Bow Pose (Dhanurasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Dhanurasana, otherwise False.
        """
        # Extract key landmarks
        left_hand = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_hand = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        # Conditions to check:
        # 1. Hands should be near ankles
        hands_on_ankles = (
            abs(left_hand.x - left_ankle.x) < 0.1 and
            abs(right_hand.x - right_ankle.x) < 0.1 and
            abs(left_hand.y - left_ankle.y) < 0.1 and
            abs(right_hand.y - right_ankle.y) < 0.1
        )

        return hands_on_ankles


    def is_ustrasana(self, landmarks):
        """
        Check if the person is in Camel Pose (Ustrasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Ustrasana, otherwise False.
        """
        # Extract key landmarks
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_heel = landmarks[self.mp_pose.PoseLandmark.LEFT_HEEL.value]
        right_heel = landmarks[self.mp_pose.PoseLandmark.RIGHT_HEEL.value]

        # Conditions to check:
        # 1. Hips should be forward relative to knees
        hips_forward = (
            left_hip.x > left_shoulder.x and
            right_hip.x > right_shoulder.x
        )

        # 2. Hands should be near the heels
        hands_to_heels = (
            abs(left_heel.y - left_hip.y) < 0.2 and
            abs(right_heel.y - right_hip.y) < 0.2
        )

        return hips_forward and hands_to_heels


    def is_paschimottanasana(self, landmarks):
        """
        Check if the person is in Seated Forward Bend (Paschimottanasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Paschimottanasana, otherwise False.
        """
        # Extract key landmarks
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_foot = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
        right_foot = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
        nose = landmarks[self.mp_pose.PoseLandmark.NOSE.value]

        # Conditions to check:
        # 1. Legs should be straight
        legs_straight = (
            left_knee.y > left_hip.y and
            right_knee.y > right_hip.y
        )

        # 2. Nose should be closer to the feet than hips
        forward_bend = (
            abs(nose.x - (left_foot.x + right_foot.x) / 2) < 0.1 and
            nose.y < left_hip.y
        )

        return legs_straight and forward_bend

    def is_padmasana(self, landmarks):
        """
        Check if the person is in Lotus Pose (Padmasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Padmasana, otherwise False.
        """
        # Extract key landmarks
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]

        # Conditions to check:
        # 1. Ankles are above the knees (cross-legged position)
        ankles_above_knees = (
            left_ankle.y < left_knee.y and
            right_ankle.y < right_knee.y
        )

        return ankles_above_knees


    def is_navasana(self, landmarks):
        """
        Check if the person is in Boat Pose (Navasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Navasana, otherwise False.
        """
        # Extract key landmarks
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_foot = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
        right_foot = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # Conditions to check:
        # 1. Knees and feet are above hips
        knees_above_hips = (
            left_knee.y < left_hip.y and
            right_knee.y < right_hip.y and
            left_foot.y < left_hip.y and
            right_foot.y < right_hip.y
        )
        # 2. Shoulders are above hips (straight back)
        shoulders_above_hips = (
            left_shoulder.y < left_hip.y and
            right_shoulder.y < right_hip.y
        )

        return knees_above_hips and shoulders_above_hips


    def is_matsyasana(self, landmarks):
        """
        Check if the person is in Fish Pose (Matsyasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Matsyasana, otherwise False.
        """
        # Extract key landmarks
        head = landmarks[self.mp_pose.PoseLandmark.NOSE.value]
        chest = (landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y + 
                landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 2
        hips = (landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y + 
                landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y) / 2

        # Conditions to check:
        # 1. Chest is significantly higher than hips (arched back)
        arched_chest = chest < hips

        # 2. Head is near the floor
        head_low = head.y > hips

        return arched_chest and head_low


    def is_kapotasana(self, landmarks):
        """
        Check if the person is in Pigeon Pose (Kapotasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Kapotasana, otherwise False.
        """
        # Extract key landmarks
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_foot = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
        right_foot = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]

        # Conditions to check:
        # 1. One leg is extended back
        one_leg_extended = (
            abs(left_knee.x - right_foot.x) > 0.3 or
            abs(right_knee.x - left_foot.x) > 0.3
        )
        # 2. One knee bent forward
        knee_bent_forward = (
            left_knee.x < right_foot.x or
            right_knee.x < left_foot.x
        )

        return one_leg_extended and knee_bent_forward

    def is_savasana(self, landmarks):
        """
        Check if the person is in Corpse Pose (Savasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Savasana, otherwise False.
        """
        # Extract key landmarks
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]

        # Conditions to check:
        # 1. Shoulders and hips are aligned and body is flat
        body_flat = (
            abs(left_shoulder.y - left_hip.y) < 0.05 and
            abs(right_shoulder.y - right_hip.y) < 0.05
        )

        return body_flat


    def is_ardha_chandrasana(self, landmarks):
        """
        Check if the person is in Half Moon Pose (Ardha Chandrasana).

        Parameters:
            landmarks (list): A list of pose landmarks detected by MediaPipe.

        Returns:
            bool: True if the pose matches Ardha Chandrasana, otherwise False.
        """
        # Extract key landmarks
        left_foot = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
        right_foot = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
        left_hand = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_hand = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]

        # Conditions to check:
        # 1. One foot is off the ground
        single_leg_balance = abs(left_foot.y - right_foot.y) > 0.3
        # 2. One arm is extended upward
        arm_raised = right_hand.y < right_foot.y or left_hand.y < left_foot.y

        return single_leg_balance and arm_raised


    def get_pose_checks(self):
        return {
            "Tadasana": self.is_tadasana,
            "Padahastasana": self.is_padahastasana,
            "Trikonasana": self.is_trikonasana,
            "Virabhadrasana I": self.is_virabhadrasana_i,
            "Vrksasana": self.is_vrksasana,
            "Bhujangasana": self.is_bhujangasana,
            "Dandasana": self.is_dandasana,
            "Paschimottanasana": self.is_paschimottanasana,
            "Phalakasana": self.is_phalakasana,
            "Ustrasana": self.is_ustrasana,
            "Dhanurasana": self.is_dhanurasana,
            "Adho Mukha Svanasana": self.is_adho_mukha_svanasana,
            "Balasana": self.is_balasana,
            "Setu Bandhasana": self.is_setu_bandhasana,
            "Cat-Cow Pose": self.is_cat_cow_pose,
            "Padmasana": self.is_padmasana,
            "Navasana": self.is_navasana,
            "Matsyasana": self.is_matsyasana,
            "Kapotasana": self.is_kapotasana,
            "Savasana": self.is_savasana,
            "Ardha Chandrasana": self.is_ardha_chandrasana,
        }
