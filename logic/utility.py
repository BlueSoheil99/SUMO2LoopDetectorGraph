import yaml
import xml.etree.ElementTree as ET


def readxml(address):
    tree = ET.parse(address)
    root = tree.getroot()
    return root


def read_yaml(features: list, config_adr):
    config_file = yaml.safe_load(open(config_adr))
    addresses = []
    for feature in features:
        adr = config_file[feature]
        addresses.append(adr)
    return addresses
