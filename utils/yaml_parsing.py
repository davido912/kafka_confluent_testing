import yaml


def parse_yaml_file(file_path: str):
    with open(file_path) as f:
        return yaml.load(f, Loader=yaml.FullLoader)
