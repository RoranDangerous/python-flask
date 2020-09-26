from kubernetes.stream import stream
from kubernetes.client.rest import ApiException
from core.kube import Core

def get_pod_name(deployment_ref):
    response = Core.API.list_namespaced_pod('default', label_selector=f'mintzone/ref={deployment_ref}')

    if len(response.items) == 0:
        print(f'[ERROR] No pods found for {deployment_ref}')
        return None

    return response.items[0].metadata.name

def add_file(pod_name):
    response = stream(
        Core.API.connect_get_namespaced_pod_exec,
        pod_name,
        'default',
        command=['/bin/sh'],
        stderr=True,
        stdin=True,
        stdout=True,
        tty=False,
        _preload_content=False
    )

    f = open('core/kube/files/main.py', 'r')

    commands = []
    commands.append("cat <<'EOF' >" + "/home/project/main.py" + "\n")
    commands.append(f.read())

    while response.is_open():
        response.update(timeout=1)
        if response.peek_stdout():
            print("STDOUT: %s" % response.read_stdout())
        if response.peek_stderr():
            print("STDERR: %s" % response.read_stderr())

        if commands:
            c = commands.pop(0)
            response.write_stdin(c)
        else:
            break

    response.close()


def get_player_move(pod_name, field):
    try:
        response = stream(
            Core.API.connect_get_namespaced_pod_exec,
            pod_name,
            'default',
            command=['/bin/sh', '-c', f'python3 /home/project/main.py {" ".join(field)}'],
            stderr=True,
            stdin=False,
            stdout=True,
            tty=False
        )
        return response.strip('\n')
    except ApiException as ex:
        print(f'[Operations] Unable to get player move: {ex}')
        return ''