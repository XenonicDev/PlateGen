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
    return open(FileName, "r+")

def RemovePlate(FileHandle, FileName, BlockLastLine):
    FileHandle.seek(0, 0)
    # Read Until We're at the Target Line
    for Iter in range(BlockLastLine):
        FileHandle.readline()
    with open(FileName + ".tmp", "w") as TmpFile:
        for Line in FileHandle:
            TmpFile.write(Line)
    FileHandle.close()
    # Swap Temp with Original
    os.remove(FileName)
    os.rename(FileName + ".tmp", FileName)

def ContainsPlate(FileHandle, PlateBlock):
    FileHandle.seek(0, 0)
    BlockList = [next(FileHandle) for X in range(PlateBlock.count("\n") + 1)]
    Block = ''.join(BlockList)
    if (PlateBlock + "\n" == Block):
        print("Found Plate Match in File: ", FileHandle.name)
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
                    RemovePlate(File, FileName, OldPlate.count("\n") + 1)
                    File = MakeFileHandle(FileName)
            if ContainsPlate(File, GetBoilerplate(ConfigRoot)):
                continue  # Skip, This File Has the Proper Plate
            AddPlate(File, GetBoilerplate(ConfigRoot))
            File.close()