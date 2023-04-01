

from db import db

class BrandModel(db.Model):
    __tablename__ = "brands"

    id = db.Column(db.Interger, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="brand", lazy="dynamic")