import sys
import glob
import xml.etree.ElementTree as ElementTree
import os

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

def MakeFileHandle(FileName):
    print("Made File Handle")
    return open(FileName, "r+")

def RemovePlate(FileHandle, FileName, BlockLastLine):
    print("Removing Plate")
    FileHandle.seek(BlockLastLine, 0)
    with open(FileName + ".tmp", "w") as TmpFile:
        for Line in FileHandle:
            TmpFile.write(Line)
    FileHandle.close()
    # Swap Temp with Original
    os.remove(FileName)
    os.rename(FileName + ".tmp", FileName)

def ContainsPlate(FileHandle, PlateBlock):
    FileHandle.seek(0, 0)
    if PlateBlock in FileHandle.read(PlateBlock.count("\n")):
        return True
    return False

def AddPlate(FileHandle, PlateBlock):
    FileHandle.seek(0, 0)
    Content = FileHandle.read()
    FileHandle.seek(0, 0)
    FileHandle.write(PlateBlock.rstrip("\r\n") + "\n" + Content)

ConfigTree = ElementTree.parse("Config.xml")
ConfigRoot = ConfigTree.getroot()

for Directory in GetDirectoryList(ConfigRoot):
    for FileExpression in GetFileList(ConfigRoot):
        for FileName in FindMatches(Directory, FileExpression):
            File = MakeFileHandle(FileName)
            for OldPlate in GetOldBoilerplates(ConfigRoot):
                if ContainsPlate(File, OldPlate):
                    RemovePlate(File, FileName, OldPlate.count("\n"))
                    File = MakeFileHandle(FileName)
            if ContainsPlate(File, GetBoilerplate(ConfigRoot)):
                RemovePlate(File, FileName, GetBoilerplate(ConfigRoot).count("\n"))
                File = MakeFileHandle(FileName)
            AddPlate(File, GetBoilerplate(ConfigRoot))
            File.close()