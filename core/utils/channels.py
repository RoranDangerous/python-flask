from core import pusher
from core.kube import models as kube_models

class Deployment:
  def __init__(self, id, **kwargs):
    self.id = id
    self.name = f'{"private-" if kwargs.get("private") else ""}deployment-{id}'

  def __str__(self):
    return self.name

  def trigger(self, event, payload):
    pusher.trigger(self.name, event, payload)

  def is_authorized(self, user_id):
    deployment = kube_models.Deployment.query.get(self.id)

    if not deployment:
      return False

    if deployment.creator_id != user_id:
      return False

    return True


class Game:
  def __init__(self, id, **kwargs):
    self.id = id
    self.name = f'{"private-" if kwargs.get("private") else ""}game-{id}'

  def __str__(self):
    return self.name

  def trigger(self, event, payload):
    pusher.trigger(self.name, event, payload)

  def is_authorized(self, user_id):
    print(f"User {user_id}")

    return True


def get_channel_from_name(name):
  ''' Returns Channel class from the name '''
  private = name.startswith('private-')
  name_components = name.replace('private-', '').split('-')

  channels = {
    'deployment': Deployment,
    'game': Game
  }

  channel = channels.get(name_components[0])
  if not channel:
    return None

  return channel(name_components[1] if len(name_components) > 1 else None, private=private)