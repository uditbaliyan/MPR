# yoga_app/routes/main.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from yoga_app.models import User, db
from yoga_app.models.recommendations import AsanaRecommendations
import re
from functools import wraps

main_bp = Blueprint('main', __name__)

# Helper function to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route("/")
def home():
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    return redirect(url_for('main.login'))

@main_bp.route("/pose_recommendations", methods=["GET", "POST"])
@login_required
def index():
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found. Please log in again.')
        return redirect(url_for('main.logout'))
    
    if request.method == "POST":
        try:
            gender = request.form.get("gender", "other")
            age = int(request.form.get("age", 0))
            if age <= 0:
                raise ValueError("Age must be positive.")
            
            asanas = AsanaRecommendations.get_recommendations(age, gender)
            return render_template("recommendations.html", asanas=asanas, age=age, gender=gender, user=user)
        except ValueError as e:
            flash(f"Error: {str(e)}")
            return render_template("index.html", error=str(e), user=user)

    return render_template("index.html", user=user)

@main_bp.route("/pose_analysis")
@login_required
def pose_analysis():
    return render_template("pose_analysis.html")

@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        # Input validations
        if not all([username, email, password, confirm_password]):
            flash("All fields are required.")
            return redirect(url_for("main.register"))
        
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("main.register"))
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address.")
            return redirect(url_for("main.register"))
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Choose another.")
            return redirect(url_for("main.register"))
        
        if User.query.filter_by(email=email).first():
            flash("Email is already registered. Try logging in.")
            return redirect(url_for("main.register"))
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)  # Assumes a secure password hashing method in your User model
        db.session.add(user)
        db.session.commit()
        
        flash("Registration successful! Please log in.")
        return redirect(url_for("main.login"))

    return render_template("register.html")

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):  # Assumes check_password method verifies hashed password
            session["user_id"] = user.id
            flash("Logged in successfully!")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid username or password.")
            return redirect(url_for("main.login"))

    return render_template("login.html")

@main_bp.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.")
    return redirect(url_for("main.login"))
