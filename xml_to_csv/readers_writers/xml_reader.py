import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import os
import sys
import logging

from readers_writers.client_registery import client_registry
from readers_writers.read_client import ReadClient

logging.basicConfig(
    level=logging.INFO,
    format="xml_reader %(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


class XMLReadClient(ReadClient):

    def __init__(self, path: str):
        self.path = path

    def read_data(self) -> List[Dict[str, Any]]:
        """
        Read the XML file and return a BeautifulSoup object.

        :param path: Path to the XML file.
        :return: BeautifulSoup object of the parsed XML.
        """
        if not os.path.exists(self.path):
            logging.error(f"File not found: {self.path}")
            sys.exit(1)
        try:
            tree = ET.parse(self.path)
            root = tree.getroot()
            logging.info("XML file parsed successfully.")
            return [{"root": root}]
        except Exception as e:
            logging.error(f"Error parsing XML file: {e}")
            sys.exit(1)


client_registry.register('xml', XMLReadClient)
