# yoga_app/models/recommendations.py
class AsanaRecommendations:
    RECOMMENDATIONS = {
        "young_adults": {
            "male": ["Surya Namaskar", "Warrior Pose", "Plank Pose", "Bridge Pose"],
            "female": ["Tree Pose", "Camel Pose", "Child's Pose", "Cobra Pose"],
            "other": ["Mountain Pose", "Seated Forward Bend", "Lotus Pose", "Butterfly Pose"]
        },
        "adults": {
            "male": ["Downward Dog", "Triangle Pose", "Chair Pose", "Warrior II"],
            "female": ["Cat-Cow Pose", "Bow Pose", "Bridge Pose", "Seated Forward Bend"],
            "other": ["Corpse Pose", "Half Spinal Twist", "Extended Side Angle", "Warrior I"]
        },
        "seniors": {
            "male": ["Mountain Pose", "Child's Pose", "Seated Twist", "Legs-Up-the-Wall"],
            "female": ["Easy Pose", "Cobra Pose", "Supported Bridge Pose", "Chair Pose"],
            "other": ["Bound Angle Pose", "Happy Baby Pose", "Gentle Twist", "Reclining Bound Angle"]
        }
    }

    @staticmethod
    def get_recommendations(age, gender):
        try:
            age = int(age)
            if age <= 35:
                group = "young_adults"
            elif age <= 55:
                group = "adults"
            else:
                group = "seniors"
        except (ValueError, TypeError):
            return AsanaRecommendations.RECOMMENDATIONS["adults"]["other"]
        
        return AsanaRecommendations.RECOMMENDATIONS.get(group, {}).get(
            gender, 
            AsanaRecommendations.RECOMMENDATIONS[group]["other"]
        )