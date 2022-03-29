from app.models import db


class Metal(db.Model):
    __tablename__ = 'metal'
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(128), index=True)
    introduction = db.Column(db.String(128))
    density = db.Column(db.String(128))
    specific_heat = db.Column(db.String(128))
    thermal_conductivity = db.Column(db.String(128))


class Insulation(db.Model):
    __tablename__ = 'insulation'
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(128), index=True)
    introduction = db.Column(db.String(128))
    classification = db.Column(db.String(128))
    density = db.Column(db.String(128))
    specific_heat = db.Column(db.String(128))
    thermal_conductivity = db.Column(db.String(128))