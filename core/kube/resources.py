from flask_jwt_extended import get_jwt_identity
from core import db
from core.generics import Resource, ListResource, SingleResource
from core.kube import models, filters


class Deployment(SingleResource):
  """
  Deployment get/update/delete
  """
  model = models.Deployment
  apply_filters = (filters.DeploymentCreatorFilter,)
  methods = ['GET', 'PATCH', 'DELETE']
  editable_fields = ['name', 'workspace_id']


class NewDeployment(Resource):
  """
  Deployment create
  """

  def post(self):
    user = get_jwt_identity()

    deployment = models.Deployment(
        creator_id=user['id'],
        name=self.data.get('name', 'New'),
        workspace_id = self.data.get('workspace')
    )

    db.session.add(deployment)
    db.session.commit()

    return deployment.serialize


class DeploymentActions(Resource):
  def patch(self, id, action):
    self.deployment = models.Deployment.query.get(id)

    if not self.deployment:
      return {'error': 'Invalid deployment id'}, 404

    try:
      getattr(self, action)()
    except AttributeError as ex:
      print(f'[Error] {ex.__class__.__name__}: {ex}')
      return {'error': 'Invalid action'}, 400
    except Exception as ex:
      print(f'ERROR: Action failed. {ex.__class__.__name__}({ex})')
      return {'error': 'Unknown error'}, 400

    return self.deployment.serialize

  def start(self):
    self.deployment.start()

  def stop(self):
    self.deployment.stop()


class Deployments(ListResource):
  model = models.Deployment
  apply_filters = (filters.DeploymentCreatorFilter,)


class DeploymentsActions(Resource):
  required_fields = ['ids']

  def patch(self, action):
    if type(self.data['ids']) != list:
      return {'error': 'Invalid parameters. Expected list of ids: {\'ids\': [1,2,3]}'}, 400

    self.deployments = models.Deployment.query.filter(models.Deployment.id.in_(self.data['ids'])).all()

    try:
      getattr(self, action)()
    except AttributeError:
      return {'error': 'Invalid action'}, 400
    except Exception as ex:
      print(f'ERROR: Action failed. {ex.__class__.__name__}({ex})')
      return {'error': 'Unknown error'}, 400

    return {'success': True}

  def start(self):
    for d in self.deployments:
      d.start()

  def stop(self):
    for d in self.deployments:
      d.stop()

  def delete(self):
    for d in self.deployments:
      db.session.delete(d)

    db.session.commit()


class Workspaces(ListResource):
  model = models.Workspace