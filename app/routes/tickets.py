from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.ticket import Ticket
from app.models.categoria import Categoria
from app.models.usuario import Usuario

tickets_bp = Blueprint("tickets", __name__)


# LISTAR Y FILTRAR TICKETS
@tickets_bp.route("/", methods=["GET"])
@login_required
def listar_tickets():
    estado = request.args.get("estado")

    if current_user.rol == "admin":
        query = Ticket.query
    else:
        query = Ticket.query.filter_by(usuario_id=current_user.id)

    if estado:
        query = query.filter_by(estado=estado)

    tickets = query.order_by(Ticket.fecha.desc()).all()

    return render_template("tickets/lista.html", tickets=tickets, estado_actual=estado)


# CREAR TICKET
@tickets_bp.route("/crear", methods=["GET", "POST"])
@login_required
def crear_ticket():
    categorias = Categoria.query.all()
    usuarios = Usuario.query.all()

    if request.method == "POST":
        titulo = request.form.get("titulo")
        descripcion = request.form.get("descripcion")
        estado = request.form.get("estado")
        prioridad = request.form.get("prioridad")
        categoria_id = request.form.get("categoria_id")

        if current_user.rol == "admin":
            usuario_id = request.form.get("usuario_id")
        else:
            usuario_id = current_user.id

        if not titulo or not descripcion or not categoria_id:
            flash("Título, descripción y categoría son obligatorios.", "danger")
            return redirect(url_for("tickets.crear_ticket"))

        nuevo_ticket = Ticket(
            titulo=titulo,
            descripcion=descripcion,
            estado=estado,
            prioridad=prioridad,
            usuario_id=usuario_id,
            categoria_id=categoria_id
        )

        db.session.add(nuevo_ticket)
        db.session.commit()

        flash("Ticket creado correctamente.", "success")
        return redirect(url_for("tickets.listar_tickets"))

    return render_template(
        "tickets/crear.html",
        categorias=categorias,
        usuarios=usuarios
    )


# EDITAR TICKET
@tickets_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    if current_user.rol != "admin" and ticket.usuario_id != current_user.id:
        flash("No tienes permiso para editar este ticket.", "danger")
        return redirect(url_for("tickets.listar_tickets"))

    categorias = Categoria.query.all()
    usuarios = Usuario.query.all()

    if request.method == "POST":
        ticket.titulo = request.form.get("titulo")
        ticket.descripcion = request.form.get("descripcion")
        ticket.estado = request.form.get("estado")
        ticket.prioridad = request.form.get("prioridad")
        ticket.categoria_id = request.form.get("categoria_id")

        if current_user.rol == "admin":
            ticket.usuario_id = request.form.get("usuario_id")

        db.session.commit()
        flash("Ticket actualizado correctamente.", "success")
        return redirect(url_for("tickets.listar_tickets"))

    return render_template(
        "tickets/editar.html",
        ticket=ticket,
        categorias=categorias,
        usuarios=usuarios
    )


# ELIMINAR TICKET
@tickets_bp.route("/eliminar/<int:id>")
@login_required
def eliminar_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    if current_user.rol != "admin" and ticket.usuario_id != current_user.id:
        flash("No tienes permiso para eliminar este ticket.", "danger")
        return redirect(url_for("tickets.listar_tickets"))

    db.session.delete(ticket)
    db.session.commit()
    flash("Ticket eliminado correctamente.", "warning")
    return redirect(url_for("tickets.listar_tickets"))
