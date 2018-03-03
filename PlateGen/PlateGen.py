import sys
import argparse
import os
import glob

Parser = argparse.ArgumentParser()
Parser.add_argument("Directory")
Parser.add_argument("Files")
Arguments = Parser.parse_args()

def FindFiles(SearchDirectory, FileTargets):
    return glob.glob(SearchDirectory + "/**/" + FileTargets, recursive=True)

def AddPlate(FileName):
    try:
        File = open(FileName, "r+")
        File.close()
    except Exception as Error:
        print("File Error: " + repr(Error))

    

for FileName in FindFiles(Arguments.Directory, Arguments.Files):
    AddPlate(FileName)