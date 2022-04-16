from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://parayiv:gaga@192.168.80.6/sldb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)

#Creating model table for our CRUD database
class qradar(db.Model):
    id = db.Column(db.Integer)
    qr_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100))
    modification_date = db.Column(db.String(100))


    def to_dict(self):
        return {
            'id': self.id,
            'qr_id': self.qr_id,
            'name' : self.name,
            'TYPE' : self.TYPE,
            'owner': self.owner        
        }

"""       
#Creating model table for our CRUD database
class SECU(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100))
    modification_date = db.Column(db.String(100))


    def __init__(self, name, TYPE, enabled, owner, identifier, origin, creation_date, modification_date):
        self.id = id
        self.name = name
        self.TYPE = TYPE
        self.enabled = enabled
        self.owner = owner
        self.identifier = identifier
        self.origin = origin
        self.creation_date = creation_date
        self.modification_date = modification_date

#Creating model table for our NewUC
class newUC(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    Type = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100))
    modification_date = db.Column(db.String(100))

    def __init__(self, name, Type, enabled, owner, identifier, origin, creation_date, modification_date):
        self.name = name
        self.Type = Type
        self.enabled = enabled
        self.owner = owner
        self.identifier = identifier
        self.origin = origin
        self.creation_date = creation_date
        self.modification_date = modification_date

        """