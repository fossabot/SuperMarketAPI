

from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    # auto fills in db
    id = db.Column(db.Integer, primary_key=True)

    # Required attributes to input by the user
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), unique=False, nullable=False)

    # setting one-to-many relationship with table : items in db
    brand = db.relationship("BrandModel", back_populates="items")
