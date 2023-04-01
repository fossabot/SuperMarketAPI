

from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    brand_id = db.Column(db.Interger, db.ForeignKey("brands.id"), unique=False, nullable=False)
    brand = db.relationship("BrandModel", back_populates="items")
