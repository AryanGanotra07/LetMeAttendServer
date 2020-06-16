from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

ma = Marshmallow()
db = SQLAlchemy()
bcrypt = Bcrypt()
