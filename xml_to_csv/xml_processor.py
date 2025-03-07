import json
import logging
from typing import List, Dict, Any

from readers_writers.read_client import ReadClient
from readers_writers.write_client import WriteClient
from transformers.transformer import Transformer

# Configure logging for production use.
logging.basicConfig(
    level=logging.INFO,
    format="xml_processor %(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


class XMLProcessor:

    def __init__(self, read_client: ReadClient, write_client: WriteClient):
        self.read_client = read_client
        self.write_client = write_client
        self.xml_data = None
        self.transformed_data = []

    def read_xml_data(self):
        self.xml_data = self.read_client.read_data()
        return self

    def do_transform(self, transformer: Transformer):
        self.transformed_data = transformer.transform(self.xml_data)
        return self

    def write(self):
        self.write_client.write(self.transformed_data)
        return self

    def start(self, transformer: Transformer):
        logging.info(f"Started Processing")

        self.read_xml_data()
        if self.xml_data:
            self.do_transform(transformer=transformer).write()
            print("Executed Write Step")
        else:
            print("No XML data Found")
        logging.info(f"Finished Processing")

        return self
