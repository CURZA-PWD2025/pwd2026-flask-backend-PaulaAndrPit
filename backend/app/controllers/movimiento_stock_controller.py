from app.models import db
from flask import Response, jsonify
from app.controllers import Controller
from app.models.producto import Producto
from app.models.movimiento_stock import MovimientoStock
from sqlalchemy.exc import IntegrityError

class MovimientoStockController (Controller):
            
    @staticmethod
    def get_all() -> tuple[Response, int]:
        movimientos_list = db.session.execute(db.select(MovimientoStock).order_by(db.desc(MovimientoStock.id))).scalars().all()
        if len(movimientos_list) > 0:
            movimientos_to_dict = [movimiento.to_dict() for movimiento in movimientos_list ]
            return jsonify(movimientos_to_dict, 200), 200 
        return jsonify({"message": 'movimiento no encontrado'}, 404), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        movimiento = db.session.get(MovimientoStock, id)
        if movimiento:
            return jsonify(movimiento.to_dict(),200), 200
        return jsonify({"message": 'movimiento no encontrado'}, 404), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:            
        tipo_movimiento: str = request.get('tipo_movimiento')
        cantidad: int = request.get('cantidad')
        motivo: str = request.get('motivo')
        producto_id: int = request.get('producto_id')
        user_id: int = request.get('user_id')
    
    
        if tipo_movimiento is None:
            return jsonify({'message': 'El tipo de movimiento es requerido'}), 422
        if tipo_movimiento not in ['entrada', 'salida']:
            return jsonify({'message': 'El tipo de movimiento debe ser "entrada" o "salida"'}), 422
        if cantidad is None:
            return jsonify({'message': 'La cantidad es requerida'}), 422
        if cantidad <= 0:
            return jsonify({'message': 'La cantidad debe ser mayor a cero'}), 422
        if producto_id is None:
            return jsonify({'message': 'El producto es requerido'}), 422

        producto = db.session.get(Producto, producto_id)
        if producto is None:
            return jsonify({'message': 'Producto no encontrado'}), 404

        try:
            movimiento_stock = MovimientoStock(tipo_movimiento=tipo_movimiento,cantidad=cantidad,motivo=motivo,producto_id=producto_id,user_id=user_id)
            db.session.add(movimiento_stock)

            if tipo_movimiento == 'entrada':
                producto.stock_actual += cantidad
            else:
                if producto.stock_actual < cantidad:
                    return jsonify({'message': 'No hay suficiente stock para realizar la salida'}), 400
                producto.stock_actual -= cantidad

            db.session.commit()
            return jsonify({'message': 'Movimiento registrado con exito'}), 200

        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': 'Error al registrar el movimiento'}), 409
    
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        movimiento = db.session.get(MovimientoStock, id)
        error = None
        if movimiento:
            db.session.delete(movimiento)
            db.session.commit()
            return jsonify({'message':'el movimiento fue eliminado con exito'}), 200
        else:
            error = jsonify({'message': 'movimiento no encontrado'}), 404
        return error