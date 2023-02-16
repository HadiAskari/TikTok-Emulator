import docker
from ppadb.client import Client as AdbClient
from time import sleep
import socket
from contextlib import closing

from android import Android

# get adb and docker clients from system
adb_client = AdbClient(host="127.0.0.1", port=5037)
docker_client = docker.from_env()

def emulate_new_device(name):
    # setup necessary host ports and environment vars
    ports = { 
        "6080/tcp": get_next_available_port(6080), 
        "5555/tcp": get_next_available_port(5555),
        "5554/tcp": get_next_available_port(7000)
    }

    environment = {
        "DEVICE": "Nexus 5", 
        "DATAPARTITION": "3000m"
    }

    # spawn container
    container = docker_client.containers.run('budtmo/docker-android-x86-12.0', name=name, detach=True, privileged=True, ports=ports, environment=environment)
        
    # wait for container to get an IP Address
    while container.attrs['NetworkSettings']['IPAddress'] == '':
        sleep(1)
        container.reload()

    # wait for device to boot
    sleep(30)

    # connect to new device
    adb_client.remote_connect(container.attrs['NetworkSettings']['IPAddress'], 5555)
    
    # return device
    return Android(device=adb_client.device(f"{ container.attrs['NetworkSettings']['IPAddress'] }:5555"), container=container, vnc_port=ports["6080/tcp"])


def get_connected_devices():
    return [Android(dev, None, None) for dev in adb_client.devices()]

def get_next_available_port(starting):
    for port in range(starting, starting + 1000):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if sock.connect_ex(('localhost', port)) != 0:
                return port
    return None
