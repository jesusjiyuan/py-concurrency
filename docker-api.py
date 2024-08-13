#!/usr/bin/python
import docker
import json

client = docker.DockerClient(base_url='tcp://192.168.220.133:2375')
cls = client.containers.list()
print(cls)