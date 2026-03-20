# 🚀 Flask Auth System

A **secure Flask web application** built to handle real-world authentication flows — not just login forms, but **verified users, protected routes, and attack resistance**.

This project focuses on doing the basics **correctly**, not just making them work.

---

## ⚡ Features

* 🔐 User Registration & Login
* 📧 Email Verification System
* 🔑 Secure Password Hashing
* 🚫 Rate Limiting (anti brute-force)
* 👤 Session Management (Flask-Login)
* 🛡️ Protected Dashboard
* 🧼 Input Validation

---

## 🧱 Tech Stack

**Backend**

* Python
* Flask
* Flask-Login
* Flask-SQLAlchemy
* Flask-Mail
* Flask-Limiter
* itsdangerous

**Database**

* SQLite

**Frontend**

* HTML / CSS / JavaScript

---

## ⚙️ Setup

### 1. Clone the repository

```bash id="cln01"
git clone https://github.com/your-username/flask-auth-system.git
cd flask-auth-system
```

### 2. Create virtual environment

```bash id="venv01"
python -m venv venv
```

Activate it:

**Windows**

```bash id="win01"
venv\Scripts\activate
```

**Linux / macOS**

```bash id="mac01"
source venv/bin/activate
```

---

### 3. Install dependencies

```bash id="dep01"
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file:

```env id="env01"
SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

> ⚠️ Never upload `.env` to GitHub

---

### 5. Run the application

```bash id="run01"
python app.py
```

Open:

```id="url01"
http://127.0.0.1:5000/
```

---

## 🧪 Workflow

1. Register account
2. Receive verification email
3. Activate account
4. Login
5. Access dashboard

---

## 🔐 Security

* Password hashing (Werkzeug)
* Token-based email verification
* Rate limiting on login
* Session protection
* Environment variable handling

---

## 📸 Preview

(Add your screenshots here)

---

## 🚧 Future Improvements

* Password reset system
* OAuth (Google login)
* Deployment (Render / VPS)
* Better UI/UX

---

## 👨‍💻 Author

**Muhammed Darwish**
🔗 https://github.com/optimuxprime8089856470

---

## ⭐ Note

This project proves you understand **how authentication actually works**.

If you extend this → you’re improving.
If you stop here → you’re still basic.
