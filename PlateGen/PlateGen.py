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

def RemovePlate(FileHandle, LineStart, LineEnd):
    print()  # Placeholder

def ContainsPlate(FileHandle, PlateBlock):
    return False

def AddPlate(FileHandle, PlateBlock):
    Content = FileHandle.read()
    FileHandle.seek(0, 0)
    FileHandle.write(PlateBlock.rstrip("\r\n") + "\n" + Content)

ConfigTree = ElementTree.parse("Config.xml")
ConfigRoot = ConfigTree.getroot()

for Directory in GetDirectoryList(ConfigRoot):
    for FileExpression in GetFileList(ConfigRoot):
        for FileName in FindMatches(Directory, FileExpression):
            with open(FileName, "r+") as File:
                for OldPlate in GetOldBoilerplates(ConfigRoot):
                    if ContainsPlate(File, OldPlate):
                        RemovePlate(File, 0, OldPlate.count("\n"))  # TODO: Search for First Character, Don't Start at 0
                if ContainsPlate(File, GetBoilerplate(ConfigRoot)):
                    RemovePlate(File, 0, GetBoilerplate(ConfigRoot).count("\n"))  # TODO: Search for First Character, Don't Start at 0
                AddPlate(File, GetBoilerplate(ConfigRoot))