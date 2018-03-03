import sys
import glob
import xml.etree.ElementTree as ElementTree

def GetDirectoryList(TreeRoot):
    Directories = []
    for Element in TreeRoot[0]:
        Directories.append(Element.text)
    return Directories

def GetFileList(TreeRoot):
    Files = []
    for Element in TreeRoot[1]:
        Files.append(Element.text)
    return Files

def GetBoilerplate(TreeRoot):
    return TreeRoot[2].text

def GetOldBoilerplates(TreeRoot):
    Plates = []
    for Element in TreeRoot[3]:
        Plates.append(Element.text)
    return Plates

def FindMatches(SearchDirectory, FileExpression):
    return glob.glob(SearchDirectory + "/**/" + FileExpression, recursive=True)

def AddPlate(FileName):
    print("Found File: ", FileName)
    try:
        File = open(FileName, "r+")
        File.close()
    except Exception as Error:
        print("File Error: " + repr(Error))

ConfigTree = ElementTree.parse("Config.xml")
ConfigRoot = ConfigTree.getroot()

for Directory in GetDirectoryList(ConfigRoot):
    for FileExpression in GetFileList(ConfigRoot):
        for FileName in FindMatches(Directory, FileExpression):
            AddPlate(FileName)