from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.categoria import Categoria
from app.models.ticket import Ticket

categorias_bp = Blueprint("categorias", __name__)


# LISTAR CATEGORIAS
@categorias_bp.route("/")
@login_required
def listar_categorias():
    categorias = Categoria.query.order_by(Categoria.id.asc()).all()
    return render_template("categorias/listar.html", categorias=categorias)


# CREAR CATEGORIA
@categorias_bp.route("/crear", methods=["GET", "POST"])
@login_required
def crear_categoria():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not nombre:
            flash("El nombre es obligatorio.", "danger")
            return redirect(url_for("categorias.crear_categoria"))

        categoria_existente = Categoria.query.filter_by(nombre=nombre).first()
        if categoria_existente:
            flash("Ya existe una categoría con ese nombre.", "danger")
            return redirect(url_for("categorias.crear_categoria"))

        nueva_categoria = Categoria(
            nombre=nombre,
            descripcion=descripcion
        )

        db.session.add(nueva_categoria)
        db.session.commit()

        flash("Categoría creada correctamente.", "success")
        return redirect(url_for("categorias.listar_categorias"))

    return render_template("categorias/crear.html")


# EDITAR CATEGORIA
@categorias_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not nombre:
            flash("El nombre es obligatorio.", "danger")
            return redirect(url_for("categorias.editar_categoria", id=id))

        categoria_existente = Categoria.query.filter(
            Categoria.nombre == nombre,
            Categoria.id != id
        ).first()

        if categoria_existente:
            flash("Ya existe otra categoría con ese nombre.", "danger")
            return redirect(url_for("categorias.editar_categoria", id=id))

        categoria.nombre = nombre
        categoria.descripcion = descripcion

        db.session.commit()

        flash("Categoría actualizada correctamente.", "success")
        return redirect(url_for("categorias.listar_categorias"))

    return render_template("categorias/editar.html", categoria=categoria)


# ELIMINAR CATEGORIA
@categorias_bp.route("/eliminar/<int:id>")
@login_required
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    ticket_asociado = Ticket.query.filter_by(categoria_id=categoria.id).first()
    if ticket_asociado:
        flash("No se puede eliminar la categoría porque tiene tickets asociados.", "danger")
        return redirect(url_for("categorias.listar_categorias"))

    db.session.delete(categoria)
    db.session.commit()

    flash("Categoría eliminada correctamente.", "warning")
    return redirect(url_for("categorias.listar_categorias"))