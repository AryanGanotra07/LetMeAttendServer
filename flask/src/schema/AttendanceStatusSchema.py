from src.extentions import ma
from src.models.AttendanceStatusModel import AttendanceStatusModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field,fields

class AttendanceStatusSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = AttendanceStatusModel
#   password = auto_field(load_only = True)
#   emailleads = fields.Nested(EmailSchema, many = True)