import xml.etree.cElementTree as ET
from collections import defaultdict
from functools import reduce
from parser import parse_tag
import re
from pprint import pprint
import json

OSMFILE = 'singapore.osm'
tag_amenity = 'amenity'

mapping = {
    'carpark'   : 'parking',
    'coffeeshop': 'cafe',
    'internet cafe': 'cafe',
    'deli': 'food_court',
    'Mail drop': 'post_box',
    'childcare': 'childcare_centre',
    'bar;restaurant': 'bar',
    'restaurant;taxi': 'taxi'
}


def audit_amenity(osm_file):
    return set(parse_tag(osm_file, tag_amenity))


def update_amenity(amenity):
    return mapping.get(amenity, amenity).lower().replace(' ', '_')


if __name__ == '__main__':
    set_amenity = audit_amenity(OSMFILE)
    pprint(set_amenity)