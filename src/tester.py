from tkinter import filedialog
from tkinter import *



if __name__ == "__main__":
    filePath =  filedialog.asksaveasfilename(initialdir = "../firingSolutionTables",title="Select file",filetypes = (("txt files", "*.txt"),("all files", "*.*")))
    print (filePath)
