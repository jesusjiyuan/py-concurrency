# coding: utf-8
import os
os.chdir(os.path.dirname(__file__))

import yaml
conf_file = "config-dev.yml"
def read_conf(conf_file) -> dict:
    with open(conf_file,"r") as f:
        return yaml.safe_load(f)

def confdata():
    return read_conf(conf_file)

def curenv():
    return read_conf(conf_file).get("env")


