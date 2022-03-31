import os.path

from flask import Blueprint, request, jsonify, json

from app.models import db
from app.models.cui_experiment import CuiExperiment
from app.utils.filename_to_url import filename_to_url
from app.utils.file_save_to_sql import file_save_to_sql
from app.utils import files_remove
from app.utils.excel_data_extract import extract_all_data, extract_x_y_z_data, extract_data_without_name, extract_mass_piece_data, extract_data_from_name, extract_ambient_data, extract_sensors_data
from app.utils.acquire_files import acquire_files
from app.const import SAVE_POSITION, SAVE_LOCAL_POSITION


cui_experiment_bp = Blueprint("cui_experiment_bp", __name__)


@cui_experiment_bp.route('/cui_show', methods=['GET', 'POST'])
def cui_show():
    res = []
    if request.method == 'GET':
        query_table = CuiExperiment.query.all()
        one_piece = {}
        for i in range(len(query_table)):
            one_piece["experiment_name"] = query_table[i].experiment_name
            one_piece["classification"] = query_table[i].classification
            one_piece["metal_material"] = query_table[i].metal_material
            one_piece["insulation_material"] = query_table[i].insulation_material
            one_piece["experimenters"] = query_table[i].experimenters
            one_piece["remarks"] = query_table[i].remarks
            one_piece["date"] = query_table[i].date
            res.append(one_piece)
            one_piece = {}
    res_table_data = {"tableData": res}
    return jsonify(res_table_data)


