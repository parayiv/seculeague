from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
from datetime import datetime
import random
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://parayiv:gaga@192.168.80.6/SLeagueDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)

#Creating model table for our CRUD database
class qradar(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qr_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modification_date = db.Column(db.String(100))
    last_updated = db.Column(db.Time, default=datetime.now().strftime("%Y-%m-%d %H:%M"))

    def to_dict(self):
        return {
            'id': self.id,
            'qr_id': self.qr_id,
            'name' : self.name,
            'TYPE' : self.TYPE,
            'enabled': self.enabled,
            'owner': self.owner,
            'identifier': self.identifier,
            'origin': self.origin,
            'creation_date': self.creation_date,
            'modification_date': self.modification_date,
            'last_updated': self.last_updated   
        }

#track all seculeague use cases: Added/removed/to be commited/
class Seculeague(db.Model):
    __tablename__ = 'Seculeague'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qr_id = db.Column(db.String(100))         #Note: This must be verified and the sl_id and the name vars default
    sl_id = db.Column(db.String(100))
    name = db.Column(db.String(200))
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modification_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20), default='News')
    current_tbl = db.Column(db.String(20), default='Seculeague')

    def to_dict(self):
        return {
            'id': self.id,
            'qr_id': self.qr_id,
            'sl_id': self.sl_id,
            'name' : self.name,
            'TYPE' : self.TYPE,
            'enabled': self.enabled,
            'owner': self.owner,
            'identifier': self.identifier,
            'origin': self.origin,
            'creation_date': self.creation_date,
            'modification_date': self.modification_date, 
            'status': self.status,
            'count': self.count,
            'comment': self.comment,
            'previous_tbl': self.previous_tbl,
            'current_tbl': self.current_tbl
        }

#Added use cases
class News(db.Model):
    __tablename__ = 'News'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qr_id = db.Column(db.String(100), default=secrets.token_hex(3))         #Note: This must be verified and the sl_id and the name vars default
    sl_id = db.Column(db.String(100), default=secrets.token_hex(3))
    name = db.Column(db.String(200), unique=True)
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modification_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer, default=1)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20), default='Null')
    current_tbl = db.Column(db.String(20), default='News')
    
    def to_dict(self):
        return {
            'id': self.id,
            'qr_id': self.qr_id,
            'sl_id': self.sl_id,
            'name' : self.name,
            'TYPE' : self.TYPE,
            'enabled': self.enabled,
            'owner': self.owner,
            'identifier': self.identifier,
            'origin': self.origin,
            'creation_date': self.creation_date,
            'modification_date': self.modification_date, 
            'status': self.status,
            'count': self.count,
            'comment': self.comment,
            'previous_tbl': self.previous_tbl,
            'current_tbl': self.current_tbl
        }

# The use cases That found in qradar but not found in seculeague
# Need to be traited then commited
class QrMinusSl(db.Model):
    __tablename__ = 'QrMinusSl'
    id = db.Column(db.Integer, autoincrement=True)
    qr_id = db.Column(db.String(100))         #Note: This must be verified and the sl_id and the name vars default
    sl_id = db.Column(db.String(100), default=secrets.token_hex(3))
    name = db.Column(db.String(200), primary_key=True)
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modification_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer, default=1)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20))
    current_tbl = db.Column(db.String(20), default='QrMinusSl')
    
    def to_dict(self):
        return {
            'id': self.id,
            'qr_id': self.qr_id,
            'sl_id': self.sl_id,
            'name' : self.name,
            'TYPE' : self.TYPE,
            'enabled': self.enabled,
            'owner': self.owner,
            'identifier': self.identifier,
            'origin': self.origin,
            'creation_date': self.creation_date,
            'modification_date': self.modification_date, 
            'status': self.status,
            'count': self.count,
            'comment': self.comment,
            'previous_tbl': self.previous_tbl,
            'current_tbl': self.current_tbl
        }


# The use cases That found in Seculeague but not found in qradar
# Need to be reevaluated
class SlMinusQr(db.Model):
    __tablename__ = 'SlMinusQr'
    id = db.Column(db.Integer, autoincrement=True)
    qr_id = db.Column(db.String(100))         #Note: This must be verified and the sl_id and the name vars default
    sl_id = db.Column(db.String(100))
    name = db.Column(db.String(200), primary_key=True,)
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modification_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer, default=1)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20))
    current_tbl = db.Column(db.String(20), default='SlMinusQr')

    def to_dict(self):
        return {
            'id': self.id,
            'qr_id': self.qr_id,
            'sl_id': self.sl_id,
            'name' : self.name,
            'TYPE' : self.TYPE,
            'enabled': self.enabled,
            'owner': self.owner,
            'identifier': self.identifier,
            'origin': self.origin,
            'creation_date': self.creation_date,
            'modification_date': self.modification_date, 
            'status': self.status,
            'count': self.count,
            'comment': self.comment,
            'previous_tbl': self.previous_tbl,
            'current_tbl': self.current_tbl
        }

#Removed Use case
class Rmvd(db.Model):
    __tablename__ = 'Rmvd'   
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qr_id = db.Column(db.String(100))         #Note: This must be verified and the sl_id and the name vars default
    sl_id = db.Column(db.String(100))
    name = db.Column(db.String(200))
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modification_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deletion_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer, default=2)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20))
    current_tbl = db.Column(db.String(20), default='Rmvd')

    def to_dict(self):
        return {
            'id': self.id,
            'qr_id': self.qr_id,
            'sl_id': self.sl_id,
            'name' : self.name,
            'TYPE' : self.TYPE,
            'enabled': self.enabled,
            'owner': self.owner,
            'identifier': self.identifier,
            'origin': self.origin,
            'creation_date': self.creation_date,
            'modification_date': self.modification_date,
            'deletion_date' : self.deletion_date,
            'status': self.status,
            'count': self.count,
            'comment': self.comment,
            'previous_tbl': self.previous_tbl,
            'current_tbl': self.current_tbl
        }

#Track history of the seculeague use case
class History(db.Model):
    __tablename__ = 'History'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qr_id = db.Column(db.String(100))         #Note: This must be verified and the sl_id and the name vars default
    sl_id = db.Column(db.String(100))
    name = db.Column(db.String(200))
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modification_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deletion_date = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer, default=2)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20))
    current_tbl = db.Column(db.String(20), default='History')
    
    def to_dict(self):
        return {
            'id': self.id,
            'qr_id': self.qr_id,
            'sl_id': self.sl_id,
            'name' : self.name,
            'TYPE' : self.TYPE,
            'enabled': self.enabled,
            'owner': self.owner,
            'identifier': self.identifier,
            'origin': self.origin,
            'creation_date': self.creation_date,
            'modification_date': self.modification_date,
            'deletion_date': self.deletion_date, 
            'status': self.status,
            'count': self.count,
            'comment': self.comment,
            'previous_tbl': self.previous_tbl,
            'current_tbl': self.current_tbl
        }

