from main import db
from datetime import date

class User(db.Model):  #notice that our class extends db.Model
    __tablename__= 'userregister'#this is the name we want the table in database to have.
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    surnname = db.Column(db.String(20), unique=False, nullable=False)
    dateofbirth = db.Column(db.Date, unique=False, nullable=True)
    residentialaddress = db.Column(db.String(50), unique=True, nullable=False)
    nationality = db.Column(db.String(100), unique=False, nullable=False)
    nationalidentificationnumber = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<User {}>'.format(self.id)