import unittest
from unittest.mock import patch, mock_open

from xml_to_csv.configs.config import load_config





class TestLoadConfig(unittest.TestCase):
    def test_load_config(self):
        with patch('builtins.open', new_callable=mock_open, read_data="key: value") as file, \
                patch('xml_to_csv.configs.config.yaml.safe_load') as yaml_load:
            yaml_load.return_value = {"key": "value"}

            config_path = './test_config.yaml'
            result = load_config(config_path)

            file.assert_called_once_with(config_path, 'r')
            yaml_load.assert_called_once_with(file.return_value)
            self.assertEqual(result, {"key": "value"})