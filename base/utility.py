from os import listdir
from os.path import isfile, join

def GetFileContents( file ):

    text = None
    files = listdir("import")

    for x in files:

        if isfile(join("import", x)) and x == file:
            with open(join("import", x), "r") as f:
                text = f.read()

            break

    return text