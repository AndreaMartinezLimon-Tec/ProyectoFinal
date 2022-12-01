from models import User
from functools import wraps
from flask import request, jsonify,redirect,url_for,render_template
from app import session

def ObtenerInfo(token):
    if token:
        resp = User.decode_auth_token(token)
        user = User.query.filter_by(id = resp).first()
        if user:
            usuario = {
                'status':'Exitoso',
                'data':{
                    'id':user.id,
                    'email':user.email,
                    'admin':user.admin,
                    'registered_on':user.registered_on
                }
            }
            return usuario
        else:
            return {
                "status":"Fallido"
            }

def tokenCheck(f):
    @wraps(f)
    def verificar(*args,**kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        elif 'token' in session:
            token = session['token']
        if not token:
            return redirect(url_for('appuser.login'))
        try:
            info = ObtenerInfo(token)
            print(info)
            if info['status']=="Fallido":
                return redirect(url_for('appuser.login'))
        except:
            return redirect(url_for('appuser.login'))
        return f(info['data'],*args,**kwargs)
    return verificar