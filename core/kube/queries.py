from flask import g
from flask_sqlalchemy import BaseQuery, SQLAlchemy

from core.kube import models

class DeploymentQuery(BaseQuery):
    def get_by_ref(self, ref):
        try:
            return self.get(int(ref.split('-')[-1]))
        except ValueError:
            print('[Error] Unablet to find Deployment. Invalid ref.')

    def filter_by_user(self, user_id):
        print("Filter by user: ", user_id)
        print(g.user)
        print(g.user.get_user_id())
        return self.filter(models.Deployment.creator_id == user_id)