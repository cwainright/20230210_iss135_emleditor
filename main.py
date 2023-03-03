from collections import OrderedDict # https://realpython.com/python-ordereddict/#:~:text=Python's%20OrderedDict%20is%20a%20dict,then%20the%20order%20remains%20unchanged.
import xmltodict
from dicttoxml import dicttoxml
import emld
import importlib
from xml.dom.minidom import parseString
importlib.reload(emld)

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
myemld.set_int_rights(license = "restrict", force = True)

# print the eml to console
myemld.print_eml()

# write the eml to file
myemld.write_eml(destination_filename="sandbox/mytestoutput2.xml")




