#----- a python sandbox

# https://docs.python.org/3/library/xml.etree.elementtree.html

import xml.etree.ElementTree as ET
tree = ET.parse('sandbox/2022_NCRN_forest_vegetation_metadata.xml')
root = tree.getroot()
root
root.tag
root.attrib
root[0][0].text

# xml closely resembles an R list; a tree structure 

# this is the core data structure
# A dictionary containing dictionaries is roughly equivalent to an R list()
# https://stackoverflow.com/questions/50731319/python-equivalent-of-r-list
mymetadata = {
    "dataset": {"title": "my title here", "creator": "the title creator here"}
    } 
# An R list 
mymetadata['dataset']['title']
list(mymetadata)[0]

mymetadata = list(mymetadata)
mymetadata[0]


py_my_metadata = {
    "@context": None,
    "@type": None,
    "additionalMetadata": None,
    "dataset": None,
    "packageId": None,
    "schemaLocation": None,
    "system": None
    } 
