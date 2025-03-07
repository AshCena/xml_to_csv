import csv
import logging
from abc import ABC, abstractmethod
from typing import List, Any

from readers_writers.client_registery import client_registry
from readers_writers.write_client import WriteClient

# Configure logging for production use.
logging.basicConfig(
    level=logging.INFO,
    format="csv_writer %(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


class CSVToXMLWriteClient(WriteClient):
    def __init__(self, path: str):
        """
        Initializes the CSVWriteClient.

        :param path: The path to the CSV file to be written.
        :param fieldnames: A list of keys to be used as column headers.
        """
        self.path = path
        self.fieldnames = None

    def write(self, data: List[Any]) -> None:
        """
        Writes the provided data to a CSV file.

        Expects data as a list of dictionaries where keys correspond to fieldnames.

        :param data: List of dictionaries containing the data to write.
        """
        try:
            with open(self.path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data[1], quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for row in data[0]:
                    out_row = {
                        "Section": row["Section"],
                        "CombinedSubsection": row["CombinedSubsection"],
                        "Content": row["Content"]
                    }
                    subs = row["Subsections"]

                    for i in range(len(data[1])-len(out_row)):
                        out_row[f"Subsection Level {i + 1}"] = subs[i] if i < len(subs) else ""
                    writer.writerow(out_row)
            logging.info(f"CSV file {self.path} created with {len(data[0])} rows.")
        except Exception as e:
            import pdb
            pdb.set_trace()
            logging.error(f"Error writing CSV: {e}")


client_registry.register('csv', CSVToXMLWriteClient)
