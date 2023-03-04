from collections import OrderedDict # https://realpython.com/python-ordereddict/#:~:text=Python's%20OrderedDict%20is%20a%20dict,then%20the%20order%20remains%20unchanged.
import xmltodict
from dicttoxml import dicttoxml
import emld
import importlib
import json
from xml.dom.minidom import parseString
import iso639
import urllib
importlib.reload(emld)
myemld = emld.Emld(filepath = myfile, NPS = True)
myemld.set_publisher(org_name = 'mytestorg', street_address = 'The big apple', URL = "a test url", zip_code = '123123')

'''
A mock workflow to test pyEML
'''
# instantiate an emld object
myfile = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/2022_NCRN_forest_vegetation_metadata.xml'
myemld = emld.Emld(filepath = myfile, NPS = True)

# test describe methods
myemld.describe_int_rights()
myemld.describe_cui()

# test `set_CUI()` (controlled unclassified information) attribute and value
myemld.set_cui(cui_code="PUBLIC", force = True)
print(xmltodict.unparse(myemld.emld["additionalMetadata"], pretty=True)) # test that the method worked

# test `set_title()` set dataset title value
myemld.emld["dataset"]["title"]
myemld.set_title(data_package_title = "my new title")
myemld.emld["dataset"]["title"]

# test `set_int_rights()` to set intellectual rights
myemld.set_int_rights(license = "CCzero", force = True)
myemld.set_int_rights(license = "pub_domain", force = True)
myemld.set_int_rights(license = "restrict", force = False)
myemld.set_int_rights(license = "restrict", force = True)

# test `set_doi()`
myemld.emld["dataset"]["alternateIdentifier"] # is there an identifier now?
myemld.set_doi('1234567', force = False) # set the identifier
myemld.emld["dataset"]["alternateIdentifier"] # confirm set
myemld.set_doi('7654321', force = False) # choose n to NOT overwrite. interactive, should prompt user for y/n to overwrite
myemld.emld["dataset"]["alternateIdentifier"] # confirm
myemld.set_doi('7654321', force = False) # choose y to overwrite. interactive, should prompt user for y/n to overwrite
myemld.emld["dataset"]["alternateIdentifier"] # confirm
myemld.set_doi('1234567', force = True) # silently overwrite with `force`
myemld.set_doi('123', force = True) # try short value, should error
myemld.set_doi('123456a', force = True) # try to include letter
myemld.set_doi(1234567, force = True) # try giving it a number, should error

# test `set_drr()`
print(json.dumps(myemld.emld["dataset"]["usageCitation"], indent=4, default=str))
myemld.set_drr(drr_ref_id = '2293234', drr_title = 'Data Release Report for Data Package 1234')
myemld.set_drr(drr_ref_id = '1234567', drr_title = 'Data Release Report for Data Package abc', force = True)
myemld.set_drr(drr_ref_id = '1234567', drr_title = 'Data Release Report for Data Package abc', force = False)
myemld.set_drr(drr_ref_id = '7777777', drr_title = 'Data Release Report for Data Package 77', force = True)

# test `set_language()`
myemld.emld["dataset"]["language"]
myemld.set_language()

# test `set_content_units()`
myemld.set_content_units('ACAD', 'GLAC', force = True, verbose = False)

# test `set_abstract()`
my_abstract = 'This is the first sentence that describes my dataset. This is another sentence about the dataset.'
myemld.set_abstract(abstract = my_abstract, force = True)
my_abstract2 = 'This is a different abstract'
myemld.set_abstract(abstract = my_abstract2, force = False)
myemld.set_abstract(abstract = my_abstract, force = True)

# test `set_publisher()`
myemld.emld[]
myemld.set_publisher(street_address = '123 Abc street', city = 'The big apple')

# print the eml to console
myemld.print_eml()

# write the eml to file
myemld.write_eml(destination_filename="sandbox/mytestoutput2.xml")

mytest = languages.get(name = 'English')
mytest = languages.name
