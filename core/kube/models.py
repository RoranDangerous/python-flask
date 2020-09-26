from random import randint
from kubernetes import client
from sqlalchemy.dialects.postgresql import JSON
from core import db, bcrypt
from core.kube import Apps, Core, containers, queries, operations
from core.utils import channels


class Deployment(db.Model):
    """ Deployment Model for storing deployment related details """
    __tablename__ = "deployments"
    query_class = queries.DeploymentQuery

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    creator = db.relationship("User", backref=db.backref("deployments", uselist=False), foreign_keys=[creator_id])
    name = db.Column(db.String(255), unique=False, nullable=False)
    status = db.Column(db.String(32), nullable=False, server_default='Stopped')
    pod = db.Column(db.String(64), nullable=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey("workspaces.id"), nullable=True)
    workspace = db.relationship("Workspace", backref=db.backref("deployments"), foreign_keys=[workspace_id]) # TODO: Test delete
    workspace_port_id = db.Column(db.Integer, db.ForeignKey("service_ports.id"), nullable=True)
    workspace_port = db.relationship("ServicePort", backref=db.backref("deployments"), foreign_keys=[workspace_port_id]) # TODO: Test delete

    @property
    def ref(self):
        """
        Generates the deployment ref
        :return: string
        """
        return f"deployment-{self.id}"

    @property
    def service_ref(self):
        """
        Generates the service ref
        :return: string
        """
        return f"service-{self.id}"

    @property
    def serialize(self):
        """
        Returns serializable object
        """
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "workspace": {
                "name": self.workspace and self.workspace.display_name,
                "url": f'http://192.168.39.189:{self.workspace_port.port}/{self.workspace_port.url_params or ""}' if self.workspace_port else None
            }
        }

    @property
    def kube_body(self):
        """
        Build kubernetes deployment
        :return: client.V1Deployment
        """
        return client.V1Deployment(
            metadata=client.V1ObjectMeta(
                name=self.ref
            ),
            spec=client.V1DeploymentSpec(
                replicas=1,
                selector=client.V1LabelSelector(
                    match_labels={
                        'mintzone/ref': self.ref
                    }
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels={
                            "mintzone/ref": self.ref
                        }
                    ),
                    spec=client.V1PodSpec(
                        containers=self.containers,
                        volumes=[
                            client.V1Volume(
                                name='data',
                                empty_dir=client.V1EmptyDirVolumeSource(),
                            )
                        ]
                    )
                )
            )
        )

    @property
    def kube_service(self):
        """
        Build kubernetes service
        :return: client.V1Service
        """
        return client.V1Service(
            metadata=client.V1ObjectMeta(
                name=self.service_ref
            ),
            spec=client.V1ServiceSpec(
                selector={
                    "mintzone/ref": self.ref
                },
                ports=self.kube_service_ports,
                external_i_ps=["192.168.39.189"]
            )
        )

    @property
    def containers(self):
        """
        Build kubernetes containers
        :return: list
        """
        result = []

        try:
            instance = getattr(containers, self.workspace.name)(self)
            result.append(instance.container)
        except AttributeError as ex:
            print(f'ERROR: [Deployment] Workspace "{self.workspace.name}" not found ({ex})')

        return result

    @property
    def kube_service_ports(self):
        """
        Build kubernetes service ports
        :return: list
        """
        if not self.workspace:
            return []

        result = []
        try:
            instance = getattr(containers, self.workspace.name)(self)
            if instance.service_port:
                result.append(instance.service_port)
        except AttributeError as ex:
            print(f'ERROR: [Deployment] Workspace "{self.workspace.name}" not found ({ex})')

        return result

    def start(self):
        # Assign port number
        self.workspace_port = ServicePort()
        db.session.commit()

        Apps.API.create_namespaced_deployment('default', self.kube_body)

        Core.API.create_namespaced_service('default', self.kube_service)

    def stop(self):
        Apps.API.delete_namespaced_deployment(
            self.ref,
            'default'
        )

        Core.API.delete_namespaced_service(
            self.service_ref,
            'default'
        )

        # Delete assigned ports
        db.session.delete(self.workspace_port)
        db.session.commit()

    def on_status_changed(self):
        channels.Deployment(self.id, private=True).trigger('status', self.status)

        switcher = {
            'Running': self.on_running,
            'Stopped': self.on_stopped,
            'Creating': None,
            'Created': self.on_created
        }

        if switcher.get(self.status):
            switcher.get(self.status)()

    def on_created(self):
        self.status = 'Running'

        db.session.commit()

        self.on_status_changed()

    def on_stopped(self):
        self.pod = None

        db.session.commit()

    def on_running(self):
        self.pod = operations.get_pod_name(self.ref)

        db.session.commit()

        operations.add_file(self.pod)


class Workspace(db.Model):
    """ Stores workspaces user can use to work in. Python, Jupyter, etc. """
    __tablename__ = "workspaces"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    display_name = db.Column(db.String(30), unique=True, nullable=False)

    @property
    def serialize(self):
        """
        Returns serializable object
        """
        return {
            "id": self.id,
            "name": self.display_name
        }


class ServicePort(db.Model):
    """ Container Model for storing container details """
    __tablename__ = "service_ports"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    port = db.Column(db.Integer, unique=True, nullable=False)
    url_params = db.Column(db.String(256), unique=False, nullable=True)

    def __init__(self, *args, **kwargs):
        port = 30000 + randint(0, 10000)
        used_ports = [port for port, in db.session.query(ServicePort.port)]
        if len(used_ports) >= 10000:
            raise Exception('Max port limit reached.')

        while port in used_ports:
            port += 1

        self.port = port

        super(ServicePort, self).__init__(*args, **kwargs)