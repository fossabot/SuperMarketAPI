

from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=False)

    # Setting up one-to-many relationship with db table : brand
    brand = db.relationship("BrandModel", back_populates="tags")

    # Setting up many-to-many relationship between 'items' and 'tags' in secondary table : 'item_tags'
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")


