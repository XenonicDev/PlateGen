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

for File in FindFiles(Arguments.Directory, Arguments.Files):
    print(File)