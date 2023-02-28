from collections import OrderedDict # https://realpython.com/python-ordereddict/#:~:text=Python's%20OrderedDict%20is%20a%20dict,then%20the%20order%20remains%20unchanged.
import xmltodict
import dicttoxml
import emld
import importlib
importlib.reload(emld)

'''
A mock workflow to test how py_emleditor
'''
myfile = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/2022_NCRN_forest_vegetation_metadata.xml'
myemld = emld.Emld(filepath = myfile)


myemld.set_cui(eml_object=myemld, cui_code="abc", force=True, NPS=True)

mytestoutput = dicttoxml.dicttoxml(myemld)


