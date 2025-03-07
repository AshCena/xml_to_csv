from transformers.xml_transformer import XMLTransformer
from xml_processor import XMLProcessor
from configs.config import load_config
from readers_writers.client_registery import client_registry
from readers_writers.csv_writer import CSVToXMLWriteClient
from readers_writers.xml_reader import XMLReadClient

def get_config():
    config = load_config('configs/config.yaml')
    # Create clients based on the configuration
    read_config = config['processor']['reader']
    write_config = config['processor']['writer']
    print(read_config, write_config)
    read_client = client_registry.create(read_config['type'], **read_config)
    write_client = client_registry.create(write_config['type'], **write_config)
    return read_client, write_client


def main():

    read_client, write_client = get_config()
    processor = XMLProcessor(read_client, write_client)
    xml_transformer = XMLTransformer()
    processor.start(transformer=xml_transformer)


if __name__ == "__main__":
    main()