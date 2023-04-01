
from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Str(required=True)


class PlainBrandSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class ItemSchema(PlainItemSchema):
    brand_id = fields.Int(required=True, load_only=True)
    brand = fields.Nested(PlainBrandSchema(), dump_only=True)


class BrandSchema(PlainBrandSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
