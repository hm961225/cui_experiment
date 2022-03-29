from flask import Blueprint, request, jsonify

from app.models import db
from app.models.materials import Metal


metal_bp = Blueprint("metal_bp", __name__)


@metal_bp.route('/metal_show', methods=['GET', 'POST'])
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
            one_piece = {}
        return jsonify(res)

@metal_bp.route('/metal_add', methods=['GET', 'POST'])
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
        print(f"{name}添加成功")
    return ""

@metal_bp.route('/metal_modify/<metal_name>', methods=['GET', 'POST'])
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
        db.session.commit()
        print(f"{metal_name}修改成功")
        return ""

@metal_bp.route("/metal_delete/<metal_name>", methods=["GET", "POST"])
def metal_delete(metal_name):
    if request.method == "GET":
        metal = Metal.query.filter_by(metal_name=metal_name).first()
        db.session.delete(metal)
        db.session.commit()
        print(f"metal{metal_name}删除成功")
    return ""