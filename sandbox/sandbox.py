#----- a python sandbox

# https://docs.python.org/3/library/xml.etree.elementtree.html

import xml.etree.ElementTree as ET
tree = ET.parse('sandbox/2022_NCRN_forest_vegetation_metadata.xml')
root = tree.getroot()
root
root.tag
root.attrib
root[0][0].text
