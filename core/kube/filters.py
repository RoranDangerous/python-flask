from flask_jwt_extended import get_jwt_identity
from core.kube import models

class DeploymentCreatorFilter:
  @classmethod
  def as_filter(self, *args, **kwargs):
    user = get_jwt_identity()

    return user and models.Deployment.creator_id == user['id']