

from db import db

class BrandModel(db.Model):
    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # setting one-to-many relationship with table : brand in db
    items = db.relationship("ItemModel", back_populates="brand", lazy="dynamic")
    # setting up one-to-many relationship with table : tag in db
    tags = db.relationship("TagModel", back_populates="brand", lazy="dynamic")