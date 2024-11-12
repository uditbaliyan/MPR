# yoga_app/routes/main.py
from flask import Blueprint, render_template, request
from yoga_app.models.recommendations import AsanaRecommendations

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            gender = request.form.get("gender", "other")
            age = int(request.form.get("age", 0))
            asanas = AsanaRecommendations.get_recommendations(age, gender)
            return render_template("recommendations.html", asanas=asanas, age=age, gender=gender)
        except ValueError:
            return render_template("index.html", error="Please enter a valid age")
    return render_template("index.html")

@main_bp.route("/pose_analysis")
def pose_analysis():
    return render_template("pose_analysis.html")