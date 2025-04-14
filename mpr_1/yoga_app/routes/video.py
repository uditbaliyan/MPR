# yoga_app/routes/video.py
from flask import Blueprint, Response
from yoga_app.utils.camera import Camera

video_bp = Blueprint('video', __name__)
camera = Camera()

@video_bp.route("/video_feed")
def video_feed():
    return Response(
        camera.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

