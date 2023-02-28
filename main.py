from collections import OrderedDict # https://realpython.com/python-ordereddict/#:~:text=Python's%20OrderedDict%20is%20a%20dict,then%20the%20order%20remains%20unchanged.
import xmltodict
import emld
import importlib
importlib.reload(emld)

'''
A mock workflow to test how py_emleditor
'''
myfile = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/2022_NCRN_forest_vegetation_metadata.xml'
mywrongfile = "myworkbook.xlsx"
myemld = emld.Emld(filepath = myfile)



mycar = emld.Car(make="mycar", model="mymodel")

