
# Flask imports
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

# DB Imports
from db import db
from models import TagModel, BrandModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

# creating a blueprint
blp = Blueprint("Tags", "tags", description="Operation on tags")

@blp.route("/brand/<int:brand_id>/tag")
class TagsInBrands(MethodView):

    @blp.alt_response(404, description="Tag not found")
    @blp.response(200, TagSchema(many=True), description="Gets all the assigned tags for the given 'brand_id'")
    def get(self, brand_id):
        brand = BrandModel.query.get_or_404(brand_id)
        # returning all the tags assigned to a brand
        return brand.tags.all()


    @blp.arguments(TagSchema)
    @blp.alt_response(500, description="Internal Error occurred when creating tag for 'brand_id'")
    @blp.response(201, TagSchema, description="Creates a tag for a particular 'brand_id'")
    def post(self, tag_data, brand_id):
        tag = TagModel(**tag_data, brand_id=brand_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):

    @blp.alt_response(404, description="tag not found")
    @blp.response(200, TagSchema, description="Returns tag details from 'tag_id'")
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag


    @blp.response(204, description="Deletes a tag if no item is tagged with it", example={"message" : "Tag deleted"})
    @blp.alt_response(404, description="When Tag is not found")
    @blp.alt_response(400, description="Returned if tag is assigned to 1 or more items. Tag will not be deleted")
    def delete(self, tag_id):

        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items: # if tag is not linked to any items, proceed with deleting that tag
            db.session.delete(tag)
            db.session.commit()
            return {"message" : "Tag deleted"}

        abort(400, message="Tag is assigned to 1 or more items. Please unlike the Tag and item(s) before deleting")


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):

    @blp.alt_response(500, description="Internal Error occurred when linking item with tag")
    @blp.alt_response(404, description="Item or Tag is not found to link with eachother")
    @blp.response(201, TagSchema, description="Creates a link between tag and items")
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        try:
            # creating the link
            item.tags.append(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort (500, message = "Received an error while creating item and tag link")

        return tag

    @blp.alt_response(500, description="Internal Error occurred when un-linking item with tag")
    @blp.alt_response(404, description="Item or Tag is not found to un-link with eachother")
    @blp.response(204, TagAndItemSchema, description="Deletes a link between tag and items")
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        try:
            # deleting the link between item and tag
            item.tags.remove(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "Received a error while deleting item and tag link")


        return {"message" : "Item removed from the tag", "item" : item, "tag" : tag}