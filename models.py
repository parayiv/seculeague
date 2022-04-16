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
    id = db.Column(db.Integer, primary_key=True)
    qr_id = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
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
            'enabled': self.enabled,
            'owner': self.owner,
            'identifier': self.identifier,
            'origin': self.origin,
            'creation_date': self.creation_date,
            'modification_date': self.modification_date       
        }

#track all seculeague use cases: Added/removed/to be commited/
class seculeague(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    qr_id = db.Column(db.Integer)
    sl_id = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100))
    modification_date = db.Column(db.String(100))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20))
    current_tbl = db.Column(db.String(20))
    
    def __init__(self, id, qr_id, sl_id, name, TYPE, enabled, owner, identifier, origin, creation_date, modification_date, status, count, comment, previous_tbl, current_tbl):
        self.id = id
        self.qr_id = qr_id
        self.sl_id = sl_id
        self.name = name
        self.TYPE = TYPE
        self.enabled = enabled
        self.owner = owner
        self.identifier = identifier
        self.origin = origin
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.status = status
        self.count = count
        self.comment = comment
        self.previous_tbl = previous_tbl
        self.current_tbl = self.current_tbl

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
class news(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    qr_id = db.Column(db.Integer)
    sl_id = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100))
    modification_date = db.Column(db.String(100))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20))
    current_tbl = db.Column(db.String(20))
    
    def __init__(self, id, qr_id, sl_id, name, TYPE, enabled, owner, identifier, origin, creation_date, modification_date, status, count, comment, previous_tbl, current_tbl):
        self.id = id
        self.qr_id = qr_id
        self.sl_id = sl_id
        self.name = name
        self.TYPE = TYPE
        self.enabled = enabled
        self.owner = owner
        self.identifier = identifier
        self.origin = origin
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.status = status
        self.count = count
        self.comment = comment
        self.previous_tbl = previous_tbl
        self.current_tbl = self.current_tbl

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
class qr_minus_sl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr_id = db.Column(db.Integer)
    sl_id = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100))
    modification_date = db.Column(db.String(100))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20))
    current_tbl = db.Column(db.String(20))
    
    def __init__(self, id, qr_id, sl_id, name, TYPE, enabled, owner, identifier, origin, creation_date, modification_date, status, count, comment, previous_tbl, current_tbl):
        self.id = id
        self.qr_id = qr_id
        self.sl_id = sl_id
        self.name = name
        self.TYPE = TYPE
        self.enabled = enabled
        self.owner = owner
        self.identifier = identifier
        self.origin = origin
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.status = status
        self.count = count
        self.comment = comment
        self.previous_tbl = previous_tbl
        self.current_tbl = self.current_tbl

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
class sl_minus_qr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr_id = db.Column(db.Integer)
    sl_id = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100))
    modification_date = db.Column(db.String(100))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20))
    current_tbl = db.Column(db.String(20))
    
    def __init__(self, id, qr_id, sl_id, name, TYPE, enabled, owner, identifier, origin, creation_date, modification_date, status, count, comment, previous_tbl, current_tbl):
        self.id = id
        self.qr_id = qr_id
        self.sl_id = sl_id
        self.name = name
        self.TYPE = TYPE
        self.enabled = enabled
        self.owner = owner
        self.identifier = identifier
        self.origin = origin
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.status = status
        self.count = count
        self.comment = comment
        self.previous_tbl = previous_tbl
        self.current_tbl = self.current_tbl

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
class rmvd(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    qr_id = db.Column(db.Integer)
    sl_id = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100))
    modification_date = db.Column(db.String(100))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20))
    current_tbl = db.Column(db.String(20))
    
    def __init__(self, id, qr_id, sl_id, name, TYPE, enabled, owner, identifier, origin, creation_date, modification_date, status, count, comment, previous_tbl, current_tbl):
        self.id = id
        self.qr_id = qr_id
        self.sl_id = sl_id
        self.name = name
        self.TYPE = TYPE
        self.enabled = enabled
        self.owner = owner
        self.identifier = identifier
        self.origin = origin
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.status = status
        self.count = count
        self.comment = comment
        self.previous_tbl = previous_tbl
        self.current_tbl = self.current_tbl

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

#Track history of the seculeague use case
class history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr_id = db.Column(db.Integer)
    sl_id = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
    TYPE = db.Column(db.String(10))
    enabled = db.Column(db.String(20))
    owner = db.Column(db.String(50))
    identifier = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    creation_date = db.Column(db.String(100))
    modification_date = db.Column(db.String(100))
    status = db.Column(db.String(20))
    count = db.Column(db.Integer)
    comment = db.Column(db.String(100))
    previous_tbl = db.Column(db.String(20))
    current_tbl = db.Column(db.String(20))
    
    def __init__(self, id, qr_id, sl_id, name, TYPE, enabled, owner, identifier, origin, creation_date, modification_date, status, count, comment, previous_tbl, current_tbl):
        self.id = id
        self.qr_id = qr_id
        self.sl_id = sl_id
        self.name = name
        self.TYPE = TYPE
        self.enabled = enabled
        self.owner = owner
        self.identifier = identifier
        self.origin = origin
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.status = status
        self.count = count
        self.comment = comment
        self.previous_tbl = previous_tbl
        self.current_tbl = self.current_tbl

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

