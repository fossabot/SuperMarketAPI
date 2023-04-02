

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import BrandModel
from schemas import BrandSchema, ItemSchema

# creating a blueprint
blp = Blueprint("Brands", "brands", description="Operation on brands")


@blp.route("/brand/<string:brand_id>")
class Brand(MethodView):

    @blp.response(200, BrandSchema)
    def get(self, brand_id):
        brand_value = BrandModel.query.get_or_404(brand_id)
        return brand_value


    @blp.response(200)
    def delete(self, brand_id):
        brand_value = BrandModel.query.get_or_404(brand_id)
        db.session.delete(brand_value)
        db.session.commit()
        return {"message": "Store deleted"}


@blp.route("/brand")
class StoreList(MethodView):

    @blp.response(200, ItemSchema(many=True)) # many=True returns the value in <List of items>
    def get(self):
        return BrandModel.query.all()

    @blp.arguments(BrandSchema)
    @blp.response(201, BrandSchema) # 201 is status code for returning if data was inserted in db correctly
    def post(self, brand_data):
        brand_data = BrandModel(**brand_data)
        try:
            db.session.add(brand_data) # add data to db
            db.session.commit() # pushes added data inside db
        except IntegrityError:
            abort(400, message="Brand name already exists")
        except SQLAlchemyError:
            abort(500, message="Error occured while adding brand name to db")

        return brand_data

