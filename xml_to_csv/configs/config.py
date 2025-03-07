import logging

import yaml

logging.basicConfig(
    level=logging.INFO,
    format="Config Logging %(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
def load_config(config_path: str) -> dict:
    """
    This function loads the config file and returns it as a dictionary.
    :param config_path:
    :return:
    """

    with open(config_path, 'r') as file:
        logging.info(f"Reading the config file from {config_path}.")
        return yaml.safe_load(file)