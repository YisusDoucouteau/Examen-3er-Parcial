from flask import Blueprint, render_template
from flask_login import login_required

categorias_bp = Blueprint("categorias", __name__)


@categorias_bp.route("/")
@login_required
def listar_categorias():
    return render_template("categorias/lista.html")