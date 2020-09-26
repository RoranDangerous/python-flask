import os
from kubernetes import client, config

CONFIG = os.environ.get('KUBERNETES_CONFIG')

assert CONFIG, "Missing Kubernetes config file."

class Core:
    """ CoreV1Api Config """

    API = client.CoreV1Api(config.new_client_from_config(
        config_file=CONFIG,
        context="minikube",
        persist_config=False
    ))

class Batch:
    """ BatchV1Api Config """
    API = client.BatchV1Api(config.new_client_from_config(
        config_file=CONFIG,
        context="minikube",
        persist_config=False
    ))

class Apps:
    """ AppsV1Api Config """
    API = client.AppsV1Api(config.new_client_from_config(
        config_file=CONFIG,
        context="minikube",
        persist_config=False
    ))

import core.kube.urls