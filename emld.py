# a constructor for class Emld

from collections import OrderedDict # https://realpython.com/python-ordereddict/#:~:text=Python's%20OrderedDict%20is%20a%20dict,then%20the%20order%20remains%20unchanged.
import xmltodict

# define static assets
NAMES_METADATA = ("@context", "@type", "additionalMetadata", "dataset", "packageId", "schemaLocation", "system") # top-level elements, determined by examining R object produced by EML::read_eml()
NAMES_METADATA_CONTEXT = ("@vocab", "eml", "xsi", "xml", "stmml", "id", "@base")

class Emld:
    """Create an object that holds metadata extracted from an EML-formatted xml file"""
    
    def __init__(self, filepath:str):
        """Constructor for class Emld"""
        assert file != "", "File cannot be blank"
        assert file.lower().endswith(".xml"), "File must end with '.xml'"
        """Read xml to dictionary"""
        with open(filepath, 'r', encoding='utf-8') as file:
            py_xml = file.read()
            my_dict = xmltodict.parse(py_xml)
        
        self.emld = OrderedDict(zip(NAMES_METADATA, [None]*len(NAMES_METADATA))) # empty metadata object with named & ordered elements
        self.emld["@context"] = dict(zip(NAMES_METADATA_CONTEXT, [None]*len(NAMES_METADATA_CONTEXT))) # add sub-elements to metadata object
        print("Emld instance created!")
        

