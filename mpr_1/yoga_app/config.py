# yoga_app/config.py
class Config:
    DEBUG = True
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    MIN_DETECTION_CONFIDENCE = 0.5
    MIN_TRACKING_CONFIDENCE = 0.5
    MODEL_COMPLEXITY = 1
    SECRET_KEY = 'e11aa36470f4a9a632ff25e045d52a5df09e354c6b3bd8f8b1c8bc03f04ae38c'  # Change this to a secure secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
