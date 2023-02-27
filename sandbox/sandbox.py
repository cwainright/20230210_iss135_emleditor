#----- a python sandbox

reticulate::use_condaenv("iss135_emleditor")
reticulate::repl_python()

from collections import OrderedDict # https://realpython.com/python-ordereddict/#:~:text=Python's%20OrderedDict%20is%20a%20dict,then%20the%20order%20remains%20unchanged.
import xmltodict

"""Start a metadata object"""
py_metadata = OrderedDict(zip(r.names_r_metadata, [None]*len(r.r_metadata))) # empty metadata object with named & ordered elements
py_metadata["@context"] = dict(zip(r.names_r_metadata_context, [None]*len(r.names_r_metadata_context))) # add sub-elements to metadata object

"""Read xml to dictionary"""
with open('C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/2022_NCRN_forest_vegetation_metadata.xml', 'r', encoding='utf-8') as file:
    py_xml = file.read()
    my_dict = xmltodict.parse(py_xml)
    
"""Functions that parse xml to metadata object"""
def xmlns_vocab(py_metadata, my_dict):
    '''Assigns a value to py_metadata["@context"]["@vocab"]'''
    if my_dict["eml:eml"]["@xmlns:eml"][-1:] != '/':
      py_metadata["@context"]["@vocab"] = my_dict["eml:eml"]["@xmlns:eml"] + '/' 
      return py_metadata
    if my_dict["eml:eml"]["@xmlns:eml"][-1:] == '/':
      py_metadata["@context"]["@vocab"] = my_dict["eml:eml"]["@xmlns:eml"]
      return py_metadata
py_metadata = xmlns_vocab(py_metadata, my_dict) # call function to parse xml to metadata

def xmlns_eml(py_metadata, my_dict):
    '''Assign a value to py_metadata["@context"]["eml"]'''
    if my_dict["eml:eml"]["@xmlns:eml"][-1:] != '/':
      py_metadata["@context"]["eml"] = my_dict["eml:eml"]["@xmlns:eml"] + '/' 
      return py_metadata
    if my_dict["eml:eml"]["@xmlns:eml"][-1:] == '/':
      py_metadata["@context"]["eml"] = my_dict["eml:eml"]["@xmlns:eml"]
      return py_metadata
py_metadata = xmlns_eml(py_metadata, my_dict) # call function to parse xml to metadata

def xmlns_xsi(py_metadata, my_dict):
    '''Assign a value to py_metadata["@context"]["xsi"]'''
    if my_dict["eml:eml"]["@xmlns:xsi"][-1:] != '/':
      py_metadata["@context"]["xsi"] = my_dict["eml:eml"]["@xmlns:xsi"] + '/' 
      return py_metadata
    if my_dict["eml:eml"]["@xmlns:xsi"][-1:] == '/':
      py_metadata["@context"]["xsi"] = my_dict["eml:eml"]["@xmlns:xsi"]
      return py_metadata
py_metadata = xmlns_xsi(py_metadata, my_dict) # call function to parse xml to metadata

def xmlns_xml(py_metadata, my_dict):
    '''Assign a value to py_metadata["@context"]["xml"]'''
    py_metadata["@context"]["xml"] = "http://www.w3.org/XML/1998/namespace"
    # This is hard-coded because this value does not exist in the original xml and I haven't been able to trace where emld::as_emld() is pulling this value from.
    # emld::as_emld() defines namespaces by calling emld::eml_ns() which is defined at line 50 here: https://github.com/ropensci/emld/blob/master/R/eml_version.R
    # 1998 is not defined (i.e., hard-coded or otherwise pointed to) in emld::eml_ns()
    # 1998 is not present in the original xml `r_original_xml` or `py_xml` for emld::eml_ns() to point to (i.e., `grepl("1998", as.character(r_original_xml)) == FALSE`),
    # I have no choice but to hard-code this value until I can figure out how library(emld) is finding a value for ["@context"]["xml"].
    return py_metadata
py_metadata = xmlns_xml(py_metadata, my_dict) # call function to parse xml to metadata

def xmlns_stmml(py_metadata, my_dict):
    '''Assign a value to py_metadata["@context"]["stmml"]'''
    py_metadata["@context"]["stmml"] = my_dict["eml:eml"]["@xmlns:stmml"]
    return py_metadata
py_metadata = xmlns_stmml(py_metadata, my_dict) # call function to parse xml to metadata

def xmlns_id(py_metadata, my_dict):
    '''Assign a value to py_metadata["@context"]["id"]'''
    py_metadata["@context"]["id"] = "@id"
    return py_metadata
py_metadata = xmlns_id(py_metadata, my_dict) # call function to parse xml to metadata

def xmlns_base(py_metadata, my_dict):
    '''Assign a value to py_metadata["@context"]["@base"]'''
    py_metadata["@context"]["@base"] = "eml://"
    return py_metadata
py_metadata = xmlns_base(py_metadata, my_dict) # call function to parse xml to metadata

"""
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

from lxml import etree
root = etree.Element("root")
print(root.tag)

mywtf = etree.parse('C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/2022_NCRN_forest_vegetation_metadata.xml')
myroot = mywtf.getroot()

xmlFile = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/2022_NCRN_forest_vegetation_metadata.xml'
with open(xmlFile) as fobj:
    xml = fobj.read()

root = etree.fromstring(xml)
root.getchildren()

