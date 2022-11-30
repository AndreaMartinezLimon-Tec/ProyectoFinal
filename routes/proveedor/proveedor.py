from flask import Blueprint, request, jsonify
from sqlalchemy import exc
from models import User,Proveedor
from app import db, bcrypt
from auth import tokenCheck
appproveedor = Blueprint('appproveedor',__name__,template_folder="template")

@appproveedor.route('/agregarproveedor', methods=['POST'])
@tokenCheck
def registro(usuario):
    proveedor = request.get_json()
    proveedorExist = Proveedor.query.filter_by(nombre=proveedor['nombre']).first()
    if not proveedorExist:
        agregar = Proveedor(nombre=proveedor['nombre'], telefono=proveedor['telefono'], marca=proveedor['marca'])
        try:
            db.session.add(agregar)
            db.session.commit()
            mensaje = "Proveedor agregado"
        except exc.SQLAlchemyError as e:
            mensaje = print(e)
    else:
        mensaje="El proveedor ya existe"
    return jsonify({"mensaje":mensaje})

@appproveedor.route('/proveedores', methods=["GET"])
@tokenCheck
def getUsers(usuario):
    print (usuario)
    if usuario['admin']:
        output=[]
        proveedores = Proveedor.query.all()
        for proveedor in proveedores:
            obj = {}
            obj['id']=proveedor.id
            obj['nombre']=proveedor.nombre
            obj['telefono']=proveedor.telefono
            obj['marca'] = proveedor.marca
            output.append(obj)
        return jsonify({'proveedor':output})