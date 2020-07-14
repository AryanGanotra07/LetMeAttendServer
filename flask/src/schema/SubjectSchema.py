from src.extentions import ma
from src.models.SubjectModel import SubjectModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field,fields
from .LectureSchema import LectureSchema

class SubjectSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = SubjectModel
#   password = auto_field(load_only = True)
  lectures = fields.Nested(LectureSchema, many = True)