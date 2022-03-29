import os

from flask import Blueprint, request, jsonify, redirect, render_template, url_for

from app.const import SAVE_POSITION
from app.models import db
from app.models.flow_experiment import FlowExperiment


flow_experiment_bp = Blueprint("flow_experiment_bp", __name__)

@flow_experiment_bp.route('/flow_show', methods=['GET', 'POST'])
def flow_show():
    if request.method == 'GET':
        query_table = FlowExperiment.query.all()
        res = []
        one_piece = {}
        for i in range(len(query_table)):
            one_piece["experiment_name"] = query_table[i].experiment_name
            one_piece["materials"] = query_table[i].materials
            res.append(one_piece)
            one_piece.clear()
        ress = jsonify(res)
    return ress


@flow_experiment_bp.route('/flow_detail/<experiment_name>', methods=['GET', 'POST'])
def flow_detail(experiment_name):
    if request.method == 'GET':
        experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
        introduction = experiment.experiment_introduction
        material = experiment.materials
        return render_template('flow_detail.html', name=experiment_name, introduction=introduction, material=material)


@flow_experiment_bp.route('/flow_add', methods=['GET', 'POST'])
def flow_add():
    if request.method == 'POST':
        experiment_name = request.form.get('experiment_name')
        materials = request.form.get('materials')
        experiment_introduction = request.form.get('experiment_introduction')
        flow_experiment = FlowExperiment(experiment_name=experiment_name, materials=materials, experiment_introduction=experiment_introduction)
        db.session.add(flow_experiment)
        db.session.commit()
        return redirect(url_for('flow_working_condition_add', experiment_name=experiment_name))
    return render_template('flow_add.html')


@flow_experiment_bp.route('/flow_modify/<experiment_name>', methods=['GET', 'POST'])
def flow_modify(experiment_name):
    flow_experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name)
    if request.method == 'POST':
        flow_experiment.experiment_name = request.form.get('experiment_name')
        flow_experiment.materials = request.form.get('materials')
        flow_experiment.experiment_introduction = request.form.get('experiment_introduction')
        db.session.commit()
        return redirect(url_for('flow_show'))
    return render_template('flow_modify.html', flow_experiment=flow_experiment)


@flow_experiment_bp.route('/flow_working_condition/<experiment_name>', methods=['GET', 'POST'])
def flow_working_condition(experiment_name):
    query_table = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
    return render_template('flow_working_condition.html', query_table=query_table)


@flow_experiment_bp.route('/flow_working_condition_add/<experiment_name>', methods=['GET', 'POST'])
def flow_working_condition_add(experiment_name):
    flow_experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == 'POST':
        text_description = request.form.get('text_description')
        image_description = acquire_files('image_description')
        f = image_description
        f.save(os.path.join(SAVE_POSITION, f.filename))
        flow_experiment.text_description = text_description
        flow_experiment.image_description = os.path.join(SAVE_POSITION, f.filename)
        db.session.commit()
        return redirect(url_for('flow_result_add', experiment_name=experiment_name))
    return render_template('flow_working_condition_add.html')


@flow_experiment_bp.route('/flow_working_condition_modify/<experiment_name>', methods=['GET', 'POST'])
def flow_working_condition_modify(experiment_name):
    flow_experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == 'POST':
        text_description = request.form.get('text_description')
        image_description = acquire_files('image_description')
        os.remove(flow_experiment.image_description)
        image_description.save(os.path.join(SAVE_POSITION, image_description.filename))
        flow_experiment.text_description = text_description
        flow_experiment.image_description = image_description
        db.session.commit()
        return redirect(url_for('flow_show'))
    return render_template('flow_working_condition_add.html', flow_experiment=flow_experiment)


@flow_experiment_bp.route('/flow_result/<experiment_name>', methods=['GET', 'POST'])
def flow_result(experiment_name):
    query_table = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
    return render_template('flow_result.html', query_table=query_table)


@flow_experiment_bp.route('/flow_result_add/<experiment_name>', methods=['GET', 'POST'])
def flow_result_add(experiment_name):
    if request.method == 'POST':
        flow_experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
        measured_velocity = request.form.get('measured_velocity')
        measured_pressure = request.form.get('measured_pressure')
        calculated_coefficients = acquire_files('calculated_coefficients')
        calculated_coefficients.save(os.path.join(SAVE_POSITION, calculated_coefficients.filename))
        flow_experiment.measured_velocity = measured_velocity
        flow_experiment.measured_pressure = measured_pressure
        flow_experiment.calculated_coefficients = os.path.join(SAVE_POSITION, calculated_coefficients.filename)
        db.session.commit()
        return redirect(url_for('flow_show'))
    return render_template('flow_result_add.html')


@flow_experiment_bp.route('/flow_result_modify/<experiment_name>', methods=['GET', 'POST'])
def flow_result_modify(experiment_name):
    flow_experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == 'POST':
        measured_velocity = request.form.get('measured_velocity')
        measured_pressure = request.form.get('measured_pressure')
        calculated_coefficients = request.form.get('calculated_coefficients')
        os.remove(flow_experiment.calculated_coefficients)
        flow_experiment.measured_velocity = measured_velocity
        flow_experiment.measured_pressure = measured_pressure
        flow_experiment.calculated_coefficients = os.path.join(SAVE_POSITION, calculated_coefficients.filename)
        calculated_coefficients.save(os.path.join(SAVE_POSITION, calculated_coefficients.filename))
        db.session.commit()
        return redirect(url_for('flow_show'))
    return render_template('flow_result_add.html', flow_experiment=flow_experiment)