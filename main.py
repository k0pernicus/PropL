import sys
import os

from threading import Thread

#from libs.xml_lib import load_xml_document
from libs.xml_lib import is_valid_XML_documents
from libs.xml_lib import is_a_valid_XML_document
from libs.xml_lib import decompose_mutations

from libs.exceptions.NoArgument import NoArgument
from libs.exceptions.RunError import RunError

from libs.use_graph_lib import UseGraph

not_authorized_files = ['.DS_Store', '__init__.py']

def help():
    """
    Abstract: Print usage and functionalities of the program
    """

    return "\
    PropL program\n\
    ---------\n\
    ---------\n\
    \n\
    Usage\n\
    -----\n\
    \tprogram <path_of_file/directory> [--help|--debug]\n\
    \n\
    List of functionalities\n\
    -----------------------\n\
    \t--help: to print help - stop the program after printing\n\
    \t--debug: to enable the debugging mode (for developers)\n\
    "

def main():

    if "--help" in sys.argv:
        print(help())
        sys.exit()

    if "--debug" in sys.argv:
        debug_mode = True
    else:
        debug_mode = False

    try:
        xml_doc = sys.argv[1]
    except Exception as excpt:
        raise NoArgument("Please to give at least the XML document (or repository) as argument...")

    #Verification of the path
    if os.path.exists(xml_doc):
        if os.path.isfile(xml_doc):
            #Transformation of the unique file -> list
            xml_doc = [xml_doc]
            if debug_mode:
                print("{0} as file".format(xml_doc))
        else:
            path = xml_doc
            xml_doc = os.listdir(path)

            #Absolute path for files
            for i in range(0, len(xml_doc)):
                xml_doc[i] = os.path.join(path, xml_doc[i])

            if debug_mode:
                print("{0} as directory".format(xml_doc))
                print("xml_doc : {0}".format(xml_doc))
    else:
        raise FailToLoad("Please to give an existing path for files...")

    #Verification of the XML validation
    print(is_valid_XML_documents(xml_doc))

    decompose_mutations(xml_doc[0], debug_mode)

    # i = 0
    #
    # #for each xml document...
    # for doc in xml_doc:
    #     #last_part is the last part of the path
    #     last_part = os.path.basename(os.path.normpath(doc))
    #     #verification : is last_part is contained in not_authorized_files field ?
    #     if not last_part in not_authorized_files:
    #         #each authorized file will be analyse in a new thread
    #         Thread(target=analyse_new_use_graph, args=(i, doc)).start()
    #         i = i + 1

if __name__ == '__main__':
    main()
