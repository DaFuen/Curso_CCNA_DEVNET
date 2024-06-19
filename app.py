from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DATABASE_URL = 'sqlite:///usuarios.db'
Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/registrar', methods=['POST'])
def registrar():
    datos = request.get_json()
    nombre = datos['nombre']
    apellido = datos['apellido']
    email = datos['email']
    password = datos['password']
    
    
    password_hash = generate_password_hash(password)
    
    
    nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, email=email, password_hash=password_hash)
    
   
    session.add(nuevo_usuario)
    session.commit()
    
    return jsonify({'mensaje': 'Usuario registrado exitosamente'})


@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    datos = request.get_json()
    email = datos['email']
    password = datos['password']
    
    
    usuario = session.query(Usuario).filter_by(email=email).first()
    
    if usuario and check_password_hash(usuario.password_hash, password):
        return jsonify({'mensaje': 'Inicio de sesión exitoso'})
    else:
        return jsonify({'mensaje': 'Email o contraseña inválidos'}), 401

if __name__ == '__main__':
    app.run(port=8500)
