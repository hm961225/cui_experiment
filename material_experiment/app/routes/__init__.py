from .index import index_bp
from .cui_experiment import cui_experiment_bp
from .flow_experiment import flow_experiment_bp
from .login import login_bp
from .insulation import insulation_bp
from .metal import metal_bp


def init_route(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(cui_experiment_bp)
    app.register_blueprint(flow_experiment_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(insulation_bp)
    app.register_blueprint(metal_bp)