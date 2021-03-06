from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, text, Boolean, CHAR
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# class User(db.Model):
#     """Data model for user accounts."""
#
#     __tablename__ = 'flasksqlalchemy-users'
#     id = db.Column(db.Integer,
#                    primary_key=True)
#     username = db.Column(db.String(64),
#                          index=False,
#                          unique=True,
#                          nullable=False)
#     email = db.Column(db.String(80),
#                       index=True,
#                       unique=True,
#                       nullable=False)
#     created = db.Column(db.DateTime,
#                         index=False,
#                         unique=False,
#                         nullable=False)
#     bio = db.Column(db.Text,
#                     index=False,
#                     unique=False,
#                     nullable=True)
#     admin = db.Column(db.Boolean,
#                       index=False,
#                       unique=False,
#                       nullable=False)
#
#     def __repr__(self):
#         return '<User {}>'.format(self.username)


class LineType(db.Model):
    __tablename__ = 'line_types'

    id = Column(BigInteger, primary_key=True)
    line_type = Column(String(50), nullable=False)


class Line(db.Model):
    __tablename__ = 'lines'

    id = Column(BigInteger, primary_key=True)
    line_name = Column(String(50), nullable=False)
    id_line_type = Column(Integer, nullable=False)

    # direction = relationship('LineDirection', backref='Line')


class Stop(db.Model):
    __tablename__ = 'stops'

    id = Column(Integer, primary_key=True, server_default=text("nextval('stops_id_seq'::regclass)"))
    stop_name = Column(String(50), nullable=False)
    zone = Column(BigInteger, nullable=False)
    lat = Column(Numeric(9, 6))
    long = Column(Numeric(9, 6))
    alternative_name = Column(String(50))


class Test(db.Model):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, server_default=text("nextval('test_id_seq'::regclass)"))
    created_at = Column(DateTime)


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, nullable=False)
    id_user = Column(Text, primary_key=True)
    onboarding_type = Column(Integer)
    os_type = Column(Text)
    created_at = Column(DateTime)


class Users(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, server_default=text("nextval('users_id_seq'::regclass)"))
    id_user = Column(String(50), primary_key=True)
    onboarding_type = Column(String(10), nullable=False)
    os_type = Column(String(50), nullable=False)
    created_at = Column(Date, nullable=False)


class LineDirection(db.Model):
    __tablename__ = 'line_directions'

    id = Column(BigInteger, primary_key=True)
    id_line = Column(ForeignKey('lines.id'), nullable=False)
    id_stop = Column(ForeignKey('stops.id'), nullable=False)


    line = relationship('Line', backref='directions')
    stop = relationship('Stop', backref='stop_directions')


class Platform(db.Model):
    __tablename__ = 'platforms'

    id = Column(BigInteger, primary_key=True)
    id_stop = Column(ForeignKey('stops.id'), nullable=False)
    platform_name = Column(String(50), nullable=False)
    lat = Column(Numeric(9, 6), nullable=False)
    long = Column(Numeric(9, 6), nullable=False)
    accesibility = Column(String(50))
    valid_from = Column(Date)
    valid_to = Column(Date)

    stop = relationship('Stop', backref="stop_platforms")


class LinePlatform(db.Model):
    __tablename__ = 'line_platforms'

    id = Column(BigInteger, primary_key=True)
    id_direction = Column(ForeignKey('line_directions.id'), nullable=False)
    id_platform = Column(ForeignKey('platforms.id'), nullable=False)
    time_span = Column(Integer, nullable=False)
    platform_order = Column(Integer, nullable=False)
    request_stop = Column(Boolean)

    line_direction = relationship('LineDirection', backref='platforms')
    platform = relationship('Platform', backref="line_platforms")


class Timetable(db.Model):
    __tablename__ = 'timetable'

    id = Column(BigInteger, primary_key=True)
    id_platform = Column(ForeignKey('platforms.id'), nullable=False)
    id_line = Column(ForeignKey('lines.id'), nullable=False)
    id_direction = Column(ForeignKey('line_directions.id'), nullable=False)
    departure_hour = Column(BigInteger, nullable=False)
    departure_minute = Column(BigInteger)
    type = Column(ForeignKey('timetable_type.indication'), nullable=False)
    low_rise = Column('low-rise', Boolean, nullable=False)
    request_stop = Column(Boolean)
    special_type = Column(CHAR(1))

    line_direction = relationship('LineDirection')
    line = relationship('Line')
    platform = relationship('Platform')
    timetable_type = relationship('TimetableType')


class TimetableType(db.Model):
    __tablename__ = 'timetable_type'

    indication = Column(BigInteger, primary_key=True)
    description = Column(String(100), nullable=False)

class Calendar(db.Model):
    __tablename__ = 'calendar'

    id = Column(BigInteger, primary_key=True)
    type = Column(BigInteger, nullable=False)
    time_from = Column(BigInteger, nullable=False)
    time_to = Column(BigInteger, nullable=False)