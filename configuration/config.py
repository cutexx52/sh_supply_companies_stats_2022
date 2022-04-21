import yaml


def get_configuration(path='config.yaml'):
    with open(path) as file:
        configuration = yaml.safe_load(file.read())

    return configuration