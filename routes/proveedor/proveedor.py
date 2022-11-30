from flask import Blueprint, request, Flask, request, url_for, render_template, redirect, jsonify, make_response
from sqlalchemy import exc
from models import User,Proveedor
from app import db, bcrypt
from auth import tokenCheck
from forms import ProveedorForm
appproveedor = Blueprint('appproveedor',__name__,template_folder="template")

@appproveedor.route('/agregarproveedor', methods=['POST','GET'])
@tokenCheck
def registrop(usuario):
    mensaje = "Registro de proveedores"
    proveedorForma = ProveedorForm()
    if request.method == "POST":
        if proveedorForma.validate_on_submit():
            proveedor = {"nombre":proveedorForma.nombre.data, "telefono":proveedorForma.telefono.data,"marca": proveedorForma.marca.data}
            userExist = User.query.filter_by(email=proveedor['nombre']).first()
            if not userExist:
                agregar = Proveedor(nombre=proveedor['nombre'], telefono=proveedor['telefono'], marca=proveedor['marca'])
                try:
                    db.session.add(agregar)
                    db.session.commit()
                    mensaje = "Proveedor Creado"
                except exc.SQLAlchemyError as e:
                    mensaje = print(e)
            else:
                mensaje="El usuario ya existe"
            return render_template('proveedor/agregarproveedor.html', forma=proveedorForma, mensaje=mensaje)
    return render_template('proveedor/agregarproveedor.html', forma=proveedorForma, mensaje=mensaje)

@appproveedor.route('/proveedores', methods=["GET"])
@tokenCheck
def getProveedor(usuario):
    if usuario['admin']:
        output=[]
        proveedores = Proveedor.query.all()
        return render_template('proveedor/proveedor.html', proveedores=proveedores)
    else:
        return jsonify({"mensaje": "Es necesario tener permisos de administrador"})




@appproveedor.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
@tokenCheck
def editarProveedor(usuario, id):
    mensaje = "Editar proveedor"
    if usuario['admin']:
        proveedor = Proveedor.query.get_or_404(id)
        proveedorForma = ProveedorForm(obj=proveedor)
        if request.method == "POST":
            if proveedorForma.validate_on_submit():
                proveedorForma.populate_obj(proveedor)
                db.session.commit()
                return redirect(url_for('appproveedor.getProveedor'))
        return render_template('proveedor/editarproveedor.html', forma=proveedorForma,mensaje=mensaje)
    else:
        return jsonify({"mensaje": "Es necesario tener permisos de administrador"})

@appproveedor.route('/proveedores/eliminar/<int:id>', methods=['GET', 'POST'])
@tokenCheck
def eliminarproveedor(usuario, id):
    if usuario['admin']:
        proveedor = Proveedor.query.get_or_404(id)
        db.session.delete(proveedor)
        db.session.commit()
        return redirect(url_for('appproveedor.getProveedor'))
    return jsonify({"mensaje": "Es necesario tener permisos de administrador"})