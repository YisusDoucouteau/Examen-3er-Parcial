from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import admin_required

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/")
@login_required
@admin_required
def listar_usuarios():
    return render_template("usuarios/lista.html")