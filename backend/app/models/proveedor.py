from app.models import db
from app.models.base_model import BaseModel


class Proveedor(BaseModel):
    __tablename__ = 'proveedores'
    
    nombre = db.Column(db.String(150), nullable=False)
    contacto = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    telefono = db.Column(db.String(30), nullable=True)
    
    productos = db.relationship('Producto', back_populates ='proveedor')
    
    def __init__(self, nombre, email=None, contacto=None, telefono=None) -> None:
        self.nombre = nombre
        self.contacto = contacto
        self.email = email
        self.telefono = telefono
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'id': self.id,
            'nombre': self.nombre,
            'contacto': self.contacto,
            'email': self.email,
            'telefono': self.telefono,
            'activo': self.activo,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        })
        return data