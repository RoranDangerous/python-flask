from flask_restful import Api
from flask import Blueprint
from core import app
from core.kube import resources

blueprint = Blueprint('kube', __name__)
api = Api(blueprint, catch_all_404s=True)
app.register_blueprint(blueprint, url_prefix='/api')

# URLs
api.add_resource(resources.Deployment, '/deployment/<regex("[0-9]*"):id>', strict_slashes=False)
api.add_resource(resources.DeploymentActions, '/deployment/<regex("[0-9]*"):id>/<regex("start|stop"):action>', strict_slashes=False)
api.add_resource(resources.NewDeployment, '/deployment', strict_slashes=False)
api.add_resource(resources.Deployments, '/deployments', strict_slashes=False)
api.add_resource(resources.DeploymentsActions, '/deployments/<regex("start|stop|delete"):action>', strict_slashes=False)
api.add_resource(resources.Workspaces, '/workspaces', strict_slashes=False)