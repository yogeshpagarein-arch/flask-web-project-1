# models.py

from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy import fields


class Person(db.Model):
    __tablename__ = "person"
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    notes = db.relationship(
        "Note",
        backref="person",#To get Parant information
        cascade="all, delete, delete-orphan",#Note cant exists without Person
        single_parent=True,#Only One Person
        order_by="desc(Note.timestamp)"
    )

class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.person_id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = True

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True
    notes = fields.Nested(NoteSchema, many=True)


person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
note_schema = NoteSchema()