@cui_experiment_bp.route('/cui_detail_show/<experiment_name>', methods=['GET', 'POST'])
def cui_detail_show(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    one_piece = {}
    if request.method == "GET":
        one_piece["experiment_name"] = cui_experiment.experiment_name
        one_piece["classification"] = cui_experiment.classification
        one_piece["metal_material"] = cui_experiment.metal_material
        one_piece["insulation_material"] = cui_experiment.insulation_material
        one_piece["experimenters"] = cui_experiment.experimenters
        one_piece["remarks"] = cui_experiment.remarks
        one_piece["date"] = cui_experiment.date
        return jsonify(one_piece)


@cui_experiment_bp.route('/cui_add', methods=['GET', 'POST'])
def cui_add():
    if request.method == 'POST':
        cui_experiment_json = request.get_data()
        cui_experiment_data = json.loads(cui_experiment_json)
        experiment_name = cui_experiment_data["data"]["experiment_name"]
        classification = cui_experiment_data["data"]["classification"]
        metal_material = cui_experiment_data["data"]["metal_materials"]
        insulation_material = cui_experiment_data["data"]["insulation_materials"]
        experimenters = cui_experiment_data["data"]["experimenters"]
        remarks = cui_experiment_data["data"]["remarks"]
        date = cui_experiment_data["data"]["date"]
        cui_experiment = CuiExperiment(experiment_name=experiment_name,
                                       classification=classification,
                                       metal_material=metal_material,
                                       insulation_material=insulation_material,
                                       experimenters=experimenters,
                                       remarks=remarks,
                                       date=date,
                                       )
        db.session.add(cui_experiment)
        db.session.commit()

        print(f"{experiment_name}cui实验：插入成功")
    return ""


@cui_experiment_bp.route('/cui_modify/<experiment_name>', methods=['GET', 'POST'])
def cui_modify(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == "GET":
        # 取出数据库信息
        classification = cui_experiment.classification
        metal_material = cui_experiment.metal_material
        insulation_material = cui_experiment.insulation_material
        experimenters = cui_experiment.experimenters
        remarks = cui_experiment.remarks
        date = cui_experiment.date
        one_piece = {
            "experiment_name": experiment_name,
            "classification": classification,
            "metal_material": metal_material,
            "insulation_material": insulation_material,
            "experimenters": experimenters,
            "remarks": remarks,
            "date": date,
        }
        return jsonify(one_piece)

    if request.method == "POST":
        # 获取信息
        classification = request.form.get("classification")
        metal_material = request.form.get("metal_material")
        insulation_material = request.form.get("insulation_material")
        experimenters = request.form.get("experimenters")
        remarks = request.form.get("remarks")
        date = request.form.get("date")
        # 修改信息
        cui_experiment.classification = classification
        cui_experiment.metal_material = metal_material
        cui_experiment.insulation_material = insulation_material
        cui_experiment.experimenters = experimenters
        cui_experiment.remarks = remarks
        cui_experiment.date = date
        db.session.commit()
        print(f"{experiment_name}---cui信息修改成功")
    return ""


@cui_experiment_bp.route("/cui_working_condition_show/<experiment_name>", methods=['GET', "POST"])
def cui_working_condition_show(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    one_piece = {}
    if request.method == "GET":
        one_piece["process_description"] = cui_experiment.process_description
        one_piece["experiment_facility_pic"] = filename_to_url(SAVE_POSITION, cui_experiment.experiment_facility_pic)
        one_piece["pipe_structure"] = cui_experiment.pipe_structure
        one_piece["insulation"] = cui_experiment.insulation
        one_piece["piece_number"] = cui_experiment.piece_number
        one_piece["piece_geometric_information"] = cui_experiment.piece_geometric_information
        one_piece["piece_pic"] = filename_to_url(SAVE_POSITION,
                                                 cui_experiment.piece_pic)
        one_piece["piece_dis_pic"] = filename_to_url(SAVE_POSITION, cui_experiment.piece_dis_pic)
        one_piece["ring_number"] = cui_experiment.ring_number
        one_piece["ring_geometric_information"] = cui_experiment.ring_geometric_information
        one_piece["ring_pic"] = filename_to_url(SAVE_POSITION,
                                                cui_experiment.ring_pic)
        one_piece["ring_dis_pic"] = filename_to_url(SAVE_POSITION, cui_experiment.piece_dis_pic)
        one_piece["pipe_number"] = cui_experiment.pipe_number
        one_piece["pipe_geometric_information"] = cui_experiment.pipe_geometric_information
        one_piece["pipe_pic"] = filename_to_url(SAVE_POSITION,
                                                cui_experiment.pipe_pic)
        one_piece["pipe_dis_pic"] = filename_to_url(SAVE_POSITION, cui_experiment.pipe_dis_pic)
        one_piece["sensors_number"] = cui_experiment.sensors_number
        one_piece["sensors_distribution_pic"] = filename_to_url(SAVE_POSITION,
                                                                cui_experiment.sensors_distribution_pic)
        one_piece["sensors_locations"] = extract_x_y_z_data(SAVE_LOCAL_POSITION, cui_experiment.sensors_location)
        one_piece["working_temperature_text"] = cui_experiment.working_temperature_text
        one_piece["working_temperature_file"] = filename_to_url(SAVE_POSITION,
                                                                cui_experiment.working_temperature_file)
        one_piece["ambient_relative_humidity_file"] = filename_to_url(SAVE_POSITION,
                                                                      cui_experiment.ambient_relative_humidity_file)
        one_piece["ambient_temperature_file"] = filename_to_url(SAVE_POSITION,
                                                                      cui_experiment.ambient_temperature_file)
        one_piece["ambient_temperature"] = extract_all_data(SAVE_LOCAL_POSITION, cui_experiment.ambient_temperature_file)
        one_piece["ambient_relative_humidity"] = extract_all_data(SAVE_LOCAL_POSITION,
                                                            cui_experiment.ambient_relative_humidity_file)
        one_piece["ambient_temperature_and_humidity_file"] = filename_to_url(SAVE_POSITION,
                                                                               cui_experiment.ambient_temperature_and_humidity_file)
        one_piece["ambient_temperature_and_humidity"] = extract_ambient_data(SAVE_LOCAL_POSITION,
                                                                             cui_experiment.ambient_temperature_and_humidity_file)
        return jsonify(one_piece)
    return ""

@cui_experiment_bp.route('/cui_working_condition_add/<experiment_name>', methods=['GET', 'POST'])
def cui_working_condition_add(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == 'POST':
        # 获取数据
        process_description = request.form.get("process_description")
        experiment_facility_pic = acquire_files("experiment_facility_pic")
        pipe_structure = request.form.get('pipe_structure')
        insulation = request.form.get('insulation')
        piece_number = request.form.get('piece_number')
        piece_geometric_information = request.form.get('piece_geometric_information')
        piece_pic = acquire_files('piece_pic')
        piece_dis_pic = acquire_files('piece_dis_pic')
        ring_number = request.form.get('ring_number')
        ring_geometric_information = request.form.get('ring_geometric_information')
        ring_pic = acquire_files('ring_pic')
        ring_dis_pic = acquire_files("ring_dis_pic")
        pipe_number = request.form.get('pipe_number')
        pipe_geometric_information = request.form.get('pipe_geometric_information')
        pipe_pic = acquire_files('pipe_pic')
        pipe_dis_pic = acquire_files("pipe_dis_dic")
        sensors_number = request.form.get('sensors_number')
        sensors_distribution_pic = acquire_files('sensors_distribution_pic')
        working_temperature_text = request.form.get('working_temperature_text')
        working_temperature_file = acquire_files('working_temperature_file')
        ambient_temperature_file = acquire_files('ambient_temperature_file')
        ambient_relative_humidity_file = acquire_files('ambient_relative_humidity_file')
        sensors_location = acquire_files('sensors_locations_file')
        ambient_temperature_and_humidity_file = acquire_files('ambient_temperature_and_humidity_file')
        # 添加信息到数据库并保存数据文件
        cui_experiment.process_description = process_description
        cui_experiment.experiment_facility_pic = file_save_to_sql(SAVE_LOCAL_POSITION, experiment_facility_pic)
        cui_experiment.pipe_structure = pipe_structure
        cui_experiment.insulation = insulation
        cui_experiment.piece_number = piece_number
        cui_experiment.piece_geometric_information = piece_geometric_information
        cui_experiment.piece_pic = file_save_to_sql(SAVE_LOCAL_POSITION, piece_pic)
        cui_experiment.piece_dis_pic = file_save_to_sql(SAVE_LOCAL_POSITION, piece_dis_pic)
        cui_experiment.ring_number = ring_number
        cui_experiment.ring_geometric_information = ring_geometric_information
        cui_experiment.ring_pic = file_save_to_sql(SAVE_LOCAL_POSITION, ring_pic)
        cui_experiment.ring_dis_pic = file_save_to_sql(SAVE_LOCAL_POSITION, ring_dis_pic)
        cui_experiment.pipe_number = pipe_number
        cui_experiment.pipe_geometric_information = pipe_geometric_information
        cui_experiment.pipe_pic = file_save_to_sql(SAVE_LOCAL_POSITION, pipe_pic)
        cui_experiment.pipe_dis_pic = file_save_to_sql(SAVE_LOCAL_POSITION, pipe_dis_pic)
        cui_experiment.sensors_number = sensors_number
        cui_experiment.sensors_distribution_pic = file_save_to_sql(SAVE_LOCAL_POSITION, sensors_distribution_pic)
        cui_experiment.sensors_location = file_save_to_sql(SAVE_LOCAL_POSITION, sensors_location)
        cui_experiment.working_temperature_text = working_temperature_text
        cui_experiment.working_temperature_file = file_save_to_sql(SAVE_LOCAL_POSITION, working_temperature_file)
        cui_experiment.ambient_temperature_file = file_save_to_sql(SAVE_LOCAL_POSITION, ambient_temperature_file)
        cui_experiment.ambient_relative_humidity_file = file_save_to_sql(SAVE_LOCAL_POSITION, ambient_relative_humidity_file)
        cui_experiment.ambient_temperature_and_humidity_file = file_save_to_sql(SAVE_LOCAL_POSITION, ambient_temperature_and_humidity_file)
        db.session.commit()
    print(f"{experiment_name}---working condition添加成功")
    return ""


@cui_experiment_bp.route('/cui_working_condition_modify/<experiment_name>', methods=['GET', 'POST'])
def cui_working_condition_modify(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    one_piece = {}
    if request.method == "GET":
        one_piece["process_description"] = cui_experiment.process_description
        one_piece["experiment_facility_pic"] = filename_to_url(SAVE_POSITION, cui_experiment.experiment_facility_pic)
        one_piece["pipe_structure"] = cui_experiment.pipe_structure
        one_piece["insulation"] = cui_experiment.insulation
        one_piece["piece_number"] = cui_experiment.piece_number
        one_piece["piece_geometric_information"] = cui_experiment.piece_geometric_information
        one_piece["piece_pic"] = filename_to_url(SAVE_POSITION, cui_experiment.piece_pic)
        one_piece["piece_dis_pic"] = filename_to_url(SAVE_POSITION, cui_experiment.piece_dis_pic)
        one_piece["ring_number"] = cui_experiment.ring_number
        one_piece["ring_geometric_information"] = cui_experiment.ring_geometric_information
        one_piece["ring_pic"] = filename_to_url(SAVE_POSITION, cui_experiment.ring_pic)
        one_piece["ring_dis_pic"] = filename_to_url(SAVE_POSITION, cui_experiment.ring_dis_pic)
        one_piece["pipe_number"] = cui_experiment.pipe_number
        one_piece["pipe_geometric_information"] = cui_experiment.pipe_geometric_information
        one_piece["pipe_pic"] = filename_to_url(SAVE_POSITION,
                                                cui_experiment.pipe_pic)
        one_piece["pipe_dis_pic"] = filename_to_url(SAVE_POSITION, cui_experiment.pipe_dis_pic)
        one_piece["sensors_number"] = cui_experiment.sensors_number
        one_piece["sensors_distribution_pic"] = filename_to_url(SAVE_POSITION,
                                                                cui_experiment.sensors_distribution_pic)
        one_piece["sensors_locations_file"] = filename_to_url(SAVE_LOCAL_POSITION, cui_experiment.sensors_location)
        one_piece["working_temperature_text"] = cui_experiment.working_temperature_text
        one_piece["working_temperature_file"] = filename_to_url(SAVE_POSITION,
                                                                cui_experiment.working_temperature_file)
        one_piece["ambient_temperature_file"] = filename_to_url(SAVE_POSITION, cui_experiment.ambient_temperature_file)
        one_piece["ambient_relative_humidity_file"] = filename_to_url(SAVE_POSITION,
                                                                          cui_experiment.ambient_relative_humidity_file)
        one_piece["ambient_temperature_and_humidity_file"] = filename_to_url(SAVE_POSITION, cui_experiment.ambient_temperature_and_humidity_file)
        return jsonify(one_piece)

    if request.method == 'POST':
        # 删除旧文件
        #cui_remove = CuiRemoveFiles()
        #cui_remove.cui_working_condition_remove_files(SAVE_POSITION, cui_experiment)
        # 获取信息
        process_description = request.form.get('process_description')
        experiment_facility_pic = acquire_files('experiment_facility_pic')
        if experiment_facility_pic != [] and experiment_facility_pic != None:
            cui_experiment.experiment_facility_pic = file_save_to_sql(SAVE_LOCAL_POSITION, experiment_facility_pic)
        pipe_structure = request.form.get('pipe_structure')
        insulation = request.form.get('insulation')
        piece_number = request.form.get('piece_number')
        piece_pic = request.form.get("piece_pic")
        if piece_pic != [] and piece_pic != None:
            cui_experiment.piece_pic = file_save_to_sql(SAVE_LOCAL_POSITION, piece_pic)
        piece_dis_pic = request.form.get("piece_dis_pic")
        if piece_dis_pic != [] and piece_dis_pic != None:
            cui_experiment.piece_dis_pic = file_save_to_sql(SAVE_LOCAL_POSITION, piece_dis_pic)
        ring_geometric_information = request.form.get('ring_geometric_information')
        ring_pic = acquire_files('ring_pic')
        if ring_pic != [] and ring_pic != None:
            cui_experiment.ring_pic = file_save_to_sql(SAVE_LOCAL_POSITION, ring_pic)
        ring_dis_pic = acquire_files("ring_dis_pic")
        if ring_dis_pic != [] and ring_dis_pic != None:
            cui_experiment.ring_dis_pic = file_save_to_sql(SAVE_LOCAL_POSITION, ring_dis_pic)
        pipe_number = request.form.get('pipe_number')
        pipe_geometric_information = request.form.get('pipe_geometric_information')
        pipe_pic = acquire_files('pipe_pic')
        if pipe_pic != [] and pipe_pic != None:
            cui_experiment.pipe_pic = file_save_to_sql(SAVE_LOCAL_POSITION, pipe_pic)
        pipe_dis_pic = acquire_files("pipe_dis_pic")
        if pipe_dis_pic != [] and pipe_dis_pic != None:
            cui_experiment.pipe_dis_pic = file_save_to_sql(SAVE_LOCAL_POSITION, pipe_dis_pic)
        sensors_number = request.form.get('sensors_number')
        sensors_distribution_pic = acquire_files('sensors_distribution_pic')
        if sensors_distribution_pic != [] and sensors_distribution_pic != None:
            cui_experiment.sensors_distribution_pic = file_save_to_sql(SAVE_LOCAL_POSITION, sensors_distribution_pic)
        working_temperature_text = request.form.get('working_temperature_text')
        working_temperature_file = acquire_files('working_temperature_file')
        if working_temperature_file != [] and working_temperature_file != None:
            cui_experiment.working_temperature_file = file_save_to_sql(SAVE_LOCAL_POSITION, working_temperature_file)
        sensors_locations = acquire_files('sensors_locations_file')
        if sensors_locations != [] and sensors_locations != None:
            cui_experiment.sensors_location = file_save_to_sql(SAVE_LOCAL_POSITION, sensors_locations)
        ambient_temperature_file = acquire_files('ambient_temperature_file')
        if ambient_temperature_file != [] and ambient_temperature_file != None:
            cui_experiment.ambient_temperature_file = file_save_to_sql(SAVE_LOCAL_POSITION, ambient_temperature_file)
        ambient_relative_humidity_file = acquire_files('ambient_relative_humidity_file')
        if ambient_relative_humidity_file != [] and ambient_relative_humidity_file != None:
            cui_experiment.environment_relative_humidity_file = file_save_to_sql(SAVE_LOCAL_POSITION, ambient_relative_humidity_file)
        ambient_temperature_and_humidity_file = acquire_files('ambient_temperature_and_humidity_file')
        if ambient_temperature_and_humidity_file != [] and ambient_temperature_and_humidity_file != None:
            cui_experiment.ambient_temperature_and_humidity_file = file_save_to_sql(SAVE_LOCAL_POSITION, ambient_temperature_and_humidity_file)
        # 修改数据库信息（非文件）
        cui_experiment.process_description = process_description
        cui_experiment.pipe_structure = pipe_structure
        cui_experiment.insulation = insulation
        cui_experiment.piece_number = piece_number
        cui_experiment.ring_geometric_information = ring_geometric_information
        cui_experiment.pipe_number = pipe_number
        cui_experiment.pipe_geometric_information = pipe_geometric_information
        cui_experiment.sensors_number = sensors_number
        cui_experiment.working_temperature_text = working_temperature_text
        db.session.commit()

        print(f"{experiment_name}---working condition信息修改成功")
    return ""


@cui_experiment_bp.route('/cui_result_show/<experiment_name>', methods=['GET', 'POST'])
def cui_result_show(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == "GET":
        one_piece = {
            "sensors_temperature_humidity_data": extract_sensors_data(SAVE_LOCAL_POSITION, cui_experiment.sensors_temperature_humidity_data_file),
            "sensors_temperature_data": extract_data_without_name(SAVE_LOCAL_POSITION, cui_experiment.sensors_temperature_data_file),
            "sensors_relative_humidity_data": extract_data_without_name(SAVE_LOCAL_POSITION, cui_experiment.sensors_relative_humidity_data_file),
            "sensors_temperature_data_file": os.path.join(SAVE_LOCAL_POSITION, cui_experiment.sensors_temperature_data_file),
            "sensors_relative_humidity_data_file": os.path.join(SAVE_LOCAL_POSITION, cui_experiment.sensors_relative_humidity_data_file),
            "localized_pic": filename_to_url(SAVE_POSITION,cui_experiment.localized_pic),
            "general_pic": filename_to_url(SAVE_POSITION, cui_experiment.general_pic),
            "pitting_pic": filename_to_url(SAVE_POSITION,cui_experiment.pitting_pic),
            "stress_pic": filename_to_url(SAVE_POSITION, cui_experiment.stress_pic),
            "morphology_piece_pic": filename_to_url(SAVE_POSITION, cui_experiment.morphology_piece_pic),
            "morphology_ring_pic": filename_to_url(SAVE_POSITION, cui_experiment.morphology_ring_pic),
            "morphology_pipe_pic": filename_to_url(SAVE_POSITION, cui_experiment.morphology_pipe_pic),
            "mass_piece": extract_data_without_name(SAVE_LOCAL_POSITION, cui_experiment.mass_piece_file),
            "mass_piece_table": extract_mass_piece_data(SAVE_LOCAL_POSITION, cui_experiment.mass_piece_file),
            "mass_piece_file": os.path.join(SAVE_LOCAL_POSITION, cui_experiment.mass_piece_file),
            "mass_ring": filename_to_url(SAVE_POSITION, cui_experiment.mass_ring_file),
            "mass_ring_table": extract_mass_piece_data(SAVE_LOCAL_POSITION, cui_experiment.mass_ring_file),
            "mass_ring_file": os.path.join(SAVE_LOCAL_POSITION, cui_experiment.mass_ring_file),
            "mass_pipe": filename_to_url(SAVE_POSITION, cui_experiment.mass_pipe_file),
            "mass_pipe_table": extract_mass_piece_data(SAVE_LOCAL_POSITION, cui_experiment.mass_pipe_file),
            "mass_pipe_file": os.path.join(SAVE_LOCAL_POSITION, cui_experiment.mass_pipe_file)
        }
        return jsonify(one_piece)
    return ""


@cui_experiment_bp.route('/cui_result_add/<experiment_name>', methods=['GET', 'POST'])
def cui_result_add(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == 'POST':
        # 获取信息
        sensors_temperature_data_file = acquire_files('sensors_temperature_data_file')
        sensors_relative_humidity_data_file = acquire_files('sensors_relative_humidity_data_file')
        sensors_temperature_humidity_data_file = acquire_files("sensors_temperature_humidity_data_file")
        localized_pic = acquire_files('localized_pic')
        general_pic = acquire_files('general_pic')
        pitting_pic = acquire_files('pitting_pic')
        stress_pic = acquire_files('stress_pic')
        morphology_piece_pic = acquire_files('morphology_piece_pic')
        morphology_ring_pic = acquire_files('morphology_ring_pic')
        morphology_pipe_pic = acquire_files('morphology_pipe_pic')
        mass_piece_file = acquire_files('mass_piece_file')
        mass_ring_file = acquire_files('mass_ring_file')
        mass_pipe_file = acquire_files('mass_pipe_file')
        # 添加信息
        cui_experiment.sensors_temperature_data_file = file_save_to_sql(SAVE_LOCAL_POSITION, sensors_temperature_data_file)
        cui_experiment.sensors_relative_humidity_data_file = file_save_to_sql(SAVE_LOCAL_POSITION, sensors_relative_humidity_data_file)
        cui_experiment.localized_pic = file_save_to_sql(SAVE_LOCAL_POSITION, localized_pic)
        cui_experiment.general_pic = file_save_to_sql(SAVE_LOCAL_POSITION, general_pic)
        cui_experiment.pitting_pic = file_save_to_sql(SAVE_LOCAL_POSITION, pitting_pic)
        cui_experiment.stress_pic = file_save_to_sql(SAVE_LOCAL_POSITION, stress_pic)
        cui_experiment.morphology_piece_pic = file_save_to_sql(SAVE_LOCAL_POSITION, morphology_piece_pic)
        cui_experiment.morphology_ring_pic = file_save_to_sql(SAVE_LOCAL_POSITION, morphology_ring_pic)
        cui_experiment.morphology_pipe_pic = file_save_to_sql(SAVE_LOCAL_POSITION, morphology_pipe_pic)
        cui_experiment.mass_piece_file = file_save_to_sql(SAVE_LOCAL_POSITION, mass_piece_file)
        cui_experiment.mass_ring_file = file_save_to_sql(SAVE_LOCAL_POSITION, mass_ring_file)
        cui_experiment.mass_pipe_file = file_save_to_sql(SAVE_LOCAL_POSITION, mass_pipe_file)
        cui_experiment.sensors_temperature_humidity_data_file = file_save_to_sql(SAVE_LOCAL_POSITION, sensors_temperature_humidity_data_file)
        db.session.commit()
        print(f"{experiment_name}---cui_result添加成功")
    return ""


@cui_experiment_bp.route('/cui_result_modify/<experiment_name>', methods=['GET', 'POST'])
def cui_result_modify(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()

    if request.method == "GET":
        one_piece = {
            "sensors_temperature_humidity_data_file": filename_to_url(SAVE_POSITION,
                                                                      cui_experiment.sensors_temperature_humidity_data_file),
            "sensors_temperature_data_file": filename_to_url(SAVE_POSITION, cui_experiment.sensors_temperature_data_file),
            "sensors_relative_humidity_data_file": filename_to_url(SAVE_POSITION,cui_experiment.sensors_relative_humidity_data_file),
            "localized_pic": filename_to_url(SAVE_POSITION, cui_experiment.localized_pic),
            "general_pic": filename_to_url(SAVE_POSITION,cui_experiment.general_pic),
            "pitting_pic": filename_to_url(SAVE_POSITION, cui_experiment.pitting_pic),
            "stress_pic": filename_to_url(SAVE_POSITION, cui_experiment.stress_pic),
            "morphology_piece_pic": filename_to_url(SAVE_POSITION, cui_experiment.morphology_piece_pic),
            "morphology_ring_pic": filename_to_url(SAVE_POSITION, cui_experiment.morphology_ring_pic),
            "morphology_pipe_pic": filename_to_url(SAVE_POSITION, cui_experiment.morphology_pipe_pic),
            "mass_piece_file": filename_to_url(SAVE_POSITION, cui_experiment.mass_piece_file),
            "mass_ring_file": filename_to_url(SAVE_POSITION, cui_experiment.mass_ring_file),
            "mass_pipe_file": filename_to_url(SAVE_POSITION, cui_experiment.mass_pipe_file),
        }
        return jsonify(one_piece)

    if request.method == "POST":
        # 删除旧文件
        # cui_remove = CuiRemoveFiles()
        # cui_remove.cui_result_remove_files(SAVE_POSITION, cui_experiment)
        # 获取信息
        sensors_temperature_humidity_data_file = acquire_files('sensors_temperature_humidity_data_file')
        if sensors_temperature_humidity_data_file != [] and sensors_temperature_humidity_data_file != None:
            cui_experiment.sensors_temperature_humidity_data_file = file_save_to_sql(SAVE_LOCAL_POSITION,
                                                                                     sensors_temperature_humidity_data_file)
        localized_pic = acquire_files('localized_pic')
        if localized_pic != [] and localized_pic != None:
            cui_experiment.localized_pic = file_save_to_sql(SAVE_LOCAL_POSITION, localized_pic)
        general_pic = acquire_files('general_pic')
        if general_pic != [] and general_pic != None:
            cui_experiment.general_pic = file_save_to_sql(SAVE_LOCAL_POSITION, general_pic)
        pitting_pic = acquire_files('pitting_pic')
        if pitting_pic != [] and pitting_pic != None:
            cui_experiment.pitting_pic = file_save_to_sql(SAVE_LOCAL_POSITION, pitting_pic)
        stress_pic = acquire_files('stress_pic')
        if stress_pic != [] and stress_pic != None:
            cui_experiment.stress_pic = file_save_to_sql(SAVE_LOCAL_POSITION, stress_pic)
        morphology_piece_pic = acquire_files('morphology_piece_pic')
        if morphology_piece_pic != [] and morphology_piece_pic != None:
            cui_experiment.morphology_piece_pic = file_save_to_sql(SAVE_LOCAL_POSITION, morphology_piece_pic)
        morphology_ring_pic = acquire_files('morphology_ring_pic')
        if morphology_ring_pic != [] and morphology_piece_pic != None:
            cui_experiment.morphology_ring_pic = file_save_to_sql(SAVE_LOCAL_POSITION, morphology_ring_pic)
        morphology_pipe_pic = acquire_files('morphology_pipe_pic')
        if morphology_pipe_pic != [] and morphology_pipe_pic != None:
            cui_experiment.morphology_pipe_pic = file_save_to_sql(SAVE_LOCAL_POSITION, morphology_pipe_pic)
        mass_piece_file = acquire_files('mass_piece_file')
        if mass_piece_file != [] and mass_piece_file != None:
            cui_experiment.mass_piece_file = file_save_to_sql(SAVE_LOCAL_POSITION, mass_piece_file)
        mass_ring_file = acquire_files('mass_ring_file')
        if mass_ring_file != [] and mass_ring_file != None:
            cui_experiment.mass_ring_file = file_save_to_sql(SAVE_LOCAL_POSITION, mass_ring_file)
        mass_pipe_file = acquire_files('mass_pipe_file')
        if mass_pipe_file != [] and mass_pipe_file != None:
            cui_experiment.mass_pipe_file = file_save_to_sql(SAVE_LOCAL_POSITION, mass_pipe_file)
        # 添加信息
        db.session.commit()
        print(f"{experiment_name}---cui_result信息修改成功")
    return ""


@cui_experiment_bp.route('/cui_delete/<experiment_name>', methods=['GET', 'POST'])
def cui_delete(experiment_name):
    cui_experiment = CuiExperiment.query.filter_by(experiment_name=experiment_name).first()
    if request.method == "GET":
        try:
            cui_remove = files_remove.CuiRemoveFiles()
            cui_remove.cui_working_condition_remove_files(SAVE_LOCAL_POSITION, cui_experiment)
            print("cui_working_condition删除成功")
            cui_remove.cui_result_remove_files(SAVE_LOCAL_POSITION, cui_experiment)
            print("cui_result删除成功")
            db.session.delete(cui_experiment)
            db.session.commit()
        except Exception as e:
            raise e
    print(f"{cui_experiment}---删除成功")
    return ""

@cui_experiment_bp.route('/test', methods=['GET', 'POST'])
def test():
    data = [[[2,3], [4,5]], [[7,8], [9,10]]]
    return json.dumps(data)