from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if not nombre or not email or not password or not confirm_password:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for("auth.register"))

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for("auth.register"))

        nuevo_usuario = Usuario(nombre=nombre, email=email, rol="usuario")
        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("index"))
        else:
            flash("Correo o contraseña incorrectos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))