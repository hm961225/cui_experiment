# coding:utf-8
import json
import os

from app import app
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_cors import cross_origin
from app.models import User, FlowExperiment, CuiExperiment, Metal, Insulation,test
from app import db
from app.utils import file_save, extract_file_name


app.secret = os.urandom(24)
save_local_position = app.root_path + '/static'
save_position = "http://127.0.0.1:7001/static"


@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        res = {
            'username': session['username']
        }
        return jsonify(res)
    else:
        return redirect(url_for('login'))


@app.route('/flow_detail/<experiment_name>', methods=['GET', 'POST'])
def flow_detail(experiment_name):
    if request.method == 'GET':
        experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
        introduction = experiment.experiment_introduction
        material = experiment.materials
        return render_template('flow_detail.html', name=experiment_name, introduction=introduction, material=material)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('index')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            session['username'] = user.username
            flash("登录成功")
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template(('register.html'))


@app.route('/flow_show', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
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


@app.route('/flow_add', methods=['GET', 'POST'])
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


@app.route('/flow_modify/<experiment_name>', methods=['GET', 'POST'])
def flow_modify(experiment_name):
    flow_experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name)
    if request.method == 'POST':
        flow_experiment.experiment_name = request.form.get('experiment_name')
        flow_experiment.materials = request.form.get('materials')
        flow_experiment.experiment_introduction = request.form.get('experiment_introduction')
        db.session.commit()
        return redirect(url_for('flow_show'))
    return render_template('flow_modify.html', flow_experiment=flow_experiment)


@app.route('/flow_working_condition/<experiment_name>', methods=['GET', 'POST'])
def flow_working_condition(experiment_name):
    query_table = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
    return render_template('flow_working_condition.html', query_table=query_table)


@app.route('/flow_working_condition_add/<experiment_name>', methods=['GET', 'POST'])
def flow_working_condition_add(experiment_name):
    flow_experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == 'POST':
        text_description = request.form.get('text_description')
        image_description = request.files.get('image_description')
        f = image_description
        f.save(os.path.join(save_position, f.filename))
        flow_experiment.text_description = text_description
        flow_experiment.image_description = os.path.join(save_position, f.filename)
        db.session.commit()
        return redirect(url_for('flow_result_add', experiment_name=experiment_name))
    return render_template('flow_working_condition_add.html')


@app.route('/flow_working_condition_modify/<experiment_name>', methods=['GET', 'POST'])
def flow_working_condition_modify(experiment_name):
    flow_experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == 'POST':
        text_description = request.form.get('text_description')
        image_description = request.files.get('image_description')
        os.remove(flow_experiment.image_description)
        image_description.save(os.path.join(save_position, image_description.filename))
        flow_experiment.text_description = text_description
        flow_experiment.image_description = image_description
        db.session.commit()
        return redirect(url_for('flow_show'))
    return render_template('flow_working_condition_add.html', flow_experiment=flow_experiment)


@app.route('/flow_result/<experiment_name>', methods=['GET', 'POST'])
def flow_result(experiment_name):
    query_table = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
    return render_template('flow_result.html', query_table=query_table)


@app.route('/flow_result_add/<experiment_name>', methods=['GET', 'POST'])
def flow_result_add(experiment_name):
    if request.method == 'POST':
        flow_experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
        measured_velocity = request.form.get('measured_velocity')
        measured_pressure = request.form.get('measured_pressure')
        calculated_coefficients = request.files.get('calculated_coefficients')
        calculated_coefficients.save(os.path.join(save_position, calculated_coefficients.filename))
        flow_experiment.measured_velocity = measured_velocity
        flow_experiment.measured_pressure = measured_pressure
        flow_experiment.calculated_coefficients = os.path.join(save_position, calculated_coefficients.filename)
        db.session.commit()
        return redirect(url_for('flow_show'))
    return render_template('flow_result_add.html')


@app.route('/flow_result_modify/<experiment_name>', methods=['GET', 'POST'])
def flow_result_modify(experiment_name):
    flow_experiment = FlowExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == 'POST':
        measured_velocity = request.form.get('measured_velocity')
        measured_pressure = request.form.get('measured_pressure')
        calculated_coefficients = request.form.get('calculated_coefficients')
        os.remove(flow_experiment.calculated_coefficients)
        flow_experiment.measured_velocity = measured_velocity
        flow_experiment.measured_pressure = measured_pressure
        flow_experiment.calculated_coefficients = os.path.join(save_position, calculated_coefficients.filename)
        calculated_coefficients.save(os.path.join(save_position, calculated_coefficients.filename))
        db.session.commit()
        return redirect(url_for('flow_show'))
    return render_template('flow_result_add.html', flow_experiment=flow_experiment)


