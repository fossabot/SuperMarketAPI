

from db import db

class ItemTags(db.Model):
    # A new table for storing many-to-many relationship between items and tags
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)

    # setting up many-to-many relationship between items and tags
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))