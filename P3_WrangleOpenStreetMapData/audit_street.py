import xml.etree.cElementTree as ET
from collections import defaultdict
from functools import reduce
from parser import parse_tag
import re
from pprint import pprint
import json

OSMFILE = 'singapore.osm'
tag_street , = 'addr:street', 

street_type_re = re.compile(r'\b[^ \d)]+\.?$', re.IGNORECASE)
number_house_re = r'(.*#([\d-]+)|(^\d+)),? '
area_re = r'(, .+)|(Blok\.? .+)$'

expected = [
    'Alley', 'Avenue', 'Boulevard', 'Central', 'Circus', 'Cirle', 'Close',
    'Crescent', 'Drive', 'Geylang', 'Grane', 'Grove', 'Hill', 'Jalan', 'Lane',
    'Link', 'Lorong', 'Path', 'Palace', 'Park', 'Place', 'Rise', 'Road',
    'Square', 'Street', 'Terrace', 'Track', 'Vale', 'View', 'Vista', 'Walk',
    'Way'
]

mapping = {
    'Ave': 'Avenue',
    'Avebune': 'Avenue',
    'Dr': 'Drive',
    'St': 'Street',
    'St.': 'Street',
    'Rd': 'Road',
    'Rd.': 'Road',
    'Roads': 'Road'
}


def audit_street_type(street_types, street_name):
    street_name = update_street_name(street_name)
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
    return street_types


def audit_street(osmfile):
    return reduce(audit_street_type, parse_tag(osmfile, tag_street), defaultdict(set))


def get_type(street_name):
    street_type = street_type_re.search(street_name)
    return (street_type and street_type.group()) or None


def update_type(street_name):
    try:
        street_type = street_type_re.search(street_name).group()
        return street_name.replace(street_type, mapping[street_type])
    except:
        return street_name


def clean_redundant(street_name):
    street_name = re.sub(number_house_re, '', street_name)
    return re.sub(area_re, '', street_name).title().replace('\n', '')


def update_street_name(street_name):
    return update_type(clean_redundant(street_name))


if __name__ == '__main__':
    st_types = audit_street(OSMFILE)
    pprint(st_types)