from io import BytesIO
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app import db
from app.models.ticket import Ticket
from app.models.categoria import Categoria
from app.models.usuario import Usuario

from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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


# EXPORTAR TODOS LOS TICKETS A EXCEL
@tickets_bp.route("/exportar/excel")
@login_required
def exportar_tickets_excel():
    if current_user.rol == "admin":
        tickets = Ticket.query.order_by(Ticket.fecha.desc()).all()
    else:
        tickets = Ticket.query.filter_by(usuario_id=current_user.id).order_by(Ticket.fecha.desc()).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Tickets"

    encabezados = ["ID", "Título", "Descripción", "Estado", "Prioridad", "Usuario", "Categoría", "Fecha"]
    ws.append(encabezados)

    for ticket in tickets:
        ws.append([
            ticket.id,
            ticket.titulo,
            ticket.descripcion,
            ticket.estado,
            ticket.prioridad,
            ticket.usuario.nombre,
            ticket.categoria.nombre,
            ticket.fecha.strftime("%Y-%m-%d %H:%M")
        ])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="tickets.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# EXPORTAR UN SOLO TICKET A PDF
@tickets_bp.route("/exportar/pdf/<int:id>")
@login_required
def exportar_ticket_pdf(id):
    ticket = Ticket.query.get_or_404(id)

    if current_user.rol != "admin" and ticket.usuario_id != current_user.id:
        flash("No tienes permiso para exportar este ticket.", "danger")
        return redirect(url_for("tickets.listar_tickets"))

    output = BytesIO()
    p = canvas.Canvas(output, pagesize=letter)
    width, height = letter

    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Reporte Individual de Ticket")

    y -= 40
    p.setFont("Helvetica", 12)

    p.drawString(50, y, f"ID: {ticket.id}")
    y -= 25
    p.drawString(50, y, f"Título: {ticket.titulo}")
    y -= 25
    p.drawString(50, y, f"Estado: {ticket.estado}")
    y -= 25
    p.drawString(50, y, f"Prioridad: {ticket.prioridad}")
    y -= 25
    p.drawString(50, y, f"Usuario: {ticket.usuario.nombre}")
    y -= 25
    p.drawString(50, y, f"Categoría: {ticket.categoria.nombre}")
    y -= 25
    p.drawString(50, y, f"Fecha: {ticket.fecha.strftime('%Y-%m-%d %H:%M')}")

    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Descripción:")
    y -= 25

    p.setFont("Helvetica", 11)

    descripcion = ticket.descripcion
    max_chars = 90

    while descripcion:
        linea = descripcion[:max_chars]
        descripcion = descripcion[max_chars:]
        p.drawString(50, y, linea)
        y -= 18

        if y < 50:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 11)

    p.save()
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name=f"ticket_{ticket.id}.pdf",
        mimetype="application/pdf"
    )