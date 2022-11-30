from flask import Flask, request, jsonify, render_template,session
from flask_session import Session
from flask_cors import CORS
from database import db
from encrypt import bcrypt
from flask_migrate import Migrate
from config import BaseConfig
from routes.imges.images import imageJuguete
from routes.user.user import appuser
from routes.proveedor.proveedor import appproveedor
from routes.juguete.juguete import appjuguete
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = "Pinocho"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.register_blueprint(appuser)
app.register_blueprint(appproveedor)
app.register_blueprint(appjuguete)
app.register_blueprint(imageJuguete)
app.config.from_object(BaseConfig)
CORS(app)
Session(app)
bootstrap = Bootstrap(app)

bcrypt.init_app(app)
db.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)

@app.route('/')
@app.route('/inicio')
@app.route('/index')
def inicio():
    user=""
    return render_template('index.html', user = user)

@app.errorhandler(404)
def paginaNoEncontrada(error):
    return render_template('404.html',error=error) , 404

@app.errorhandler(500)
def paginaNoEncontrada(error):
    return render_template('500.html',error=error) , 500