@app.route('/cui_show', methods=['GET', 'POST'])
def cui_show():
    if request.method == 'GET':
        query_table = CuiExperiment.query.all()
        res = []
        one_piece = {}
        for i in range(len(query_table)):
            one_piece["experiment_name"] = query_table[i].experiment_name
            one_piece["classification"] = query_table[i].classification
            one_piece["metal_material"] = query_table[i].metal_material
            one_piece["insulation_material"] = query_table[i].insulation_material
            one_piece["experiment_introduction"] = query_table[i].experiment_introduction
            res.append(one_piece)
            one_piece.clear()
    return jsonify(res)

@app.route('/cui_detail_show/<experiment_name>', methods=['GET', 'POST'])
def cui_detail_show(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    one_piece = {}
    if request.method == "GET":
        one_piece["experiment_name"] = cui_experiment.experiment_name
        one_piece["classification"] = cui_experiment.classification
        one_piece["metal_material"] = cui_experiment.metal_material
        one_piece["insulation_material"] = cui_experiment.insulation_material
        one_piece["experiment_introduction"] = cui_experiment.experiment_introduction
        return jsonify(one_piece)

@app.route('/cui_add', methods=['GET', 'POST'])
def cui_add():
    if request.method == 'POST':
        cui_experiment_json = request.get_data()
        cui_experiment_data = json.loads(cui_experiment_json)
        experiment_name = cui_experiment_data["data"]["experiment_name"]
        classification = cui_experiment_data["data"]["classification"]
        metal_material = cui_experiment_data["data"]["metal_materials"]
        insulation_material = cui_experiment_data["data"]["insulation_materials"]
        experiment_introduction = cui_experiment_data["data"]["experiment_introduction"]
        cui_experiment = CuiExperiment(experiment_name=experiment_name,
                                       classification=classification,
                                       metal_material=metal_material,
                                       insulation_material=insulation_material,
                                       experiment_introduction=experiment_introduction
                                       )
        db.session.add(cui_experiment)
        db.session.commit()

        print(f"cui实验：插入成功")
    return ""


@app.route('/cui_modify/<experiment_name>', methods=['GET', 'POST'])
def cui_modify(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == "GET":
        # 取出数据库信息
        classification = cui_experiment.classification
        metal_material = cui_experiment.metal_material
        insulation = cui_experiment.insulation
        experiment_introduction = cui_experiment.experiment_introduction
        one_piece = {
            "experiment_name": experiment_name,
            "classification": classification,
            "metal_material": metal_material,
            "insulation": insulation,
            "experiment_introduction": experiment_introduction
        }
        return jsonify(one_piece)

    if request.method == "POST":
        # 获取信息
        cui_experiment_json = request.get_data()
        cui_experiment_data = json.loads(cui_experiment_json)
        experiment_name = cui_experiment_data["params"]["data"]["experiment_name"]
        classification = cui_experiment_data["params"]["data"]["classification"]
        metal_material = cui_experiment_data["params"]["data"]["metal_materials"]
        insulation_material = cui_experiment_data["params"]["data"]["insulation_materials"]
        experiment_introduction = cui_experiment_data["params"]["data"]["introduction"]
        # 修改信息
        cui_experiment.classification = classification
        cui_experiment.metal_material = metal_material
        cui_experiment.insulation = insulation_material
        cui_experiment.experiment_introduction = experiment_introduction
        cui_experiment.experiment_name = experiment_name
        db.session.commit()

    print("cui信息修改成功")
    return ""


@app.route("/cui_working_condition_show/<experiment_name>", methods=['GET', "POST"])
def cui_working_condition_show(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    one_piece = {}
    if request.method == "GET":
        one_piece["process_description"] = cui_experiment.process_description
        one_piece["experiment_pic"] = cui_experiment.experiment_pic
        one_piece["pipe_size"] = cui_experiment.pipe_size
        one_piece["insulation"] = cui_experiment.insulation
        one_piece["pipe_temperature"] = cui_experiment.pipe_temperature
        one_piece["sensors_distribution_pic"] = cui_experiment.sensors_distribution_pic
        one_piece["sensors_distribution_table_pic"] = cui_experiment.sensors_distribution_table_pic
        one_piece["environment_temperature_description"] = cui_experiment.environment_temperature_description
        one_piece["environment_temperature_pic"] = cui_experiment.environment_temperature_pic
        one_piece["environment_temperature_file"] = cui_experiment.environment_temperature_file
        one_piece["environment_relative_humidity_description"] = cui_experiment.environment_relative_humidity_description
        one_piece["environment_relative_humidity_pic"] = cui_experiment.environment_relative_humidity_pic
        one_piece["environment_relative_humidity_file"] = cui_experiment.environment_relative_humidity_file
        return jsonify(one_piece)
    return ""

@app.route('/cui_working_condition_add/<experiment_name>', methods=['GET', 'POST'])
def cui_working_condition_add(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == 'POST':
        # 获取数据，如果是文件则保存文件
        process_description = request.form.get("process_description")
        experiment_pic = request.files.get("picture")
        experiment_pic.save(os.path.join(save_position, experiment_pic.filename))
        pipe_size = request.form.get('pipe_size')
        insulation = request.form.get('insulation')
        pipe_temperature = request.form.get('pipe_temperature')
        sensors_distribution_pic = request.files.get('sensors_distribution_pic')
        sensors_distribution_pic.save(os.path.join(save_position, sensors_distribution_pic.filename))
        sensors_distribution_table_pic = request.files.get('sensors_distribution_table_pic')
        sensors_distribution_table_pic.save(os.path.join(save_position, sensors_distribution_table_pic.filename))
        environment_temperature_description = request.form.get('environment_temperature_description')
        environment_temperature_pic = request.files.get('environment_temperature_pic')
        environment_temperature_pic.save(os.path.join(save_position, environment_temperature_pic.filename))
        environment_temperature_file = request.files.get('environment_temperature_file')
        environment_temperature_file.save(os.path.join(save_position, environment_temperature_file.filename))
        environment_relative_humidity_description = request.form.get('environment_relative_humidity_description')
        environment_relative_humidity_pic = request.files.get('environment_relative_humidity_pic')
        environment_relative_humidity_pic.save(os.path.join(save_position, environment_relative_humidity_pic.filename))
        environment_relative_humidity_file = request.files.get('environment_temperature_file')
        environment_relative_humidity_file.save(os.path.join(save_position, environment_relative_humidity_file.filename))
        # 添加信息到数据库
        cui_experiment.process_description = process_description
        cui_experiment.experiment_pic = os.path.join(save_position, experiment_pic.filename)
        cui_experiment.pipe_size = pipe_size
        cui_experiment.insulation = insulation
        cui_experiment.pipe_temperature = pipe_temperature
        cui_experiment.sensors_distribution_pic = os.path.join(save_position, sensors_distribution_pic.filename)
        cui_experiment.sensors_distribution_table_pic = os.path.join(save_position, sensors_distribution_table_pic.filename)
        cui_experiment.environment_temperature_description = environment_temperature_description
        cui_experiment.environment_temperature_pic = os.path.join(save_position, environment_temperature_pic.filename)
        cui_experiment.environment_temperature_file = os.path.join(save_position, environment_temperature_file.filename)
        cui_experiment.environment_relative_humidity_description = environment_relative_humidity_description
        cui_experiment.environment_relative_humidity_pic = os.path.join(save_position, environment_relative_humidity_pic.filename)
        cui_experiment.environment_relative_humidity_file = os.path.join(save_position, environment_relative_humidity_file.filename)
        db.session.commit()
    return ""


@app.route('/cui_working_condition_modify/<experiment_name>', methods=['GET', 'POST'])
def cui_working_condition_modify(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == "GET":
        one_piece = {
            "process_description": cui_experiment.process_description,
            "experiment_pic": cui_experiment.experiment_pic,
            "pipe_size": cui_experiment.pipe_size,
            "insulation": cui_experiment.insulation,
            "pipe_temperature": cui_experiment.pipe_temperature,
            "sensors_distribution_pic": cui_experiment.sensors_distribution_pic,
            "sensors_distribution_table_pic": cui_experiment.sensors_distribution_table_pic,
            "environment_temperature_description": cui_experiment.environment_temperature_description,
            "environment_temperature_pic": cui_experiment.environment_temperature_description,
            "environment_temperature_file": cui_experiment.environment_temperature_file,
            "environment_relative_humidity_description": cui_experiment.environment_relative_humidity_description,
            "environment_relative_humidity_pic": cui_experiment.environment_relative_humidity_pic,
            "environment_relative_humidity_file": cui_experiment.environment_relative_humidity_file
        }
        return jsonify(one_piece)

    if request.method == 'POST':
        # 获取信息
        process_description = request.form.get('process_description')
        experiment_pic = request.files.get('experiment_pic')
        os.remove(cui_experiment.experiment_pic)
        experiment_pic.save(os.path.join(save_position, experiment_pic.filename))
        pipe_size = request.form.get('pipe_size')
        insulation = request.form.get('insulation')
        pipe_temperature = request.form.get('pipe_temperature')
        sensors_distribution_pic = request.files.get('sensors_distribution_pic')
        os.remove(cui_experiment.sensors_distribution_pic)
        sensors_distribution_pic.save(os.path.join(save_position, sensors_distribution_pic.filename))
        sensors_distribution_table_pic = request.files.get('sensors_distribution_table_pic')
        os.remove(cui_experiment.sensors_distribution_table_pic)
        sensors_distribution_table_pic.save(os.path.join(save_position, sensors_distribution_table_pic.filename))
        environment_temperature_description = request.form.get('environment_temperature_description')
        environment_temperature_pic = request.files.get('environment_temperature_pic')
        os.remove(cui_experiment.environment_temperature_pic)
        environment_temperature_pic.save(os.path.join(save_position, environment_temperature_pic.filename))
        environment_temperature_file = request.files.get('environment_temperature_file')
        os.remove(cui_experiment.environment_temperature_file)
        environment_temperature_file.save(os.path.join(save_position, environment_temperature_file.filename))
        environment_relative_humidity_description = request.form.get('environment_relative_humidity_description')
        environment_relative_humidity_pic = request.files.get('environment_relative_humidity_pic')
        os.remove(cui_experiment.environment_relative_humidity_pic)
        environment_relative_humidity_pic.save(os.path.join(save_position, environment_relative_humidity_pic.filename))
        environment_relative_humidity_file = request.files.get('environment_temperature_file')
        os.remove(cui_experiment.environment_relative_humidity_file)
        environment_relative_humidity_file.save(os.path.join(save_position, environment_relative_humidity_file.filename))
        # 修改信息
        cui_experiment.process_description = process_description
        cui_experiment.experiment_pic = os.path.join(save_position, experiment_pic.filename)
        cui_experiment.pipe_size = pipe_size
        cui_experiment.insulation = insulation
        cui_experiment.pipe_temperature = pipe_temperature
        cui_experiment.sensors_distribution_pic = os.path.join(save_position, sensors_distribution_pic.filename)
        cui_experiment.sensors_distribution_table_pic = os.path.join(save_position,
                                                                     sensors_distribution_table_pic.filename)
        cui_experiment.environment_temperature_description = environment_temperature_description
        cui_experiment.environment_temperature_pic = os.path.join(save_position, environment_temperature_pic.filename)
        cui_experiment.environment_temperature_file = os.path.join(save_position, environment_temperature_file.filename)
        cui_experiment.environment_relative_humidity_description = environment_relative_humidity_description
        cui_experiment.environment_relative_humidity_pic = os.path.join(save_position,
                                                                        environment_relative_humidity_pic.filename)
        cui_experiment.environment_relative_humidity_file = os.path.join(save_position,
                                                                         environment_relative_humidity_file.filename)

        print("cui_working_condition信息修改成功")
    return ""


@app.route('/cui_result_show/<experiment_name>', methods=['GET', 'POST'])
def cui_result_show(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == "GET":
        one_piece = {
            "sim_temperature_description": cui_experiment.sim_temperature_description,
            "sim_temperature_pic": cui_experiment.sim_temperature_pic,
            "sim_temperature_file": cui_experiment.sim_temperature_file,
            "sim_humidity_description": cui_experiment.sim_humidity_description,
            "sim_humidity_pic": cui_experiment.sim_humidity_pic,
            "sim_humidity_file": cui_experiment.sim_humidity_file,
            "corrosion_type_description": cui_experiment.corrosion_type_description,
            "corrosion_type_pic1": cui_experiment.corrosion_type_pic1,
            "corrosion_type_pic2": cui_experiment.corrosion_type_pic2,
            "corrosion_position_description": cui_experiment.corrosion_position_description,
            "corrosion_position_pic1": cui_experiment.corrosion_position_pic1,
            "corrosion_position_pic2": cui_experiment.corrosion_position_pic2,
            "corrosion_area_description": cui_experiment.corrosion_area_description,
            "corrosion_area_pic1": cui_experiment.corrosion_area_pic1,
            "corrosion_area_pic2": cui_experiment.corrosion_area_pic2,
            "mass_loss_description": cui_experiment.mass_loss_description,
            "mass_loss_pic1": cui_experiment.mass_loss_pic1,
            "mass_loss_pic2": cui_experiment.mass_loss_pic2,
            "analysis_conclusion_description": cui_experiment.analysis_conclusion_description,
            "analysis_conclusion_pic1": cui_experiment.analysis_conclusion_pic1,
            "analysis_conclusion_pic2": cui_experiment.analysis_conclusion_pic2
        }
        return jsonify(one_piece)
    return ""


@app.route('/cui_result_add/<experiment_name>', methods=['GET', 'POST'])
def cui_result_add(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name)
    if request.method == 'POST':
        # 获取信息
        sim_temperature_description = request.form.get('sim_temperature_description')
        sim_temperature_pic = request.files.get('sim_temperature_pic')
        sim_temperature_pic.save(os.path.join(save_position, sim_temperature_pic.filename))
        sim_temperature_file = request.files.get('sim_temperature_file')
        sim_temperature_file.save(os.path.join(save_position, sim_temperature_file.filename))
        sim_humidity_description = request.form.get('sim_humidity_description')
        sim_humidity_pic = request.files.get('sim_humidity_pic')
        sim_humidity_pic.save(os.path.join(save_position, sim_humidity_pic.filename))
        sim_humidity_file = request.files.get('sim_humidity_file')
        sim_humidity_file.save(os.path.join(save_position, sim_humidity_file.filename))
        corrosion_type_description = request.form.get('corrosion_type_description')
        corrosion_type_pic1 = request.files.get('corrosion_type_pic1')
        corrosion_type_pic1.save(os.path.join(save_position, corrosion_type_pic1.filename))
        corrosion_type_pic2 = request.files.get('corrosion_type_pic2')
        corrosion_type_pic2.save(os.path.join(save_position, corrosion_type_pic2.filename))
        corrosion_position_description = request.form.get('corrosion_position_description')
        corrosion_position_pic1 = request.files.get('corrosion_position_pic1')
        corrosion_position_pic1.save(os.path.join(save_position, corrosion_position_pic1.filename))
        corrosion_position_pic2 = request.files.get('corrosion_position_pic2')
        corrosion_position_pic2.save(os.path.join(save_position, corrosion_position_pic2.filename))
        corrosion_area_description = request.form.get('corrosion_area_description')
        corrosion_area_pic1 = request.files.get('corrosion_area_pic1')
        corrosion_area_pic1.save(os.path.join(save_position, corrosion_area_pic1.filename))
        corrosion_area_pic2 = request.files.get('corrosion_area_pic2')
        corrosion_area_pic2.save(os.path.join(save_position, corrosion_area_pic2.filename))
        mass_loss_description = request.form.get('mass_loss_description')
        mass_loss_pic1 = request.files.get('mass_loss_pic1')
        mass_loss_pic1.save(os.path.join(save_position, mass_loss_pic1.filename))
        mass_loss_pic2 = request.files.get('mass_loss_pic2')
        mass_loss_pic2.save(os.path.join(save_position, mass_loss_pic2.filename))
        analysis_conclusion_description = request.form.get('analysis_conclusion_description')
        analysis_conclusion_pic1 = request.files.get('analysis_conclusion_pic1')
        analysis_conclusion_pic1.save(save_position, analysis_conclusion_pic1.filename)
        analysis_conclusion_pic2 = request.files.get('analysis_conclusion_pic2')
        analysis_conclusion_pic2.save(save_position, analysis_conclusion_pic2.filename)
        # 添加信息
        cui_experiment.sim_temperature_description = sim_temperature_description
        cui_experiment.sim_temperature_pic = os.path.join(save_position, sim_temperature_pic.filename)
        cui_experiment.sim_temperature_file = os.path.join(save_position, sim_temperature_file.filename)
        cui_experiment.sim_humidity_description = sim_humidity_description
        cui_experiment.sim_humidity_pic = os.path.join(save_position, sim_humidity_pic.filename)
        cui_experiment.sim_humidity_file = os.path.join(save_position, sim_humidity_file.filename)
        cui_experiment.corrosion_type_description = corrosion_type_description
        cui_experiment.corrosion_type_pic1 = os.path.join(save_position, corrosion_type_pic1.filename)
        cui_experiment.corrosion_type_pic2 = os.path.join(save_position, corrosion_type_pic2.filename)
        cui_experiment.corrosion_position_description = corrosion_position_description
        cui_experiment.corrosion_area_description = corrosion_area_description
        cui_experiment.corrosion_area_pic1 = os.path.join(save_position, corrosion_area_pic1.filename)
        cui_experiment.corrosion_area_pic2 = os.path.join(save_position, corrosion_area_pic2.filename)
        cui_experiment.mass_loss_description = mass_loss_description
        cui_experiment.mass_loss_pic1 = os.path.join(save_position, mass_loss_pic1.filename)
        cui_experiment.mass_loss_pic2 = os.path.join(save_position, mass_loss_pic2.filename)
        cui_experiment.analysis_conclusion_description = analysis_conclusion_description
        cui_experiment.analysis_conclusion_pic1 = os.path.join(save_position, analysis_conclusion_pic1.filename)
        cui_experiment.analysis_conclusion_pic2 = os.path.join(save_position, analysis_conclusion_pic2.filename)
    print("cui_result添加成功")
    return ""


@app.route('/cui_result_modify/<experiment_name>', methods=['GET', 'POST'])
def cui_result_modify(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name)

    if request.method == "GET":
        one_piece = {
            "sim_temperature_description": cui_experiment.sim_temperature_description,
            "sim_temperature_pic": cui_experiment.sim_temperature_pic,
            "sim_temperature_file": cui_experiment.sim_temperature_file,
            "sim_humidity_description": cui_experiment.sim_humidity_description,
            "sim_humidity_pic": cui_experiment.sim_humidity_pic,
            "sim_humidity_file": cui_experiment.sim_humidity_file,
            "corrosion_type_description": cui_experiment.corrosion_type_description,
            "corrosion_type_pic1": cui_experiment.corrosion_type_pic1,
            "corrosion_type_pic2": cui_experiment.corrosion_type_pic2,
            "corrosion_position_description": cui_experiment.corrosion_position_description,
            "corrosion_position_pic1": cui_experiment.corrosion_position_pic1,
            "corrosion_position_pic2": cui_experiment.corrosion_position_pic2,
            "corrosion_area_description": cui_experiment.corrosion_area_description,
            "corrosion_area_pic1": cui_experiment.corrosion_area_pic1,
            "corrosion_area_pic2": cui_experiment.corrosion_area_pic2,
            "mass_loss_description": cui_experiment.mass_loss_description,
            "mass_loss_pic1": cui_experiment.mass_loss_pic1,
            "mass_loss_pic2": cui_experiment.mass_loss_pic2,
            "analysis_conclusion_description": cui_experiment.analysis_conclusion_description,
            "analysis_conclusion_pic1": cui_experiment.analysis_conclusion_pic1,
            "analysis_conclusion_pic2": cui_experiment.analysis_conclusion_pic2
        }
        return jsonify(one_piece)

    if request.method == "POST":
        # 获取信息
        sim_temperature_description = request.form.get('sim_temperature_description')
        sim_temperature_pic = request.files.get('sim_temperature_pic')
        os.remove(cui_experiment.sim_temperature_pic)
        sim_temperature_pic.save(os.path.join(save_position, sim_temperature_pic.filename))
        sim_temperature_file = request.files.get('sim_temperature_file')
        os.remove(cui_experiment.sim_temperature_file)
        sim_temperature_file.save(os.path.join(save_position, sim_temperature_file.filename))
        sim_humidity_description = request.form.get('sim_humidity_description')
        sim_humidity_pic = request.files.get('sim_humidity_pic')
        os.remove(cui_experiment.sim_humidity_pic)
        sim_humidity_pic.save(os.path.join(save_position, sim_humidity_pic.filename))
        sim_humidity_file = request.files.get('sim_humidity_file')
        os.remove(cui_experiment.sim_humidity_file)
        sim_humidity_file.save(os.path.join(save_position, sim_humidity_file.filename))
        corrosion_type_description = request.form.get('corrosion_type_description')
        corrosion_type_pic1 = request.files.get('corrosion_type_pic1')
        os.remove(cui_experiment.corrosion_type_pic1)
        corrosion_type_pic1.save(os.path.join(save_position, corrosion_type_pic1.filename))
        corrosion_type_pic2 = request.files.get('corrosion_type_pic2')
        os.remove(cui_experiment.corrosion_type_pic2)
        corrosion_type_pic2.save(os.path.join(save_position, corrosion_type_pic2.filename))
        corrosion_position_description = request.form.get('corrosion_position_description')
        corrosion_position_pic1 = request.files.get('corrosion_position_pic1')
        os.remove(cui_experiment.corrosion_position_pic1)
        corrosion_position_pic1.save(os.path.join(save_position, corrosion_position_pic1.filename))
        corrosion_position_pic2 = request.files.get('corrosion_position_pic2')
        os.remove(cui_experiment.corrosion_position_pic2)
        corrosion_position_pic2.save(os.path.join(save_position, corrosion_position_pic2.filename))
        corrosion_area_description = request.form.get('corrosion_area_description')
        corrosion_area_pic1 = request.files.get('corrosion_area_pic1')
        os.remove(cui_experiment.corrosion_area_pic1)
        corrosion_area_pic1.save(os.path.join(save_position, corrosion_area_pic1.filename))
        corrosion_area_pic2 = request.files.get('corrosion_area_pic2')
        os.remove(cui_experiment.corrosion_area_pic2)
        corrosion_area_pic2.save(os.path.join(save_position, corrosion_area_pic2.filename))
        mass_loss_description = request.form.get('mass_loss_description')
        mass_loss_pic1 = request.files.get('mass_loss_pic1')
        os.remove(cui_experiment.mass_loss_pic1)
        mass_loss_pic1.save(os.path.join(save_position, mass_loss_pic1.filename))
        mass_loss_pic2 = request.files.get('mass_loss_pic2')
        os.remove(cui_experiment.mass_loss_pic2)
        mass_loss_pic2.save(os.path.join(save_position, mass_loss_pic2.filename))
        analysis_conclusion_description = request.form.get('analysis_conclusion_description')
        analysis_conclusion_pic1 = request.files.get('analysis_conclusion_pic1')
        os.remove(cui_experiment.analysis_conclusion_pic1)
        analysis_conclusion_pic1.save(save_position, analysis_conclusion_pic1.filename)
        analysis_conclusion_pic2 = request.files.get('analysis_conclusion_pic2')
        os.remove(cui_experiment.analysis_conclusion_pic2)
        analysis_conclusion_pic2.save(save_position, analysis_conclusion_pic2.filename)
        # 添加信息
        cui_experiment.sim_temperature_description = sim_temperature_description
        cui_experiment.sim_temperature_pic = os.path.join(save_position, sim_temperature_pic.filename)
        cui_experiment.sim_temperature_file = os.path.join(save_position, sim_temperature_file.filename)
        cui_experiment.sim_humidity_description = sim_humidity_description
        cui_experiment.sim_humidity_pic = os.path.join(save_position, sim_humidity_pic.filename)
        cui_experiment.sim_humidity_file = os.path.join(save_position, sim_humidity_file.filename)
        cui_experiment.corrosion_type_description = corrosion_type_description
        cui_experiment.corrosion_type_pic1 = os.path.join(save_position, corrosion_type_pic1.filename)
        cui_experiment.corrosion_type_pic2 = os.path.join(save_position, corrosion_type_pic2.filename)
        cui_experiment.corrosion_position_description = corrosion_position_description
        cui_experiment.corrosion_area_description = corrosion_area_description
        cui_experiment.corrosion_area_pic1 = os.path.join(save_position, corrosion_area_pic1.filename)
        cui_experiment.corrosion_area_pic2 = os.path.join(save_position, corrosion_area_pic2.filename)
        cui_experiment.mass_loss_description = mass_loss_description
        cui_experiment.mass_loss_pic1 = os.path.join(save_position, mass_loss_pic1.filename)
        cui_experiment.mass_loss_pic2 = os.path.join(save_position, mass_loss_pic2.filename)
        cui_experiment.analysis_conclusion_description = analysis_conclusion_description
        cui_experiment.analysis_conclusion_pic1 = os.path.join(save_position, analysis_conclusion_pic1.filename)
        cui_experiment.analysis_conclusion_pic2 = os.path.join(save_position, analysis_conclusion_pic2.filename)
        print("cui_result信息修改成功")
    return ""

@app.route('/cui_delete/<experiment_name>', methods=['GET', 'POST'])
def cui_delete(experiment_name):
    if request.method == "GET":
        db.session.delete(experiment_name)
        db.session.commit()
    return ""
@app.route('/metal_show', methods=['GET', 'POST'])
def metal_show():
    all_metal = Metal.query.all()
    res = []
    one_piece = {}
    if request.method == "GET":
        for item in all_metal:
            one_piece["name"] = item.name
            one_piece["introduction"] = item.introduction
            one_piece["density"] = item.density
            one_piece["specific_heat"] = item.specific_heat
            one_piece["thermal_conductivity"] = item.thermal_conductivity
            res.append(one_piece)
        return jsonify(res)

@app.route('/metal_add', methods=['GET', 'POST'])
def metal_add():
    if request.method == 'POST':
        name = request.form.get("name")
        introduction = request.form.get("introduction")
        density = request.form.get("density")
        specific_heat = request.form.get("specific_heat")
        thermal_conductivity = request.form.get("thermal_conductivity")

        one_piece = Metal(
            name=name,
            introduction = introduction,
            density = density,
            specific_heat = specific_heat,
            thermal_conductivity = thermal_conductivity
        )
        db.session.add(one_piece)
        db.session.commit()
        print("添加成功")

@app.route('/metal_modify/<metal_name>', methods=['GET', 'POST'])
def metal_modify(metal_name):
    one_metal = Metal.query.filter_by(name=metal_name)
    if request.method == "GET":
        name = one_metal.name
        introduction = one_metal.introduction
        density = one_metal.density
        specific_heat = one_metal.specific_heat
        thermal_conductivity = one_metal.thermal_conductivity
        one_piece = {
            "name": name,
            "introduction": introduction,
            "density": density,
            "specific_heat": specific_heat,
            "thermal_conductivity": thermal_conductivity
        }
        return jsonify(one_piece)
    if request.method == "POST":
        one_metal.name = request.form.get("name")
        one_metal.introduction = request.form.get("introduction")
        one_metal.density = request.form.get("density")
        one_metal.specific_heat = request.form.get("specific_heat")
        one_metal.thermal_conductivity = request.form.get("thermal_conductivity")


@app.route('/test', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def test():
    # username  = request.form.get('username')
    # a = 321
    # b = 0
    # res = {
    #     "weq": a,
    #     "dsa": b
    # }

    # 返回图片流
    # image = open('/Users/heming/Desktop/test.jpg', 'rb').read()
    # image_stream = base64.b64encode(image)

    # 接收图片流
    # byte_stream = io.BytesIO(image_stream)  # byte_stream是图片对象

    # 接收
    #data = json.load(request.form.get('data'))
    #print(data)
    if request.method == "POST":
        print("收到请求")
        #a = request.get_data()
        #print(a)
        # b = json.loads(a)
        #c = request.form.get("name")
        #b = request.form.get("age")
        # b = request.files.get("file")
        #file = request.files.get("files")
        file = request.files.getlist("files")
        print("请求数据")
        print("-----------")
        print(file)
        #print(file[0])
        a = file[0]
        print(a.filename)
        print("-------")
        # print(a)
        # print(type(a))

        # 此处的数量可以为数据库对应的id
        # with open("/static/file1") as f:
        #     f.write(a)
        #byte_stream = io.BytesIO(a)
        # with open(os.path.join(save_position, "test"), 'wb') as f:
        #     f.save(os.path.join(save_position, "test", 'wb'))

        #byte_stream = io.BytesIO(a)
        #_dict = json.loads(a)
        #print(_dict)
        return "ewqq"

    if request.method == "GET":
        print("收到请求")
        a = request.get_data()
        # pic_info = [
        #     "http://192.168.43.204:7001/static/test.jpg",
        #     "http://192.168.43.204:7001/static/test.jpg"
        # ]
        pic_info = [
            "http://127.0.0.1:7001/static/test.jpg",
            "http://127.0.0.1:7001/static/test1.jpg"
        ]
        pic = "http://10.2.153.129:7001/static/test.jpg"
        pic_info = json.dumps(pic_info)
        print(request.files.getlist("dsa"))
        print(request.files.getlist("dsa") == [])
        #os.remove(os.path.join(save_local_position, "test.jpg"))
        # add_info = Metal(name=name, density=pic_info)
        # db.session.add(add_info)
        # db.session.commit()
        # metal_query = Metal.query.filter_by(name="test_name").first()
        # print(metal_query)
        # metal_json = metal_query.density
        # print(json.loads(metal_json))
        # pic = json.loads(metal_json)
        # print(pic["pic1"])



        # image = open('/Users/heming/Desktop/test.jpg', 'rb').read()
        # image_stream = base64.b64encode(image)
        # (传name)

        return pic_info

@app.route('/test_add', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def test_add():
    if request.method == "POST":
        print(request.form)
        print(request.files)
        name = request.form.get("name")
        print(name)
        request.files.get("")
        return ""

@app.route('/test_index', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def test_index():
    f = open('/Users/heming/Desktop/test.go')
    text = f.read()
    print(text)
    request.get_data()
    return render_template("index.html", test_res=text)