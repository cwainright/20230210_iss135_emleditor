# a constructor for class Emld

from collections import OrderedDict # https://realpython.com/python-ordereddict/#:~:text=Python's%20OrderedDict%20is%20a%20dict,then%20the%20order%20remains%20unchanged.
import xmltodict
import dicttoxml

# define static assets outside of class instances
NAMES_METADATA = ("@context", "@type", "additionalMetadata", "dataset", "packageId", "schemaLocation", "system") # top-level elements, determined by examining R object produced by EML::read_eml()
NAMES_METADATA_CONTEXT = ("@vocab", "eml", "xsi", "xml", "stmml", "id", "@base")

class Emld:
    """Create an object that holds metadata extracted from an EML-formatted xml file"""
    
    def __init__(self, filepath:str):
        """Constructor for class Emld"""
        assert filepath != "", "File cannot be blank"
        assert filepath.lower().endswith(".xml"), "File must end with '.xml'"
        
        # read user-provided xml to dictionary for parsing
        with open(filepath, 'r', encoding='utf-8') as file:
            py_xml = file.read()
            my_dict = xmltodict.parse(py_xml)
        
        # create empty dictionary with correct element names
        self.emld = OrderedDict(zip(NAMES_METADATA, [None]*len(NAMES_METADATA))) # empty metadata object with named & ordered elements
        self.emld["@context"] = dict(zip(NAMES_METADATA_CONTEXT, [None]*len(NAMES_METADATA_CONTEXT))) # add sub-elements to metadata object
        
        '''Parse user-provided xml to dictionary'''
        # Assign a value to self.emld["@context"]["@vocab"]
        if my_dict["eml:eml"]["@xmlns:eml"][-1:] != '/':
            self.emld["@context"]["@vocab"] = my_dict["eml:eml"]["@xmlns:eml"] + '/' 
        else:
            self.emld["@context"]["@vocab"] = my_dict["eml:eml"]["@xmlns:eml"]
            
        # Assign a value to self.emld["@context"]["eml"]
        if my_dict["eml:eml"]["@xmlns:eml"][-1:] != '/':
            self.emld["@context"]["eml"] = my_dict["eml:eml"]["@xmlns:eml"] + '/' 
        else:
            self.emld["@context"]["eml"] = my_dict["eml:eml"]["@xmlns:eml"]
            
        # Assign a value to self.emld["@context"]["xsi"]
        if my_dict["eml:eml"]["@xmlns:xsi"][-1:] != '/':
            self.emld["@context"]["xsi"] = my_dict["eml:eml"]["@xmlns:xsi"] + '/' 
        else:
            self.emld["@context"]["xsi"] = my_dict["eml:eml"]["@xmlns:xsi"]
          
        # Assign a value to self.emld["@context"]["xml"]
        self.emld["@context"]["xml"] = "http://www.w3.org/XML/1998/namespace"
        '''
        This is hard-coded because this value does not exist in the original xml and I haven't been able to trace where emld::as_emld() is pulling this value from.
        emld::as_emld() defines namespaces by calling emld::eml_ns() which is defined at line 50 here: https://github.com/ropensci/emld/blob/master/R/eml_version.R
        1998 is not defined (i.e., hard-coded) in emld::eml_ns(), which tells me it's not a default value defined in the package library(emld)
        1998 is also not present in the original xml `r_original_xml` or `py_xml` for emld::eml_ns() to point to (i.e., `grepl("1998", as.character(r_original_xml)) == FALSE`)
        which tells me emld::as_emld() isn't pulling this value from the user-provided xml
        the remaining option is that emld::as_emld() is pointing to a remote for this value
        Since I haven't traced where this remote is located,
        I have no choice but to hard-code this value until I can figure out how library(emld) is finding a value for ["@context"]["xml"].
        '''
        # Assign a value to self.emld["@context"]["stmml"]
        self.emld["@context"]["stmml"] = my_dict["eml:eml"]["@xmlns:stmml"]
        
        # Assign a value to self.emld["@context"]["id"]
        self.emld["@context"]["id"] = "@id"
        
        # Assign a value to self.emld["@context"]["@base"]
        self.emld["@context"]["@base"] = "eml://"
        
        # Assign a value to self.emld["dataset"]
        self.emld["dataset"] = my_dict["eml:eml"]["dataset"]
        
        # Assign a value to self.emld["additionalMetadata"]
        self.emld["additionalMetadata"] = my_dict["eml:eml"]["additionalMetadata"]
        
        # Assign a value to self.emld["packageId"]
        self.emld["packageId"] = my_dict["eml:eml"]["@packageId"]
        
        # Assign a value to self.emld["schemaLocation"]
        self.emld["schemaLocation"] = my_dict["eml:eml"]["@xsi:schemaLocation"]
        
        # Assign a value to self.emld["schemaLocation"]
        self.emld["system"] = my_dict["eml:eml"]["@system"]
        
        # Assign a value to self.emld["@context"]["@base"]
        self.emld["@type"] = "EML"
        
        self.__class__ = collections.OrderedDict
        
        print("Emld instance created!")
        
    def set_cui(self, cui_code = ("PUBLIC", "NOCON", "DL_ONLY", "FEDCON", "FED_ONLY"), force = False, NPS = True):
        '''Setter function for controlled unclassified information (CUI)'''
        # @param cui_code a string consisting of one of 7 potential CUI codes (defaults to "PUBFUL").
            # FED_ONLY - Contains CUI. Only federal employees should have access (similar to "internal only" in DataStore)
            # FEDCON - Contains CUI. Only federal employees and federal contractors should have access (also very much like current "internal only" setting in DataStore)
            # DL_ONLY - Contains CUI. Should only be available to a names list of individuals (where and how to list those individuals TBD)
            # NOCON - Contains  CUI. Federal, state, local, or tribal employees may have access, but contractors cannot.
            # PUBLIC - Does NOT contain CUI.
        
        # verify CUI code entry; stop if does not equal one of six valid codes listed above:
        assert cui_code in ("PUBLIC", "NOCON", "DL_ONLY", "FEDCON", "FED_ONLY"), 'You must choose a cui_code from the pick-list: ("PUBLIC", "NOCON", "DL_ONLY", "FEDCON", "FED_ONLY")'
        self.emld["dataset"]["title"] = cui_code

