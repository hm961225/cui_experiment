from flask import request, Blueprint, jsonify

from app.models import db
from app.models.materials import Insulation


insulation_bp = Blueprint("insulation_bp", __name__)


@insulation_bp.route("/insulation_add", methods=["GET","POST"])
def insulation_add():
    if request.method == "POST":
        name = request.name = request.form.get("name")
        introduction = request.form.get("introduction")
        classification = request.form.get("classification")
        density = request.form.get("density")
        specific_heat = request.form.get("specific_heat")
        thermal_conductivity = request.form.get("thermal_conductivity")

        insulation = Insulation(name=name,
                                introduction=introduction,
                                classification=classification,
                                density=density,
                                specific_heat=specific_heat,
                                thermal_conductivity=thermal_conductivity
                                )
        db.session.add(insulation)
        db.session.commit()
    return ""

@insulation_bp.route("/insulation_modify/<insulation_name>", methods=["GET", "POST"])
def insulation_modify(insulation_name):
    insulation = Insulation.query.filter_by(name=insulation_name)
    one_piece = {}
    if request.method == "GET":
        one_piece["name"] = insulation.name
        one_piece["introduction"] = insulation.introduction
        one_piece["classification"] = insulation.classification
        one_piece["density"] = insulation.density
        one_piece["specific_heat"] = insulation.specific_heat
        one_piece["thermal_conductivity"] = insulation.thermal_conductivity
        return jsonify(one_piece)
    if request.method == "POST":
        insulation.name = request.form.get("name")
        insulation.introduction = request.form.get("introduction")
        insulation.classification = request.form.get("classification")
        insulation.density = request.form.get("density")
        insulation.specific_heat = request.form.get("specific_heat")
        insulation.thermal_conductivity = request.form.get("thermal_conductivity")
        db.session.commit()
    return ""

@insulation_bp.route("/insulation_delete/<insulation_name>", methods=["GET", "POST"])
def insulation_delete(insulation_name):
    if request.method == "GET":
        insulation = Insulation.query.filter_by(name=insulation_name)
        db.session.delete(insulation)
        db.session.commit()
