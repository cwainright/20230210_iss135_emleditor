#----- a python sandbox

reticulate::use_condaenv("iss135_emleditor")
reticulate::repl_python()

from collections import OrderedDict # https://realpython.com/python-ordereddict/#:~:text=Python's%20OrderedDict%20is%20a%20dict,then%20the%20order%20remains%20unchanged.
import xmltodict

"""Start a metadata object"""
# define static assets
NAMES_METADATA = ("@context", "@type", "additionalMetadata", "dataset", "packageId", "schemaLocation", "system") # top-level elements, determined by examining R object produced by EML::read_eml()
NAMES_METADATA_CONTEXT = ("@vocab", "eml", "xsi", "xml", "stmml", "id", "@base")

py_metadata = OrderedDict(zip(NAMES_METADATA, [None]*len(NAMES_METADATA))) # empty metadata object with named & ordered elements
py_metadata["@context"] = dict(zip(NAMES_METADATA_CONTEXT, [None]*len(NAMES_METADATA_CONTEXT))) # add sub-elements to metadata object

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
    # 1998 is not defined (i.e., hard-coded) in emld::eml_ns(), which tells me it's not a default value defined in the package library(emld)
    # 1998 is also not present in the original xml `r_original_xml` or `py_xml` for emld::eml_ns() to point to (i.e., `grepl("1998", as.character(r_original_xml)) == FALSE`)
    # which tells me emld::as_emld() isn't pulling this value from the user-provided xml
    # the remaining option is that emld::as_emld() is pointing to a remote for this value
    # Since I haven't traced where this remote is located,
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

def dataset(py_metadata, my_dict):
    '''Assign a value to py_metadata["dataset"]'''
    py_metadata["dataset"] = my_dict["eml:eml"]["dataset"]
    return py_metadata
py_metadata = dataset(py_metadata, my_dict) # call function to parse xml to metadata

def additional_metadata(py_metadata, my_dict):
    '''Assign a value to py_metadata["additionalMetadata"]'''
    py_metadata["additionalMetadata"] = my_dict["eml:eml"]["additionalMetadata"]
    return py_metadata
py_metadata = additional_metadata(py_metadata, my_dict) # call function to parse xml to metadata

def package_id(py_metadata, my_dict):
    '''Assign a value to py_metadata["packageId"]'''
    py_metadata["packageId"] = my_dict["eml:eml"]["@packageId"]
    return py_metadata
py_metadata = package_id(py_metadata, my_dict) # call function to parse xml to metadata

def schema_location(py_metadata, my_dict):
    '''Assign a value to py_metadata["schemaLocation"]'''
    py_metadata["schemaLocation"] = my_dict["eml:eml"]["@xsi:schemaLocation"]
    return py_metadata
py_metadata = schema_location(py_metadata, my_dict) # call function to parse xml to metadata

def system(py_metadata, my_dict):
    '''Assign a value to py_metadata["schemaLocation"]'''
    py_metadata["system"] = my_dict["eml:eml"]["@system"]
    return py_metadata
py_metadata = system(py_metadata, my_dict) # call function to parse xml to metadata

def data_type(py_metadata, my_dict):
    '''Assign a value to py_metadata["@context"]["@base"]'''
    py_metadata["@type"] = "EML"
    return py_metadata
py_metadata = data_type(py_metadata, my_dict) # call function to parse xml to metadata

