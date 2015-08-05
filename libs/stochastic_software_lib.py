#Python3.4 - Antonin Carette

import os
import json

name_dir = "env_stored"
def createPathDir():


    """
        Method to create the path dir to store the environnment file
    """
    if not name_dir in os.listdir():
        os.system("mkdir ./{0}".format(name_dir))
        print("Path dir {0} created!".format(name_dir))

def getEnv(usegraph_object):
    """
        Method to get the environnment of your program
        usegraph_object : The usegraph to get some informations (the environnment)
    """
    usegraph_type = usegraph_object.usegraph_choosen
    usegraph_name = usegraph_object.id
    usegraph_path = usegraph_object.path_file
    usegraph_edges = usegraph_object.usefull_edges
    usegraph_weights_matrix = usegraph_object.all_weights

    return json.dump([usegraph_type, usegraph_name, usegraph_path, usegraph_edges, usegraph_weights_matrix])

def storeIntoFile(usegraph_object):
    """
        Method to save the environnment of your program into a file
    """
    createPathDir()

    #The name of the file is the current time
    current_time = time.asctime( time.localtime(time.time()) ).replace(" ", "_")

    #Open the file & store data in
    f = open("{0}/{1}".format(current_time, usegraph_object.id), 'w')
    f.write(getEnv(usegraph_object))
    f.close()

def loadFromFile():
    """
        Method to pull the environnment from a file to a new instance of this program
    """
    pass

def verificationOfFile():
    """
        Method to verify the good structure of the stochastic file
    """
    pass

def isFileCanBeLoad():
    """
        Method to return a boolean : is the file can be load to retrieve data?
    """
    pass
