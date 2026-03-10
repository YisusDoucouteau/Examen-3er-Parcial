from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Debes iniciar sesión para acceder.", "warning")
            return redirect(url_for("auth.login"))

        if current_user.rol != "admin":
            flash("No tienes permisos para acceder a esta sección.", "danger")
            return redirect(url_for("index"))

        return func(*args, **kwargs)
    return decorated_view