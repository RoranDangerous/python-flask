from multiprocessing import Process
from kubernetes.watch import Watch
from core import db
from core.kube import Apps, models


class DeploymentSync:
    '''
    Sync Deployments status. Watches for kubernetes deployment events and updates database references.
    '''
    def start_async(self):
        process = Process(target=self.start)
        process.start()

    def start(self):
        # Update all deployments to status 'Stopped'.
        for deployment in models.Deployment.query.all():
            deployment.status = 'Stopped'
            deployment.on_status_changed()
        db.session.commit()

        # Create a watcher for kube events. Sync deployment status on each event.
        watch = Watch()
        for event in watch.stream(Apps.API.list_namespaced_deployment, 'default', watch=True):
            print('[DEBUG]', event['type'], event['object'].metadata.name, event['object'].status.available_replicas)

            deployment = models.Deployment.query.get_by_ref(event['object'].metadata.name)

            if event['type'] == 'DELETED':
                deployment.status = 'Stopped'
            elif not event['object'].status.available_replicas:
                deployment.status = 'Creating'
            elif event['type'] == 'MODIFIED':
                deployment.status = 'Created'
            else:
                deployment.status = 'Running'

            db.session.commit()

            deployment.on_status_changed()