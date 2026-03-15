from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func

from app.models.ticket import Ticket
from app.models.categoria import Categoria
from app import db
from app.services.ai_service import generar_respuesta_ia

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    total = Ticket.query.count()
    abiertos = Ticket.query.filter_by(estado="abierto").count()
    en_proceso = Ticket.query.filter_by(estado="en proceso").count()
    cerrados = Ticket.query.filter_by(estado="cerrado").count()

    categorias_query = (
        db.session.query(Categoria.nombre, func.count(Ticket.id))
        .join(Ticket)
        .group_by(Categoria.id)
        .all()
    )

    categorias = [[nombre, cantidad] for nombre, cantidad in categorias_query]

    alerta = None
    if abiertos > cerrados:
        alerta = "Se detecta una mayor cantidad de tickets abiertos que cerrados, lo que podría indicar acumulación de incidencias pendientes."
    elif cerrados >= abiertos and total > 0:
        alerta = "El sistema muestra un buen nivel de resolución, ya que los tickets cerrados igualan o superan a los abiertos."

    resumen_contexto = f"""
    Analiza estos datos del sistema de soporte técnico:

    Total de tickets: {total}
    Tickets abiertos: {abiertos}
    Tickets en proceso: {en_proceso}
    Tickets cerrados: {cerrados}
    Tickets por categoría: {categorias}

    Redacta un análisis breve en español, en un solo párrafo, natural y profesional.
    Menciona cuál categoría tiene más tickets y si existe carga alta de incidencias pendientes.
    No uses listas, no uses markdown, no pongas títulos.
    """

    analisis_ia = generar_respuesta_ia(resumen_contexto)

    return render_template(
        "dashboard.html",
        total=total,
        abiertos=abiertos,
        en_proceso=en_proceso,
        cerrados=cerrados,
        categorias=categorias,
        analisis_ia=analisis_ia,
        alerta=alerta
    )