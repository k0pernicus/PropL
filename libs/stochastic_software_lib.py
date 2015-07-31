import os

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
    pass

def storeIntoFile():
    """
        Method to save the environnment of your program into a file
    """
    pass

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
