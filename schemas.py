

# This file contains the schema for payload which user will
# send to the APIs.

from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Str(required=True)


class PlainBrandSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class ItemSchema(PlainItemSchema):
    brand_id = fields.Int(required=True, load_only=True)
    brand = fields.Nested(PlainBrandSchema(), dump_only=True)


class BrandSchema(PlainBrandSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)



class TagSchema(PlainTagSchema):
    brand_id = fields.Int(load_only=True)
    brand = fields.Nested(PlainBrandSchema(), dump_only=True)