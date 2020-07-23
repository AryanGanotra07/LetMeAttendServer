from src.extentions import ma
from src.models.SubjectModel import SubjectModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field,fields


class SubjectQuerySchema(SQLAlchemyAutoSchema):
  class Meta:
    model = SubjectModel
    fields = ("id", "name", "color")
#   password = auto_field(load_only = True)
