from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from sqlalchemy import func

from app.models.ticket import Ticket
from app.models.categoria import Categoria
from app import db
from app.services.ai_service import generar_respuesta_ia, clasificar_intencion

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chatbot-page")
@login_required
def chatbot_page():
    return render_template("chatbot.html")


@chatbot_bp.route("/chatbot", methods=["POST"])
@login_required
def chatbot():
    pregunta = request.json.get("pregunta", "").strip()

    if not pregunta:
        return jsonify({"respuesta": "Debes escribir una pregunta."})

    analisis = clasificar_intencion(pregunta)
    intent = analisis.get("intent", "desconocida")

    if intent == "total_tickets":
        total = Ticket.query.count()
        contexto = f"El usuario preguntó: '{pregunta}'. El sistema tiene {total} tickets registrados."
        return jsonify({"respuesta": generar_respuesta_ia(contexto)})

    elif intent == "tickets_abiertos":
        abiertos = Ticket.query.filter_by(estado="abierto").count()
        contexto = f"El usuario preguntó: '{pregunta}'. El sistema tiene {abiertos} tickets abiertos."
        return jsonify({"respuesta": generar_respuesta_ia(contexto)})

    elif intent == "tickets_cerrados":
        cerrados = Ticket.query.filter_by(estado="cerrado").count()
        contexto = f"El usuario preguntó: '{pregunta}'. El sistema tiene {cerrados} tickets cerrados."
        return jsonify({"respuesta": generar_respuesta_ia(contexto)})

    elif intent == "total_categorias":
        total_categorias = Categoria.query.count()
        contexto = f"El usuario preguntó: '{pregunta}'. El sistema tiene {total_categorias} categorías registradas."
        return jsonify({"respuesta": generar_respuesta_ia(contexto)})

    elif intent == "lista_categorias":
        categorias = Categoria.query.all()
        nombres = ", ".join([c.nombre for c in categorias]) if categorias else "ninguna"
        contexto = f"El usuario preguntó: '{pregunta}'. Las categorías registradas son: {nombres}."
        return jsonify({"respuesta": generar_respuesta_ia(contexto)})

    elif intent == "categoria_mas_usada":
        resultado = (
            db.session.query(Categoria.nombre, func.count(Ticket.id))
            .join(Ticket)
            .group_by(Categoria.id)
            .order_by(func.count(Ticket.id).desc())
            .first()
        )

        if resultado:
            nombre_categoria, cantidad = resultado
            contexto = (
                f"El usuario preguntó: '{pregunta}'. "
                f"La categoría con más tickets es {nombre_categoria} con {cantidad} incidencias."
            )
            return jsonify({"respuesta": generar_respuesta_ia(contexto)})

        return jsonify({"respuesta": "No hay datos suficientes para responder esa pregunta."})

    return jsonify({
        "respuesta": (
            "Puedo ayudarte con preguntas sobre tickets y categorías, por ejemplo: "
            "cuántos tickets hay, cuántos abiertos, cuántos cerrados, cuántas categorías hay o cuáles existen."
        )
    })