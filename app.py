from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 🔥 NEW: load .env
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# 🔥 limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# 🔥 CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# 🔥 MAIL CONFIG (FIXED)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# 🔥 DATABASE MODEL
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

# 🔥 CREATE DB
with app.app_context():
    db.create_all()

# 🔥 LOGIN MANAGER
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# 🔥 ROUTES
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            if not user.is_verified:
                return render_template("index.html", error="Please verify your email first.")
            login_user(user)
            return redirect(url_for("dashboard"))

        return render_template("index.html", error="Invalid username or password")

    return render_template("index.html")

# 🔥 HELPERS
def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

def username_sec_check(username):
    return re.fullmatch(r"[A-Za-z0-9_]+", username)

# 🔥 REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not is_strong_password(password):
            return render_template("register.html", error="Weak password")

        if not username_sec_check(username):
            return render_template("register.html", error="Invalid username")

        existing_user = Users.query.filter_by(email=email).first()

        if existing_user:
            if not existing_user.is_verified:
                token = serializer.dumps(email, salt="email-verify")
                verify_url = url_for("verify_email", token=token, _external=True)

                msg = Message(
                    subject="Verify your email",
                    recipients=[email],
                    body=f"Click to verify:\n{verify_url}"
                )
                mail.send(msg)

                return "Verification email resent."

            return render_template("register.html", error="Email already registered!")

        if Users.query.filter_by(username=username).first():
            return render_template("register.html", error="Username taken!")

        hashed_password = generate_password_hash(password)

        new_user = Users(
            username=username,
            email=email,
            password=hashed_password,
            is_verified=False
        )
        db.session.add(new_user)
        db.session.commit()

        token = serializer.dumps(email, salt="email-verify")
        verify_url = url_for("verify_email", token=token, _external=True)

        msg = Message(
            subject="Verify your email",
            recipients=[email],
            body=f"Click to verify:\n{verify_url}"
        )
        mail.send(msg)

        return "Verification email sent!"

    return render_template("register.html")

# 🔥 VERIFY
@app.route("/verify/<token>")
def verify_email(token):
    try:
        email = serializer.loads(token, salt="email-verify", max_age=3600)
    except:
        return "Invalid or expired link"

    user = Users.query.filter_by(email=email).first()

    if user.is_verified:
        return "Already verified"

    user.is_verified = True
    db.session.commit()

    return redirect(url_for("index"))

# 🔥 DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

# 🔥 LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# 🔥 NO CACHE
@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# 🔥 RUN
if __name__ == "__main__":
    app.run(debug=True)