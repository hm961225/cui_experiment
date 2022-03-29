from flask import Blueprint, session, jsonify, redirect, url_for


index_bp = Blueprint('index_bp', __name__)


@index_bp.route('/')
@index_bp.route('/index')
def index():
    if 'username' in session:
        res = {
            'username': session['username']
        }
        return jsonify(res)
    # else:
    #     return redirect(url_for('login'))
    return ""