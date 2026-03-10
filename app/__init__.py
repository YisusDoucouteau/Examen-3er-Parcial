from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."


def create_default_admin():
    from app.models.usuario import Usuario

    admin_email = "admin@soporte.com"
    admin_password = "Admin123*"

    admin = Usuario.query.filter_by(email=admin_email).first()

    if not admin:
        nuevo_admin = Usuario(
            nombre="Administrador",
            email=admin_email,
            rol="admin"
        )
        nuevo_admin.set_password(admin_password)

        db.session.add(nuevo_admin)
        db.session.commit()
        print("Admin por defecto creado.")
    else:
        print("El admin por defecto ya existe.")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models.usuario import Usuario
    from app.models.categoria import Categoria
    from app.models.ticket import Ticket

    from app.routes.auth import auth_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.categorias import categorias_bp
    from app.routes.tickets import tickets_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(tickets_bp, url_prefix="/tickets")

    @app.route("/")
    def index():
        return render_template("index.html")

    with app.app_context():
        create_default_admin()

    return app