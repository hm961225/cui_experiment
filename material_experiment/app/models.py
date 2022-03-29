# coding:utf-8
from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))


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


class CuiExperiment(db.Model):
    __tablename__ = 'cui_experiment'
    id = db.Column(db.Integer, index=True, primary_key=True)
    experiment_name = db.Column(db.String(128), index=True, unique=True)
    classification = db.Column(db.String(128))
    metal_material = db.Column(db.String(128))
    insulation_material = db.Column(db.String(128))
    experiment_introduction = db.Column(db.String(128))
    # working condition
    process_description = db.Column(db.String(128))
    experiment_pic = db.Column(db.String(128))
    pipe_size = db.Column(db.String(128))
    insulation = db.Column(db.String(128))
    pipe_temperature = db.Column(db.String(128))
    sensors_distribution_pic = db.Column(db.String(128))
    sensors_distribution_table_pic = db.Column(db.String(128))
    environment_temperature_description = db.Column(db.String(128))
    environment_temperature_pic = db.Column(db.String(128))
    environment_temperature_file = db.Column(db.String(128))
    environment_relative_humidity_description = db.Column(db.String(128))
    environment_relative_humidity_pic = db.Column(db.String(128))
    environment_relative_humidity_file = db.Column(db.String(128))
    # result
    sim_temperature_description = db.Column(db.String(128))
    sim_temperature_pic = db.Column(db.String(128))
    sim_temperature_file = db.Column(db.String(128))
    sim_humidity_description = db.Column(db.String(128))
    sim_humidity_pic = db.Column(db.String(128))
    sim_humidity_file = db.Column(db.String(128))
    corrosion_type_description = db.Column(db.String(128))
    corrosion_type_pic1 = db.Column(db.String(128))
    corrosion_type_pic2 = db.Column(db.String(128))
    corrosion_position_description = db.Column(db.String(128))
    corrosion_position_pic1 = db.Column(db.String(128))
    corrosion_position_pic2 = db.Column(db.String(128))
    corrosion_area_description = db.Column(db.String(128))
    corrosion_area_pic1 = db.Column(db.String(128))
    corrosion_area_pic2 = db.Column(db.String(128))
    mass_loss_description = db.Column(db.String(128))
    mass_loss_pic1 = db.Column(db.String(128))
    mass_loss_pic2 = db.Column(db.String(128))
    analysis_conclusion_description = db.Column(db.String(128))
    analysis_conclusion_pic1 = db.Column(db.String(128))
    analysis_conclusion_pic2 = db.Column(db.String(128))


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

class test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(128), index=True)






