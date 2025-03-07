import re
import logging
from typing import Dict, Any, List
from .transformer import Transformer

# Configure logging.
logging.basicConfig(
    level=logging.INFO,
    format="xml_transformer %(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


class XMLTransformer(Transformer):

    def transform(self, root):
        """
        Parse the XML tree starting at root, extracting rows with hierarchy and content and headers.

        :param root: The root ElementTree element.
        :return: List of : List of rows (each a dict with keys "hierarchy" and "content") and list of column headers.
        """
        rows = self.process_element(root[0]['root'], [])
        logging.info(f"Extracted {len(rows)} rows from XML.")
        return self.parse_rows(rows)

    def extract_text(self, elem):
        text = " ".join(elem.itertext())
        text = re.sub(r'\s+', ' ', text)
        text = text.replace(",", ";")
        # text = re.sub(r'[\r\n]+', ' ', text)
        return text.strip()

    def convert_table_to_markdown(self, table_elem):
        """
        Convert an XML table element into a Markdown formatted table text.

        :param table_elem: ElementTree element representing a table.
        :return: A single-line Markdown string representing the table.
        Source: https://stackoverflow.com/questions/47048906/convert-markdown-tables-to-html-tables-using-python/47049406
        Basically reverse of the above logic
        """
        lines = []
        headers = []

        # Use XPath search to find the <thead> even if nested within <tgroup>
        thead = table_elem.find('.//thead')
        if thead is not None:
            header_row = thead.find('.//row')
        else:
            # If no thead, take the first <row> found anywhere
            header_row = table_elem.find('.//row')

        if header_row is not None:
            for cell in list(header_row):
                headers.append(self.extract_text(cell))
        if headers:
            header_line = "| " + " | ".join(headers) + " |"
            boundary_line = "| " + " | ".join(["---"] * len(headers)) + " |"
            lines.extend([header_line, boundary_line])

        # Process body rows by searching for <tbody> regardless of nesting
        tbody = table_elem.find('.//tbody')
        if tbody is not None:
            rows_table = tbody.findall('.//row')
        else:
            # If no tbody is present, take all <row> elements and skip the header row if necessary.
            rows_table = table_elem.findall('.//row')
            if header_row is not None and rows_table:
                rows_table = [row for row in rows_table if row is not header_row]

        for row in rows_table:
            # Extract text from each cell of the row.
            cells = [self.extract_text(cell) for cell in list(row)]
            row_line = "| " + " | ".join(cells) + " |"
            lines.append(row_line)

        # Return a single-line Markdown string by joining with a space.
        return "\n".join(lines)

    def process_element(self, elem, hierarchy=None):
        """
        Recursively traverse the XML tree and extract content with its hierarchical path.

        For each element:
          - Build the hierarchy as a list.
          - If the element is a table, convert it to Markdown.
          - Otherwise, extract its text using extract_text.
          - Recursively process child elements.

        :param elem: The current ElementTree element.
        :param hierarchy: List of strings representing the hierarchy up to this element.
        :return: A list of rows. Each row is a dict with keys:
                 "hierarchy": a list of strings,
                 "content": the extracted and processed text.
        """
        if hierarchy is None:
            hierarchy = []
        rows = []

        header = elem.tag
        current_hierarchy = hierarchy + [header]

        # Extracting the content: if element is a table, convert it; else, get its text.
        if elem.tag.lower() == "table":
            content = self.convert_table_to_markdown(elem)
        else:
            content = self.extract_text(elem)

        if content:
            rows.append({"hierarchy": current_hierarchy, "content": content})

        # Recurse for child elements.
        for child in list(elem):
            rows.extend(self.process_element(child, current_hierarchy))
        return rows

    def parse_rows(self, rows: List[Dict[str, any]]) -> (List[Dict[str, any]], List[str]):
        """
        Transform raw rows into a format ready for CSV writing.

        Each raw row is expected to be a dict with:
          - "hierarchy": a list of strings (e.g. ["Section", "Subsection", "NestedSubsection"])
          - "content": a string.

        This transformation produces a new dict with:
          - "Section": the first element of the hierarchy.
          - "CombinedSubsection": the remaining hierarchy joined by " > ".
          - "Subsection Level 1", "Subsection Level 2", etc.: each nested level in a separate column.
          - "Content": the text content.

        Returns:
          A list [processed_rows, fieldnames] where processed_rows is the list of dictionaries
          and fieldnames is the list of CSV column names.
        """
        processed_rows = []
        max_sub_levels = 0
        for row in rows:
            hierarchy = row["hierarchy"]
            section = hierarchy[0] if hierarchy else ""
            subsections = hierarchy[1:]  # nested subsections
            combined = " > ".join(subsections) if subsections else ""
            if len(subsections) > max_sub_levels:
                max_sub_levels = len(subsections)
            processed_rows.append({
                "Section": section,
                "CombinedSubsection": combined,
                "Subsections": subsections,
                "Content": row["content"]
            })

        fieldnames = ["Section", "CombinedSubsection"]
        for i in range(max_sub_levels):
            fieldnames.append(f"Subsection Level {i + 1}")
        fieldnames.append("Content")
        logging.info(f"Transformed {len(processed_rows)} rows with maximum {max_sub_levels} nested levels.")
        return [processed_rows, fieldnames]