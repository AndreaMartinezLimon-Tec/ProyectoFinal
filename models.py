import jwt
import datetime
from config import BaseConfig
from app import db, bcrypt

class User(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self,nombre = None,email = None,telefono = None,password = None,admin = None) -> None: 
        self.nombre = nombre 
        self.email = email
        self.telefono = telefono
        self.password=bcrypt.generate_password_hash(password, BaseConfig.BCRYPT_LOG_ROUND).decode()
        self.registered_on=datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, BaseConfig.SECRET_KEY, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, BaseConfig.SECRET_KEY, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError as e:
            return "Token Expirado"
        except jwt.InvalidTokenError as e:
            return "Token No Valido"

class Proveedor(db.Model):
    __tablename__ = "proveedor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(255), nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    juguetes = db.relationship("Juguete",cascade="all, delete-orphan", back_populates = "proveedor")

    def __init__(self,nombre,telefono,marca) -> None:
        self.nombre = nombre
        self.telefono = telefono
        self.marca = marca

class Juguete(db.Model):
    __tablename__ = "juguete"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    costo = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    proveedor = db.relationship('Proveedor', back_populates = "juguetes")

    def __init__(self,nombre,costo,cantidad,proveedor_id) -> None:
        self.nombre = nombre
        self.costo = costo
        self.cantidad = cantidad
        self.proveedor_id = proveedor_id

class Juguete_Imagen(db.Model):
    __tablename__ = "juguete_imagen"
    id_imagen = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    renderate_date = db.Column(db.Text, nullable=False)
    juguete_id = db.Column(db.Integer, db.ForeignKey('juguete.id'),nullable = False)
    juguete_relacion = db.relationship('Juguete', backref="juguete")
