from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "troque-por-uma-chave-grande-e-secreta")

# ✅ Banco real no Railway: DATABASE_URL (PostgreSQL)
db_url = os.getenv("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Fallback local (no seu PC) continua SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(180), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    title = db.Column(db.String(140), nullable=False)
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.get("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Preencha email e senha.", "error")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Esse email já está cadastrado.", "error")
            return redirect(url_for("register"))

        user = User(email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        flash("Conta criada! Faça login.", "ok")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Email ou senha inválidos.", "error")
            return redirect(url_for("login"))

        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Digite a tarefa.", "error")
            return redirect(url_for("dashboard"))

        db.session.add(Task(user_id=current_user.id, title=title))
        db.session.commit()
        flash("Tarefa adicionada!", "ok")
        return redirect(url_for("dashboard"))

    tasks = (Task.query
             .filter_by(user_id=current_user.id)
             .order_by(Task.created_at.desc())
             .all())

    pending = [t for t in tasks if not t.done]
    done = [t for t in tasks if t.done]

    # stats para gráfico (últimos 7 dias)
    today = datetime.utcnow().date()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    labels = [d.strftime("%d/%m") for d in days]
    created_counts = [sum(1 for t in tasks if t.created_at.date() == d) for d in days]
    completed_counts = [sum(1 for t in done if t.created_at.date() == d) for d in days]
    stats = {"labels": labels, "created": created_counts, "completed": completed_counts}

    # eventos para calendário
    events = [{
        "title": ("✅ " if t.done else "🕒 ") + t.title,
        "start": t.created_at.strftime("%Y-%m-%d"),
        "allDay": True
    } for t in tasks]

    return render_template(
        "dashboard.html",
        tasks=tasks,
        pending=pending,
        done=done,
        stats=stats,
        events=events
    )


@app.post("/toggle/<int:task_id>")
@login_required
def toggle_task(task_id):
    t = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    t.done = not t.done
    db.session.commit()
    return redirect(url_for("dashboard"))


@app.post("/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    t = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(t)
    db.session.commit()
    flash("Tarefa excluída.", "ok")
    return redirect(url_for("dashboard"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
