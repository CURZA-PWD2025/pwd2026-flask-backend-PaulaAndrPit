from app.models import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'activo': self.activo,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }