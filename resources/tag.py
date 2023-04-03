
# Flask imports
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

# DB Imports
from db import db
from models import TagModel, BrandModel
from schemas import TagSchema

# creating a blueprint
blp = Blueprint("Tags", "tags", description="Operation on tags")

@blp.route("/brand/<string:brand_id>/tag")
class TagsInBrands(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, brand_id):
        brand = BrandModel.query.get_or_404(brand_id)
        # returning all the tags assigned to a brand
        return brand.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, brand_id):
        tag = TagModel(**tag_data, brand_id=brand_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        " Returns searched tag else 404"
        tag = TagModel.query.get_or_404(tag_id)
        return tag