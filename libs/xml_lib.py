import os

from libs.exceptions.FailToLoad import FailToLoad
from xml.dom import minidom
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import xml.etree.ElementTree as ET

def loadXmlDocument(xml_document):
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

def isValidXMLDocuments(xml_documents):
    """
    Abstract: Procedure to know if all XML files given as parameters are valid XML documents
    """

    #creation of the parser
    xml_parsing = make_parser()

    #set the ContentHandler
    xml_parsing.setContentHandler(ContentHandler())

    if os.path.isfile(xml_documents):
        if isAValidXMLDocument(xml_parsing, xml_documents):
            print("{0} is a valid XML document".format(xml_documents))
        else:
            print("{0} is not a valid XML document".format(xml_documents))
    else:
        #verification on each document
        for doc in xml_documents:
            if os.path.isfile(doc):
                if isAValidXMLDocument(xml_parsing, doc):
                    print("{0} is a valid XML document".format(doc))
                else:
                    print("{0} is not a valid XML document".format(doc))
            else:
                print("{0} is not a file".format(doc))

def isAValidXMLDocument(xml_parsing, xml_document):
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
