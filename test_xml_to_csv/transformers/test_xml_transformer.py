import unittest
import xml.etree.ElementTree as ET
import logging
from xml_to_csv.transformers.xml_transformer import XMLTransformer


class TestXMLTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = XMLTransformer()

    def test_extract_text(self):
        xml_string = '<root>John, <child>Deer</child>!</root>'
        elem = ET.fromstring(xml_string)
        extracted = self.transformer.extract_text(elem)
        self.assertEqual(extracted, "John; Deer !")

    def test_convert_table_to_markdown(self):
        sample_table = '''
        <table>
            <tgroup>
                <thead>
                    <row>
                        <entry><para>ABCD</para></entry>
                        <entry><para>EFGH</para></entry>
                    </row>
                </thead>
                <tbody>
                    <row>
                        <entry><para>KLMN</para></entry>
                        <entry><para>OPQR</para></entry>
                    </row>
                    <row>
                        <entry><para>UVW</para></entry>
                        <entry><para>XYZ</para></entry>
                    </row>
                </tbody>
            </tgroup>
        </table>
        '''
        table_elem = ET.fromstring(sample_table)
        markdown = self.transformer.convert_table_to_markdown(table_elem)
        expected = ("| ABCD | EFGH |\n"
                    "| --- | --- |\n"
                    "| KLMN | OPQR |\n"
                    "| UVW | XYZ |")
        self.assertEqual(markdown, expected)

    def test_process_element(self):
        # Create a simple XML with nested structure, including a table.
        xml_string = '''
        <root>
            <section>Section A</section>
            <table>
                <tgroup>
                    <thead>
                        <row>
                            <entry><para>ABC</para></entry>
                        </row>
                    </thead>
                    <tbody>
                        <row>
                            <entry><para>DEF</para></entry>
                        </row>
                    </tbody>
                </tgroup>
            </table>
        </root>
        '''
        root_elem = ET.fromstring(xml_string)
        rows = self.transformer.process_element(root_elem)
        section_found = any("section" in [tag.lower() for tag in row["hierarchy"]]
                            and "Section A" in row["content"] for row in rows)
        table_found = any("table" in [tag.lower() for tag in row["hierarchy"]]
                          and "ABC" in row["content"] and "DEF" in row["content"] for row in rows)
        self.assertTrue(section_found)
        self.assertTrue(table_found)

    def test_parse_rows(self):
        sample_rows = [
            {"hierarchy": ["A", "B", "C"], "content": "Test Content"},
            {"hierarchy": ["A", "D"], "content": "Another Content"}
        ]
        processed, fieldnames = self.transformer.parse_rows(sample_rows)
        expected_fieldnames = ["Section", "CombinedSubsection", "Subsection Level 1", "Subsection Level 2", "Content"]
        self.assertEqual(fieldnames, expected_fieldnames)
        row1 = processed[0]
        self.assertEqual(row1["Section"], "A")
        self.assertEqual(row1["CombinedSubsection"], "B > C")
        self.assertEqual(row1["Content"], "Test Content")
        row2 = processed[1]
        self.assertEqual(row2["Section"], "A")
        self.assertEqual(row2["CombinedSubsection"], "D")
        self.assertEqual(row2["Content"], "Another Content")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
