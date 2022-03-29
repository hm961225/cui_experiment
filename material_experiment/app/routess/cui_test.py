from app import app
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_cors import cross_origin
from app.models import User, FlowExperiment, CuiExperiment, Metal, Insulation, test
from app import db

@app.route('/test_adds', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def test_adds():
    if request.method == "POST":
        print(request.form)
        print(request.files)
        name = request.form.get("name")
        print(name)
        request.files.get("")
        return ""
    return ""