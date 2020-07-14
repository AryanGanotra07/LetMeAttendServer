from src.extentions import ma
from src.models.LectureModel import LectureModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field,fields

class LectureSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = LectureModel
#   password = auto_field(load_only = True)
#   emailleads = fields.Nested(EmailSchema, many = True)