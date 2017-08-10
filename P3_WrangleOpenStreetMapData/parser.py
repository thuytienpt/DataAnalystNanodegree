import xml.etree.cElementTree as ET
from pprint import pprint

# def is_singapore(elem):
#     return (not elem.findall('.//tag[@k="addr:country"]')
#             ) or elem.findall('.//tag[@v="SG"]')


def is_chosen_tag(elem):
    return elem.tag in ['node', 'way']


def parse_tag(osm_file, attrib):
    values = []
    for event, elem in ET.iterparse(osm_file, events=('start', )):
        if is_chosen_tag(elem):
            # if is_chosen_tag(elem) and is_singapore(elem):
            for tag in elem.iter('tag'):
                if tag.attrib['k'] == attrib:
                    values.append(tag.attrib['v'])
    return values
