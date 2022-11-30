from flask import Blueprint, request, jsonify
from sqlalchemy import exc
from models import User,Proveedor,Juguete
from app import db, bcrypt
from auth import tokenCheck
appjuguete = Blueprint('appjuguete',__name__,template_folder="template")

@appjuguete.route('/agregarjuguetes', methods=['POST'])
@tokenCheck
def registro(usuario):
    juguete = request.get_json()
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
    return jsonify({"mensaje":mensaje})

@appjuguete.route('/juguetes', methods=["GET"])
@tokenCheck
def getUsers(usuario):
    print (usuario)
    if usuario['admin']:
        output=[]
        juguetes = Juguete.query.all()
        for juguete in juguetes:
            obj = {}
            obj['id']=juguete.id
            obj['nombre']=juguete.nombre
            obj['costo']=juguete.costo
            obj['cantidad'] = juguete.cantidad
            obj['proveedor_id'] = juguete.proveedor_id
            output.append(obj)
        return jsonify({'proveedor':output})