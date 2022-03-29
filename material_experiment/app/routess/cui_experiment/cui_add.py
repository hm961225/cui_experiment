import json

from app.models import CuiExperiment
from app import db

from flask import request, Blueprint


bp = Blueprint('cui_add', __name__, url_prefix='/v1')
@bp.route('/cui_add', methods=['GET', 'POST'])
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