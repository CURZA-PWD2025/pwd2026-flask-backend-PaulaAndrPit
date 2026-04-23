from app.models import db 
from app.models.base_model import BaseModel

class Categoria(BaseModel):
    __tablename__ = 'categorias'
    
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    
    productos = db.relationship('Producto', back_populates='categoria')
    
    def __init__(self, nombre, descripcion=None) -> None:
        self.nombre = nombre
        self.descripcion = descripcion
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        })
        return data