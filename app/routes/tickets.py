from flask import Blueprint, render_template
from flask_login import login_required

tickets_bp = Blueprint("tickets", __name__)


@tickets_bp.route("/")
@login_required
def listar_tickets():
    return render_template("tickets/lista.html")