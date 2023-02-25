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




myxml = "<?xml version="1.0"?>
<actors xmlns:fictional="http://characters.example.com"
        xmlns="http://people.example.com">
    <actor type='T1'>
        <name>John Cleese</name>
        <fictional:character>Lancelot</fictional:character>
        <fictional:character>Archie Leach</fictional:character>
    </actor>
    <actor type='T2'>
        <name>Eric Idle</name>
        <fictional:character>Sir Robin</fictional:character>
        <fictional:character>Gunther</fictional:character>
        <fictional:character>Commander Clement</fictional:character>
    </actor>
</actors>"

myparsed = ET.fromstring(myxml)
ns = {
    'ns'         : 'http://people.example.com',
    'fictional': 'http://characters.example.com'
}


for prefix, uri in ns.items():
    ET.register_namespace(prefix, uri)
    
    
mynamespaces = root.findall('xmlns:eml', root)
for n in mynamespaces: 
    print(n)

import xmltodict
import pprint
with open('C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/2022_NCRN_forest_vegetation_metadata.xml', 'r', encoding='utf-8') as file:
    my_xml = file.read()
    
my_dict = xmltodict.parse(my_xml)
