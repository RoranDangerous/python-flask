from kubernetes import client
from core import db
from core.kube import models


class BaseContainer:
    def __init__(self, deployment):
        assert deployment, f'Deployment object is required.'

        self.deployment = deployment

    @property
    def container(self):
        raise Exception("Not implemented.")

    @property
    def service_port(self):
        raise Exception("Not implemented.")


class SFTP(BaseContainer):
    """ SFTP Container Config """
    IMAGE = "atmoz/sftp"
    NAME = "sftp"

    def __init__(self, *args, **kwargs):
        super(SFTP, self).__init__(*args, **kwargs)

        assert False, 'KubeContainer model was removed, this needs to be fixed.'

        assert self.kube_container.options and self.kube_container.options.get('username'), "Username is required."
        assert self.kube_container.options and self.kube_container.options.get('password'), "Password is required."

    @property
    def args(self):
        return [
            f'{self.kube_container.options.get("username")}:{self.kube_container.options.get("password")}:1001'
        ]

    @property
    def container(self):
        return client.V1Container(
            name=self.NAME,
            image=self.IMAGE,
            args=self.args,
            ports=[
                client.V1ContainerPort(
                    container_port=22,
                    name=self.kube_container.ref
                )
            ],
            volume_mounts=[
                client.V1VolumeMount(
                    mount_path=f'/home/{self.kube_container.options.get("username")}/',
                    name='data',
                )
            ]
        )

    @property
    def service_port(self):
        return client.V1ServicePort(
            name=self.NAME,
            port=self.deployment.workspace_port.port,
            target_port=self.kube_container.ref
        )


class JUPYTER(BaseContainer):
    """ Jupyter Container Config """
    IMAGE = "ufoym/deepo:all-py36-jupyter"
    NAME = "jupyter"
    DATA_DIR = "/root/data"

    def __init__(self, *args, **kwargs):
        super(JUPYTER, self).__init__(*args, **kwargs)

        self.token = 'BsisPdTtEZwDJEK8YolVNMhs7uMP42DeoFKl_eZP2wE'
        self.deployment.workspace_port.url_params = '?token=BsisPdTtEZwDJEK8YolVNMhs7uMP42DeoFKl_eZP2wE'
        db.session.commit()

    @property
    def args(self):
        return [
            ("jupyter notebook --no-browser --ip=0.0.0.0 "
                f"--allow-root --NotebookApp.token={self.token} "
                f"--notebook-dir='{self.DATA_DIR}'")
        ]

    @property
    def service_port(self):
        return client.V1ServicePort(
            name=self.NAME,
            port=self.deployment.workspace_port.port,
            target_port=self.deployment.ref,
        )

    @property
    def container(self):
        return client.V1Container(
            name=self.NAME,
            image=self.IMAGE,
            command=['sh', '-c'],
            args=self.args,
            ports=[
                client.V1ContainerPort(
                    container_port=8888,
                    name=self.deployment.ref,
                ),
            ],
            volume_mounts=[
                client.V1VolumeMount(
                    mount_path=self.DATA_DIR,
                    name='data',
                )
            ]
        )


class THEIA_PYTHON(BaseContainer):
    """ Theia Python IDE Container Config """
    IMAGE = "theiaide/theia-python:latest"
    NAME = "theia-python"
    DATA_DIR = "/home/project"

    @property
    def args(self):
        return [f'--init -p 3000:3000 -v "$(pwd):{self.DATA_DIR}"']

    @property
    def service_port(self):
        return client.V1ServicePort(
            name=self.NAME,
            port=self.deployment.workspace_port.port,
            target_port=self.deployment.ref,
        )

    @property
    def container(self):
        return client.V1Container(
            name=self.NAME,
            image=self.IMAGE,
            args=self.args,
            ports=[
                client.V1ContainerPort(
                    container_port=3000,
                    name=self.deployment.ref,
                ),
            ],
            volume_mounts=[
                client.V1VolumeMount(
                    mount_path=self.DATA_DIR,
                    name='data',
                )
            ]
        )