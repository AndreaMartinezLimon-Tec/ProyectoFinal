from flask import Blueprint, request, Flask, request, url_for, render_template, redirect, jsonify, make_response
from sqlalchemy import exc
from models import User,Proveedor,Juguete
from app import db, bcrypt
from auth import tokenCheck
from forms import JugueteForm
appjuguete = Blueprint('appjuguete',__name__,template_folder="template")

@appjuguete.route('/agregarjuguetes', methods=['POST','GET'])
@tokenCheck
def registro(usuario):
    mensaje = "Registro de juguetes"
    jugueteForma = JugueteForm()
    if request.method == "POST":
        if jugueteForma.validate_on_submit():
            juguete = {"nombre":jugueteForma.nombre.data, "costo":jugueteForma.costo.data,"cantidad": jugueteForma.cantidad.data,"proveedor_id": jugueteForma.proveedor_id.data}
            jugueteExist = Juguete.query.filter_by(nombre=juguete['nombre']).first()
            proveedorExist= Proveedor.query.filter_by(id=juguete['proveedor_id']).first()
            if not jugueteExist:
                if proveedorExist:
                    agregarj = Juguete(nombre=juguete['nombre'], costo=juguete['costo'], cantidad=juguete['cantidad'],proveedor_id=juguete['proveedor_id'])
                    try:
                        db.session.add(agregarj)
                        db.session.commit()
                        mensaje = "Juguete agregado"
                    except exc.SQLAlchemyError as e:
                        mensaje = print(e)
                else:
                    mensaje= "El proveedor no existe"
            else:
                mensaje="El juguete ya existe"
            return render_template('juguete/agregarjuguete.html', forma=jugueteForma, mensaje=mensaje)
    return render_template('juguete/agregarjuguete.html', forma=jugueteForma, mensaje=mensaje)

@appjuguete.route('/juguetes', methods=["GET"])
@tokenCheck
def getJuguete(usuario):
    if usuario['admin']:
        output=[]
        juguetes = Juguete.query.all()
        return render_template('juguete/juguete.html', juguetes=juguetes)
    else:
        return jsonify({"mensaje": "Es necesario tener permisos de administrador"})


@appjuguete.route('/juguetes/editar/<int:id>', methods=['GET', 'POST'])
@tokenCheck
def editarjuguete(usuario, id):
    mensaje = "Editar juguete"
    if usuario['admin']:
        juguete = Juguete.query.get_or_404(id)
        jugueteForma = JugueteForm(obj=juguete)
        if request.method == "POST":
            if jugueteForma.validate_on_submit():
                jugueteForma.populate_obj(juguete)
                db.session.commit()
                return redirect(url_for('appjuguete.getJuguete'))
        return render_template('juguete/editarjuguete.html', forma=jugueteForma,mensaje=mensaje)
    else:
        return jsonify({"mensaje": "Es necesario tener permisos de administrador"})

@appjuguete.route('/juguetes/eliminar/<int:id>', methods=['GET', 'POST'])
@tokenCheck
def eliminarjuguete(usuario, id):
    if usuario['admin']:
        juguete = Juguete.query.get_or_404(id)
        db.session.delete(juguete)
        db.session.commit()
        return redirect(url_for('appjuguete.getJuguete'))
    return jsonify({"mensaje": "Es necesario tener permisos de administrador"})