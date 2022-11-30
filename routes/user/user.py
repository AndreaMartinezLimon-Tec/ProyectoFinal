from flask import Blueprint, request, Flask, request, url_for, render_template, redirect, jsonify, make_response
from sqlalchemy import exc
from models import User
from app import session
from app import db, bcrypt
from auth import tokenCheck
from forms import UserForm,UserFormRegistro
appuser = Blueprint('appuser',__name__,template_folder="template")

@appuser.route('/auth/login',methods={'POST','GET'})
def login():
    mensaje = "Inicio de Sesion"
    pop = ""
    usuarioForma = UserForm()
    if request.method == "POST":
        if usuarioForma.validate_on_submit():
            user = {"email": usuarioForma.email.data,"password": usuarioForma.password.data}
            usuario = User(email=user['email'], password=user["password"])
            searchUser = User.query.filter_by(email=usuario.email).first()
            if searchUser:
                validation = bcrypt.check_password_hash(searchUser.password,user["password"])
                if validation:
                    auth_token = usuario.encode_auth_token(user_id=searchUser.id)
                    responseObj = {
                        "status": "exitoso",
                        "mensaje": "Login",
                        "auth_token": auth_token
                    }
                    #print(responseObj)
                    session['token'] = auth_token
                    return render_template('index.html')
                pop.replace = "Datos incorrectos"
                return render_template('login.html', forma=usuarioForma, mensaje=mensaje, pop=pop)
            mensaje = "Usuario Creado"
    return render_template('login.html', forma=usuarioForma, mensaje=mensaje, pop=pop)

@appuser.route('/auth/registrar', methods={'POST','GET'})
def registro():
    mensaje = "Registro de Nuevo Usuario"
    registroForma = UserFormRegistro()
    if request.method == "POST":
        if registroForma.validate_on_submit():
            user = {"nombre":registroForma.nombre.data,"email": registroForma.email.data,"telefono":registroForma.telefono.data,"admin":0,"password": registroForma.password.data}
            userExist = User.query.filter_by(email=user['email']).first()
            if not userExist:
                usuario = User(nombre=user['nombre'], email=user['email'], telefono=user["telefono"], password=user["password"],admin=user["admin"])
                try:
                    db.session.add(usuario)
                    db.session.commit()
                    mensaje = "Usuario Creado"
                except exc.SQLAlchemyError as e:
                    mensaje = print(e)
            else:
                mensaje="El usuario ya existe"
            return render_template('registro.html', forma=registroForma, mensaje=mensaje)
    return render_template('registro.html', forma=registroForma, mensaje=mensaje)


# Sin modificar, es el mismo que el de arriba ^
# @appuser.route('/auth/registrar', methods=['POST'])
# def registro():
#     user = request.get_json()
#     userExist = User.query.filter_by(email=user['email']).first()
#     if not userExist:
#         usuario = User(nombre=user['nombre'], email=user['email'], telefono=user["telefono"], password=user["password"],admin=user["admin"])
#         try:
#             db.session.add(usuario)
#             db.session.commit()
#             mensaje = "Usuario Creado"
#         except exc.SQLAlchemyError as e:
#             mensaje = print(e)
#     else:
#         mensaje="El usuario ya existe"
#     return jsonify({"mensaje":mensaje})

@appuser.route('/usuarios', methods=["GET"])
@tokenCheck
def getUsers(usuario):
    print (usuario)
    if usuario['admin']:
        output=[]
        usuarios = User.query.all()
        for usuario in usuarios:
            obj = {}
            obj['id']=usuario.id
            obj['email']=usuario.email
            obj['password']=usuario.password
            obj['registered_on'] = usuario.registered_on
            obj['admin'] = usuario.admin
            output.append(obj)
        return jsonify({'usuarios':output})