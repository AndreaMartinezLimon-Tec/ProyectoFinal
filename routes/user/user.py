from flask import Blueprint, request, Flask, request, url_for, render_template, redirect, jsonify, make_response
from sqlalchemy import exc
from models import User
from app import session
from app import db, bcrypt
from auth import tokenCheck
from forms import UserForm,UserFormRegistro, UserFormObtener
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
                pop = "Datos incorrectos"
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


@appuser.route('/usuario', methods=["GET"])
@tokenCheck
def getUsers(usuario):
    mensaje =  "Vista de todos los usuarios"
    if usuario['admin']:
            output=[]
            usuarios = User.query.all()
            return render_template('usuario/usuario.html', usuarios = usuarios, mensaje=mensaje)
    else:
        return jsonify({"Mesaje","Es necesario tener los permisos administrador"})


@appuser.route('/usuario/editar/<int:id>', methods=['GET', 'POST'])
@tokenCheck
def editarUsuario(usuario, id):
    mensaje = "Editar usuario"
    if usuario['admin']:
        usuario = User.query.get_or_404(id)
        consultaForma = UserFormObtener(obj=usuario)
        if request.method == "POST":
            if consultaForma.validate_on_submit():
                consultaForma.populate_obj(usuario)
                db.session.commit()
                return redirect(url_for('appuser.getUsers'))
        return render_template('usuario/editarusuario.html', forma=consultaForma,mensaje=mensaje)
    else:
        return jsonify({"mensaje": "Es necesario tener permisos de administrador"})
    
    
@appuser.route('/usuario/eliminar/<int:id>', methods=['GET', 'POST'])
@tokenCheck
def eliminar(usuario, id):
    if usuario['admin']:
        usuario = User.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('appuser.getUsers'))
    return jsonify({"mensaje": "no eres admin"})