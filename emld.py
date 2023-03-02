# a constructor for class Emld

from collections import OrderedDict # https://realpython.com/python-ordereddict/#:~:text=Python's%20OrderedDict%20is%20a%20dict,then%20the%20order%20remains%20unchanged.
import xmltodict
import dicttoxml
from xml.dom.minidom import parseString
import importlib

# constants for __init__()
NAMES_METADATA = ("@context", "@type", "additionalMetadata", "dataset", "packageId", "schemaLocation", "system") # top-level elements, determined by examining R object produced by EML::read_eml()
NAMES_METADATA_CONTEXT = ("@vocab", "eml", "xsi", "xml", "stmml", "id", "@base")

class Emld():
    """An object that holds metadata extracted from an EML-formatted xml file"""
    
    def __init__(self, filepath:str):
        """Constructor for class Emld"""
        # @param filepath
            # a string containing the filepath and filename, including file extension, of the .xml file generated by EML
            # valid EML is usually generated from an R tool like library(EML)
            
        # validate user input
        assert filepath != "", "File cannot be blank"
        assert filepath.lower().endswith(".xml"), "File must end with '.xml'"
        
        # procedure
        try:
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
              
            self.emld["@context"]["xml"] = "http://www.w3.org/XML/1998/namespace" # Assign a value to self.emld["@context"]["xml"]
            '''
            ["@context"]["xml"] is hard-coded because 1998 does not exist in the original xml and I haven't been able to trace where emld::as_emld() is pulling this value from.
            emld::as_emld() defines namespaces by calling emld::eml_ns() which is defined at line 50 here: https://github.com/ropensci/emld/blob/master/R/eml_version.R
            1998 is not defined (i.e., hard-coded) in emld::eml_ns(), which tells me it's not a default value defined in the package library(emld)
            1998 is also not present in the original xml `r_original_xml` or `py_xml` for emld::eml_ns() to point to (i.e., `grepl("1998", as.character(r_original_xml)) == FALSE`)
            which tells me emld::as_emld() isn't pulling this value from the user-provided xml
            the remaining option is that emld::as_emld() is pointing to a remote for this value
            Since I haven't traced where this remote is located,
            I have no choice but to hard-code this value until I can figure out how library(emld) is finding a value for ["@context"]["xml"].
            '''
            self.emld["@context"]["stmml"] = my_dict["eml:eml"]["@xmlns:stmml"] # Assign a value to self.emld["@context"]["stmml"]
            self.emld["@context"]["id"] = "@id" # Assign a value to self.emld["@context"]["id"]
            self.emld["@context"]["@base"] = "eml://" # Assign a value to self.emld["@context"]["@base"]
            self.emld["dataset"] = my_dict["eml:eml"]["dataset"] # Assign a value to self.emld["dataset"]
            self.emld["additionalMetadata"] = my_dict["eml:eml"]["additionalMetadata"] # Assign a value to self.emld["additionalMetadata"]
            self.emld["packageId"] = my_dict["eml:eml"]["@packageId"] # Assign a value to self.emld["packageId"]
            self.emld["schemaLocation"] = my_dict["eml:eml"]["@xsi:schemaLocation"] # Assign a value to self.emld["schemaLocation"]
            self.emld["system"] = my_dict["eml:eml"]["@system"] # Assign a value to self.emld["schemaLocation"]
            self.emld["@type"] = "EML" # Assign a value to self.emld["@context"]["@base"]
            
            # self.emld["dataset"]["publisher"] = PUBSET # enforce class requirement: set publisher to NPS-required values
            
            # add_required(self) # enforce class Emld requirements
            self.add_required()
            # self.test_init()
            
            print("Emld instance created!") # print success message
        except:
            print("An error occurred and your Emld did not instantiate.")
            
    def test_init(self):
        print("got to test_init()")
        
    def set_cui(self, cui_code:str = ("PUBLIC", "NOCON", "DL_ONLY", "FEDCON", "FED_ONLY"), force:bool = False, NPS:bool = True):
        '''Setter function for controlled unclassified information (CUI)'''
        # @param cui_code a string consisting of one of 7 potential CUI codes (defaults to "PUBFUL").
            # FED_ONLY - Contains CUI. Only federal employees should have access (similar to "internal only" in DataStore)
            # FEDCON - Contains CUI. Only federal employees and federal contractors should have access (also very much like current "internal only" setting in DataStore)
            # DL_ONLY - Contains CUI. Should only be available to a names list of individuals (where and how to list those individuals TBD)
            # NOCON - Contains  CUI. Federal, state, local, or tribal employees may have access, but contractors cannot.
            # PUBLIC - Does NOT contain CUI.
        # @param force bool
            # Default False
            # True means the program will over-write any value in <metadata><CUI> if one exists or create that tag and add `cui_code` if !exists
            # False prints the value of <metadata><CUI> to console and asks the user to decide to over-write or not
        # @param NPS bool
            # Default True
            # True means
            # False means

        # saving in case I need to pivot to xml instead of dict
        # https://www.geeksforgeeks.org/turning-a-dictionary-into-xml-in-python/


        # verify CUI code entry; stop if does not equal one of six valid codes listed above:
        assert cui_code in ("PUBLIC", "NOCON", "DL_ONLY", "FEDCON", "FED_ONLY"), 'You must choose a `cui_code` from the pick-list: ("PUBLIC", "NOCON", "DL_ONLY", "FEDCON", "FED_ONLY")'
        assert force in (True, False), "Parameter `force` must be either True or False."
        assert NPS in (True, False), "Parameter `NPS` must be either True or False."

        # procedure
        try:
            if force == True:
                self.emld["additionalMetadata"]["metadata"]['@id'] = "CUI" # set the value of attribute "id" in <additionalMetadata id=fill_in_the_blank> with "CUI"
                self.emld["additionalMetadata"]["metadata"]["CUI"] = cui_code   # set the value of <metadata><CUI>
                print(f"Value of <CUI> set to '{cui_code}'\nParameter 'id' set to 'CUI'!")
            else:
                pass
        except:
            print("CUI did not update.")

    def set_title(self, data_package_title:str, force:bool = False, NPS:bool = True):
        # @param data_package_title str
            # The title the user wants to change their data package title to
            # e.g., data_package_title = "My new title"
        # @param force bool
            # Default False
            # True means the program will over-write any value in <metadata><CUI> if one exists or create that tag and add `cui_code` if !exists
            # False prints the value of <metadata><CUI> to console and asks the user to decide to over-write or not
        # @param NPS bool
            # Default True
            # True means
            # False means
            
        # validate user input
        assert data_package_title != "", "Parameter `data_package_title` cannot be blank"
        assert force in (True, False), "Parameter `force` must be either True or False."
        assert NPS in (True, False), "Parameter `NPS` must be either True or False."
        
        # procedure
        try:
            if force == True:
                self.emld["dataset"]["title"] = data_package_title # set the value of attribute "title"
                print(f"Value of dataset title set to '{data_package_title}'!")
            if force == False:
                if self.emld["dataset"]["title"] != None:
                    print(f'Your dataset already has a title: {self.emld["dataset"]["title"]}')
                    user_choice = input("Do you want to overwrite your original title?\n'y' then enter to overwrite or 'n' then enter to keep original title\n\n")
                    if user_choice != 'y':
                        pass
                    else:
                        self.emld["dataset"]["title"] = data_package_title
                        print(f"You overwrote your original data package title to '{data_package_title}'!")
                        
            if NPS == True:
                # need to figure out what's going on here line 50 https://github.com/nationalparkservice/EMLeditor/blob/main/R/editEMLfunctions.R
                # what are .set_npspublisher() and .set_version()?????
                # Set NPS publisher, if it doesn't already exist
                    # if (NPS == TRUE) {
                    #     eml_object <- .set_npspublisher(eml_object)
                    # }
                    # # add/update EMLeditor and version to metadata:
                    # eml_object <- .set_version(eml_object)
                pass
            else:
                pass
        except:
            print("Title did not update.")
        
    # def set_int_rights(self, license:str = ("CC0", "public", "restricted"), force:bool = False, NPS:bool = True):
    #     # @param license str
    #         # The intellectual rights the user wants to set for their data package
    #         # e.g., data_package_title = "My new title"
    #     # @param force bool
    #         # Default False
    #         # True means the program will over-write any value in <metadata><CUI> if one exists or create that tag and add `license` if !exists
    #         # False prints the value of <metadata><CUI> to console and asks the user to decide to over-write or not
    #     # @param NPS bool
    #         # Default True
    #         # True means
    #         # False means
    #         
    #     license_text = {
    #         'CCzero': 'This product is released to the "public domain" under Creative Commons CC0 1.0 No Rights Reserved (see: https://creativecommons.org/publicdomain/zero/1.0/).',
    #         'pub_domain': 'This product is released to the "public domain" under U.S. Government Works No Rights Reserved (see: http://www.usa.gov/publicdomain/label/1.0/).',
    #         'restrict' <- 'This product has been determined to contain Controlled Unclassified Information (CUI) by the National Park Service, and is intended for internal use only. It is not published under an open license. Unauthorized access, use, and distribution are prohibited.'
    #     }
    #     
    #     # validate user input
    #     assert license != "", "Parameter `license` cannot be blank"
    #     assert force in (True, False), "Parameter `force` must be either True or False."
    #     assert NPS in (True, False), "Parameter `NPS` must be either True or False."
    #     
    #     # procedure
    #     try:
    #         if force == True:
    #             pass
    #         if force == False:
    #             pass
    #         if NPS == True:
    #             # need to figure out what's going on here line 50 https://github.com/nationalparkservice/EMLeditor/blob/main/R/editEMLfunctions.R
    #             # what are .set_npspublisher() and .set_version()?????
    #             # Set NPS publisher, if it doesn't already exist
    #                 # if (NPS == TRUE) {
    #                 #     eml_object <- .set_npspublisher(eml_object)
    #                 # }
    #                 # # add/update EMLeditor and version to metadata:
    #                 # eml_object <- .set_version(eml_object)
    #             pass
    #         else:
    #             pass
    #     except:
    #         print("Title did not update.")
    
    def set_npspublisher(self):
        '''set the publisher for the dataset'''
        
        PUBSET = {
            'organizationName': 'National Park Service',
            'address': {
                'deliveryPoint': '1201 Oakridge Drive, Suite 150',
                'city': 'Fort Collins',
                'administrativeArea': 'CO',
                'postalCode': '80525',
                'country': 'USA'
            },
            'onlineUrl': 'http://www.nps.gov',
            'electronicMailAddress': 'irma@nps.gov',
            'userId': {
                'directory': 'https://ror.org/',
                'userId': "https://ror.org/044zqqy65"
            }
        }
        
        # try:
        #     self.emld["dataset"]["publisher"]
        #     print(f'the publisher is {self.emld["dataset"]["publisher"]}')
        #     if self.emld["dataset"]["publisher"] != PUBSET:
        #         self.emld["dataset"]["publisher"] = PUBSET
        # except:
        #     print("Your dataset had no publisher")
        #     self.emld["dataset"]["publisher"] = PUBSET
        #     print("Your dataset's publisher has been set to the NPS default: Fort Collins IRMA")
        
        # The R version of this function is designed to ensure that the dataset always ends up with the values of `PUBSET`.
        # That version checks whether ["dataset"]["publisher"] matches `PUBSET` and then re-assigns the values if they don't match
        # Since the goal of this function is to set ["dataset"]["publisher"] to `PUBSET` I just skipped that logic
        # line 15 https://github.com/nationalparkservice/EMLeditor/blob/main/R/utils.R
        self.emld["dataset"]["publisher"] = PUBSET
        
    def set_for_by_nps(self):
        '''Set the value of ["additionalMetadata"]["metadata"]["agencyOriginated"]'''
        
        # delete context attribute from ["additionalMetadata"]
        try: # not sure why this is necessary but line 167 does this https://github.com/nationalparkservice/EMLeditor/blob/main/R/utils.R
            del self.emld["additionalMetadata"]["@context"] # delete if it exists
        except:
            pass
        
        # constants
        FOR_BY = {
            'metadata': {
                'agencyOriginated': {
                    'agency': "NPS",
                    'byOrForNPS': "TRUE"
                }
            }
        }
        FOR_BY2 = {
                'agency': "NPS",
                'byOrForNPS': "TRUE"
            }
        print("got past for_by{}")
        
        addl_md_len = len(self.emld["additionalMetadata"])
        # if ["additionalMetadata"] is empty
        if "agencyOriginated" in self.emld["additionalMetadata"]["metadata"]: # check dict keys
            pass # if agencyOriginated is already there, this step is already done so skip
        else: # otherwise, our next step depends on what's already there
            if addl_md_len == 0:
                print("len = 0")
                self.emld["additionalMetadata"] = FOR_BY # add the whole deal
            else:
                print("len >= 1")
                self.emld['additionalMetadata']["metadata"]["agencyOriginated"] = FOR_BY2 # add a shortened version of the whole deal
                
    def add_required(self):
        '''A method that enforces class Emld data requirements'''
        
        '''
        Several functions in R EMLeditor::editEMLfunctions.R (examples below) silently execute functions from EMLeditor::utils.R.
        Those hidden functions silently apply required standards to the dataset provided by a user (e.g., filling in required fields,
        like `publisher`, that the "valid EML" doesn't require but NPS does require, so earlier EML/XML validation does not enforce on user data).
        Hiding a function call inside another function and silently
        executing the hidden function is an unnecessarily convoluted way of enforcing the class rules on user data.
        
        Instead, I'm calling a method that executes these required data package changes
        from the class's `__init__()` method.
        A. This enforces the "rules" of a class instance on instantiation.
        B. It's also easier to maintain code when functions do one thing.
        
        Examples of R EMLeditor functions that update elements from other function calls:
        `set_title()` line 18 calls .set_npspublisher()` line 52 and `set_version()` line 55 https://github.com/nationalparkservice/EMLeditor/blob/main/R/editEMLfunctions.R
        `set_doi()` line 73 calls `.set_npspublisher()` line 152 and `.set_version()` line 156 https://github.com/nationalparkservice/EMLeditor/blob/main/R/editEMLfunctions.R
        `set_content_units()` line 178 calls `.set_npspublisher()` line 412 and `.set_version()` line 416 https://github.com/nationalparkservice/EMLeditor/blob/main/R/editEMLfunctions.R
        ctrl+f for ".set" shows 25 calls of hidden functions from other functions in EMLeditor::editEMLfunctions.R
        '''
        
        # procedure
        print("got into add_required()")
        self.set_npspublisher() # set publisher regardless of other params
        print("got past set_npspublisher()")
        self.set_for_by_nps() # set publisher regardless of other params
        print("got past set_for_by_nps()")
        
    def write_eml(self, destination_filename:str, attr_type:bool = False):
        '''Write emld to .xml'''
        # @param destination_filename
            # the name and filepath, including the .xml file extension, where the Emld.emld should be saved
        # @param attr_type
            # default value is False
            # True adds an attribute to every xml tag that specifies the data type stored in that tag
            # e.g., If a tag holds string data (str), its tag might be this: <mytag type="str">
            # False omits the attribute tag like this: <mytag>
            
        # validate user input
        assert destination_filename != "", "File cannot be blank"
        assert destination_filename.lower().endswith(".xml"), "File must end with '.xml'"
        assert attr_type in (True, False), "Parameter `attr_type` must be either True or False."
        
        # procedure
        try:
            xmloutput = dicttoxml.dicttoxml(self.emld, attr_type = attr_type)
            xml_decode = xmloutput.decode()
            xmlfile = open(destination_filename, "w")
            xmlfile.write(xml_decode)
            xmlfile.close()
        except:
            print("Unable to write eml to xml.")
        
    def print_eml(self, attr_type:bool = False):
        '''Pretty-print xml to console'''
        # @param attr_type
            # default value is False
            # True adds an attribute to every xml tag that specifies the data type stored in that tag
            # e.g., If a tag holds string data (str), its tag might be this: <mytag type="str">
            
        # validate user input
        assert attr_type in (True, False), "Parameter `attr_type` must be either True or False."
        
        # procedure
        try:
            xmloutput = dicttoxml.dicttoxml(self.emld, attr_type = attr_type)
            print(parseString(xmloutput).toprettyxml())
            # eventually, update to:
            # print(xmltodict.unparse(myemld.emld["additionalMetadata"], pretty=True))
        except:
            print("error in printing eml")
            
        '''
        Eventually, we're going to need to adjust the way we print tag attributes to match the EML spec.
        We need to duplicate <additionalMetadata><metadata> tags from myemld.emld["additionalMetadata"]["metadata"] to look like this:
            
        <additionalMetadata id="CUI">
            <metadata>
                <CUI>PUBLIC</CUI>
            </metadata>
        </additionalMetadata>
        <additionalMetadata>
            <metadata>
                <emlEditor>
                    <app>EMLassemblyline</app>
                    <release>3.5.5</release>
                </emlEditor>
            </metadata>
        </additionalMetadata>
        
        Our current data structure would omit the id attribute and fail to duplicate tags and would look like this:
            
        <additionalMetadata>
            <metadata>
                <CUI>PUBLIC</CUI>
                <emlEditor>
                    <app>EMLassemblyline</app>
                    <release>3.5.5</release>
                </emlEditor>
            </metadata>
        </additionalMetadata>
        
        To overcome this, we'll duplicate tags and assign attribute "id" a value by looping over our dictionary like this:
        for thing in myemld.emld["additionalMetadata"]["metadata"]:
            if thing != 'emlEditor':
                print(thing)
        where a "thing" is the value of the `id` attribute and we duplicate <additionalMetadata><metadata> len(myemld.emld["additionalMetadata"]["metadata"]) times
        in R we accomplish this with a for loop and xml2::xml_add_child() and xml2::xml_set_attr()
        in python it seems like we use the append method... https://stackoverflow.com/questions/43883650/insert-xml-string-from-a-dicttoxml-object-into-a-lxml-etree
        '''
    

