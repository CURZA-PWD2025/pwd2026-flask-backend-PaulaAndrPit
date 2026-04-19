from abc import abstractmethod
from typing import Literal

from sqlalchemy.exc import IntegrityError
#from app.models.producto import Producto--es necesario importarlo o ya basta con que este relacionado??
from app.models.categoria import Categoria
from app.models.proveedor import Proveedor
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller

class ProveedorController (Controller):
    
    @staticmethod
    def get_all() -> tuple[Response, int]:
        proveedores_list = db.session.execute(db.select(Proveedor).order_by(db.desc(Proveedor.id))).scalars().all()
        if len(proveedores_list) > 0:
            proveedores_to_dict = [proveedor.to_dict() for proveedor in proveedores_list ]
            return jsonify(proveedores_to_dict, 200), 200 
        return jsonify({"message": 'proveedores no encontrados'}, 404), 404
    

    @staticmethod
    def show(id)->tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        if proveedor:
            return jsonify(proveedor.to_dict(),200), 200
        return jsonify({"message": 'proveedor no encontrado'}, 404), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre:str = request.get[('nombre')]
        contacto: str = request[('contacto')]
        email: str = request[('email')]
        telefono: str = request[('telefono')]
        
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        
            
        if error is None:
            try:
                proveedor = Proveedor(nombre=nombre, contacto=contacto, email=email, telefono=telefono)
                db.session.add(proveedor)
                db.session.commit()
                return jsonify({'message': "proveedor creado con exito"}, 201), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "Proveedor ya registrado"}, 409), 409
        return jsonify ({'message': error}, 422), 422
        
        
    @staticmethod
    def update(request, id)->tuple[Response, int]:
        nombre:str = request.get['nombre']
        contacto: str = request[('contacto')]
        email: str = request[('email')]
        telefono: str = request[('telefono')]
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
                    
        if error is None:
            proveedor = db.session.get(Proveedor, id)
            if proveedor:
                try:
                    proveedor.nombre = nombre
                    proveedor.contacto = contacto
                    proveedor.email = email
                    proveedor.telefono = telefono
                    db.session.commit()
                    return jsonify({'message':'proveedor modificado con exito'}, 200), 200
                except IntegrityError:
                    error = 'el nombre ya existe' 
                    return jsonify({'message':error}, 409), 409
            else:     
                error = 'proveedor no encontrado'
            
        return jsonify({'message':error}, 404), 404
        
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        error = None
        if proveedor and len(proveedor.productos) == 0:
            db.session.delete(proveedor)
            db.session.commit()
            return jsonify({'message':'el proveedor fue eliminado con exito'}, 200), 200
        else:
            error = 'proveedor no encontrado o tiene productos asociados'
        return jsonify({'message':error}, 409), 409