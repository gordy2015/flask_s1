from flask_sqlalchemy import SQLAlchemy
import datetime
# from exts import db

db = SQLAlchemy()

# appoint_ser = db.Table('appoint_ser',db.Column('st_id',db.Integer,db.ForeignKey('service_type.id'),primary_key=True),
#                        db.Column('appoint_id',db.Integer,db.ForeignKey('appointment.id'),primary_key=True))

#
class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user = db.Column(db.String(64),nullable=False)
    phone = db.Column(db.String(64),nullable=False)
    address = db.Column(db.String(64),nullable=False)
    note = db.Column(db.String(64))
    appoint_num = db.Column(db.Integer)
    appoint_date = db.Column(db.String(64), default=datetime.date.today())
    #一对多
    pt_id = db.Column(db.Integer,db.ForeignKey('ptime.id'))
    pt_appoint = db.relationship('Ptime',backref=db.backref('pta'))
    # 多对多
    # st_appoint = db.relationship('Service_type', secondary=appoint_ser, backref=db.backref('sta'))


class Ptime(db.Model):
    __tablename__ = 'ptime'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_time = db.Column(db.String(12))


class Service_type(db.Model):
    __tablename__ = 'service_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))


class Appoint_ser(db.Model):
    __tablename__ = 'appoint_ser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    st_id = db.Column(db.Integer, db.ForeignKey('service_type.id'))
    st_a = db.relationship('Service_type', backref=db.backref('sta'))
    appoint_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    ap_a = db.relationship('Appointment', backref=db.backref('apa'))
    appoint_num = db.Column(db.Integer)