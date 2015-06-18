import os

from libs.exceptions.FailToLoad import FailToLoad
from xml.dom import minidom
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import xml.etree.ElementTree as ET

def load_xml_document(xml_document):
    """
    Abstract: Function to load an XML document, given as parameter.
    Return the minidom object corresponding to the XML document, given as parameter.
    Exception: fail_to_load_XML_document - raised if the XML document canno't be load
    """
    try:
        #parsing with 'parse()' and conversion to XML with 'toxml()'
        return minidom.parse(xml_document).toxml()
    except Exception as excpt:
        raise FailToLoad("XML document loading failed : {0}".format(excpt))

def is_valid_XML_documents(xml_documents):
    """
    Abstract: Procedure to know if all XML files given as parameters are valid XML documents
    """

    #creation of the parser
    xml_parsing = make_parser()

    #set the ContentHandler
    xml_parsing.setContentHandler(ContentHandler())

    #verification on each document
    for doc in xml_documents:
        if os.path.isfile(doc):
            if is_a_valid_XML_document(xml_parsing, doc):
                print("{0} is a valid XML document".format(doc))
            else:
                print("{0} is not a valid XML document".format(doc))
        else:
            print("{0} is not a file".format(doc))

def is_a_valid_XML_document(xml_parsing, xml_document):
    """
    Abstract: Function to return if the parameter is a valid document
    Return a boolean to know if the parameter is a valid document
    """

    try:
        xml_parsing.parse(xml_document)
    except Exception as excpt:
        print(excpt)
        return False

    return True

def parse_smf_run(smf_run_document, debug_mode = False):
    """
    Abstract: Function to parse the smf_run document, which contains all usefull informations about tests.
    Return a dictionary of tests (which contains ids of their methods and variables),\
    a dictionary of test name (to find the id) and a dictionary of case name (to find the id).
    Notice: Each case is a method in the class test!
    """

    tree = ET.parse(smf_run_document)
    root = tree.getroot()

    tests_table = {}

    test_name_to_id = {}

    case_name_to_id = {}

    for test in root.findall("tests"):

        #get classes
        for classes in test.findall("classes"):
            i = 0
            for class_item in classes.findall("class"):

                #build the id
                test_id = "t{0}".format(i)
                test_name = class_item.text

                if debug_mode:
                    print("{0} -> {1}... ".format(test_id, test_name), end="")

                #put the test in the list of available tests
                tests_table[test_id] = { 'name' : test_name, 'items' : [] }

                #save name -> id
                test_name_to_id[test_name] = test_id

                if debug_mode:
                    print("saved!")

                i = i + 1

        if debug_mode:
            print("#"*80)

        #get cases
        for cases in test.findall("cases"):

            i = 0

            for case_item in cases.findall("case"):

                #search for the test_id to make the case_id & build the id
                case_id = "c{0}".format(i)
                case_name = case_item.text
                test_id = test_name_to_id[case_name.rsplit('.', 1)[0]]
                case_id  = test_id + case_id

                if debug_mode:
                    print("{0} in {1}... ".format(case_id, test_id), end="")

                #put the node case in the list of items of the test_id
                tests_table[test_id]['items'].append(case_id)

                #save name -> id
                case_name_to_id[case_name] = {'name' : case_id, 'original_test' : test_id}

                if debug_mode:
                    print("saved!")

                i = i + 1

    return tests_table, test_name_to_id, case_name_to_id

def parse_mutations(mutations_document, debug_mode = False):
    """
    Abstract: Function to decompose mutations in the xml document (given as parameter), usefull to merge with use graph
    Return a list of couples (mutant, impacted_nodes)
    """

    tree = ET.parse(xml_document)
    root = tree.getroot()

    mutants_table = []

    good_mutants = 0

    bad_mutants = 0

    #simple search for all mutations
    for mutation in root.findall("mutations"):
        #get simple mutation
        for simple_mutation in mutation.findall("mutation"):
            print(simple_mutation.get('operator-id'))
            #search mutants
            for mutant in simple_mutation.findall("mutant"):
                #interesting if viable...
                if mutant.get('viable') == "true":
                    impacted_nodes = []
                    good_mutants = good_mutants + 1
                    if debug_mode:
                        print("good mutant: {0}".format(mutant.get('id')))
                    #search after "failing tests"
                    for child in mutant:
                        if child.tag == "failing":
                            #It's ok -> print out failing tests...
                            for child_failing in child:
                                impacted_nodes.append(child_failing.text)
                    #append to the mutants table the real id of the mutant, and the impacted nodes
                    mutants_table.append((mutant.get('in'), impacted_nodes))
                else:
                    bad_mutants = bad_mutants + 1

    if debug_mode:
        print("{0} good mutants / {1} bad mutants".format(good_mutants, bad_mutants))

    #print(mutants_table)

    return mutants_table
