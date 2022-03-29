from app.models import db


class FlowExperiment(db.Model):
    __tablename__ = 'flow_experiment'
    id = db.Column(db.Integer, index=True, primary_key=True)
    experiment_name = db.Column(db.String(128), index=True, unique=True)
    materials = db.Column(db.String(128), index=True)
    experiment_introduction = db.Column(db.String(128))
    # working_condition
    text_description = db.Column(db.String(128))
    image_description = db.Column(db.String(128))
    # result
    measured_velocity = db.Column(db.String(128))
    measured_pressure = db.Column(db.String(128))
    calculated_coefficients = db.Column(db.String(128))