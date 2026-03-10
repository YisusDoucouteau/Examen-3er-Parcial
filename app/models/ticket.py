from datetime import datetime
from app import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado = db.Column(
        db.Enum("abierto", "en proceso", "cerrado"),
        default="abierto",
        nullable=False
    )
    prioridad = db.Column(
        db.Enum("baja", "media", "alta"),
        default="media",
        nullable=False
    )
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)