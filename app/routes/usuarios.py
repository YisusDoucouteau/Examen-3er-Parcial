from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.models.usuario import Usuario
from app import db

usuarios_bp = Blueprint("usuarios", __name__)


# LISTAR USUARIOS
@usuarios_bp.route("/")
@login_required
@admin_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template("usuarios/lista.html", usuarios=usuarios)


# CREAR USUARIO
@usuarios_bp.route("/crear", methods=["GET", "POST"])
@login_required
@admin_required
def crear_usuario():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")
        rol = request.form.get("rol")

        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for("usuarios.crear_usuario"))

        if Usuario.query.filter_by(email=email).first():
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for("usuarios.crear_usuario"))

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            rol=rol
        )
        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario creado correctamente.", "success")
        return redirect(url_for("usuarios.listar_usuarios"))

    return render_template("usuarios/crear.html")


# EDITAR USUARIO
@usuarios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == "POST":
        usuario.nombre = request.form.get("nombre")
        usuario.email = request.form.get("email")
        usuario.rol = request.form.get("rol")

        db.session.commit()
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("usuarios.listar_usuarios"))

    return render_template("usuarios/editar.html", usuario=usuario)


# ELIMINAR USUARIO
@usuarios_bp.route("/eliminar/<int:id>")
@login_required
@admin_required
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if usuario.id == current_user.id:
        flash("No puedes eliminar tu propia cuenta.", "danger")
        return redirect(url_for("usuarios.listar_usuarios"))

    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario eliminado correctamente.", "warning")
    return redirect(url_for("usuarios.listar_usuarios"))