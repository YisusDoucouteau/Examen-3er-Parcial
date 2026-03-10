from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.categoria import Categoria

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')


# LISTAR CATEGORIAS
@categorias_bp.route('/')
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template('categorias/listar.html', categorias=categorias)


# CREAR CATEGORIA
@categorias_bp.route('/crear', methods=['GET','POST'])
def crear_categoria():

    if request.method == 'POST':

        nombre = request.form['nombre']

        if not nombre:
            flash("El nombre es obligatorio", "error")
            return redirect(url_for('categorias.crear_categoria'))

        nueva_categoria = Categoria(nombre=nombre)

        db.session.add(nueva_categoria)
        db.session.commit()

        flash("Categoria creada correctamente")
        return redirect(url_for('categorias.listar_categorias'))

    return render_template('categorias/crear.html')


# EDITAR CATEGORIA
@categorias_bp.route('/editar/<int:id>', methods=['GET','POST'])
def editar_categoria(id):

    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':

        nombre = request.form['nombre']

        if not nombre:
            flash("El nombre es obligatorio")
            return redirect(url_for('categorias.editar_categoria', id=id))

        categoria.nombre = nombre

        db.session.commit()

        flash("Categoria actualizada")
        return redirect(url_for('categorias.listar_categorias'))

    return render_template('categorias/editar.html', categoria=categoria)


# ELIMINAR CATEGORIA
@categorias_bp.route('/eliminar/<int:id>')
def eliminar_categoria(id):

    categoria = Categoria.query.get_or_404(id)

    db.session.delete(categoria)
    db.session.commit()

    flash("Categoria eliminada")

    return redirect(url_for('categorias.listar_categorias'))