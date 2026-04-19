from app.models import db
from app.models.base_model import BaseModel

class Producto(BaseModel):
    __tablename__ = 'productos'
    
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio_costo = db.Column(db.Numeric(10,2), nullable=False)
    precio_venta = db.Column(db.Numeric(10,2), nullable=False)
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=True)
    
    categoria = db.relationship('Categoria', back_populates='productos')
    proveedor = db.relationship('Proveedor', back_populates='productos')
    movimientos_stock = db.relationship('MovimientoStock', back_populates='producto')
    
    
    def __init__(self, nombre, descripcion, precio_costo, precio_venta, stock_actual, stock_minimo, categoria_id, proveedor_id) -> None:
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.categoria_id = categoria_id if categoria_id else None
        self.proveedor_id = proveedor_id if proveedor_id else None
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_costo': self.precio_costo,
            'precio_venta': self.precio_venta,
            'categoria_id': self.categoria_id,
            'proveedor_id': self.proveedor_id,
            'activo': self.activo,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        })
        return data