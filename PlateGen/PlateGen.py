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

def FindFiles(SearchDirectory, FileTargets):
    return glob.glob(SearchDirectory + "/**/" + FileTargets, recursive=True)

def AddPlate(FileName):
    try:
        File = open(FileName, "r+")
        File.close()
    except Exception as Error:
        print("File Error: " + repr(Error))

ConfigTree = ElementTree.parse("Config.xml")

ConfigRoot = ConfigTree.getroot()

for Iter in GetDirectoryList(ConfigRoot):
    print("Directory Found: ", Iter)
for Iter in GetFileList(ConfigRoot):
    print("File Found: ", Iter)
print("Boilerplate Block Found:\n", GetBoilerplate(ConfigRoot))
for Iter in GetOldBoilerplates(ConfigRoot):
    print("Old Boilerplate Blocks Found:\n", Iter)

#for FileName in FindFiles(Arguments.Directory, Arguments.Files):
#    AddPlate(FileName)