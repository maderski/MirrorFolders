__author__ = 'Jason Maderski'
__date__ = '10-07-16'
from Tkinter import *
import tkFileDialog
import os.path
import subprocess
import re
import thread


# Folder related tasks are here
class Folders:

    sourcefolder = "Nothing"
    destinationfolder = "Nothing"

    # Brings up GUI to select the source folder and stores choice in the variable sourcefolder
    def pickSourceFolder(self, root):
        self.sourcefolder = tkFileDialog.askdirectory(parent=root, title='Choose SOURCE folder')
        # print self.sourcefolder

    # Brings up GUI to select the destination folder and stores choice in the variable destinationfolder
    def pickDestinationFolder(self, root):
        self.destinationfolder = tkFileDialog.askdirectory(parent=root, title='Choose DESTINATION folder')
        # print self.destinationfolder

# Batchfile related tasks are here
class BatchFile:

    previousfolders = "None"

    # Gets the current location of the program, currently not used
    def getCurrentlocation(self):
        return os.getcwd()

    # Checks to see if a batchfile exists, if batchfile with inputted name exists then it returns 'true'
    def batchFileDoesExist(self, batchfilename):
        return os.path.isfile(batchfilename)

    # Creates a batch file that uses the built in windows tool robocopy
    def writeBatchFile(self, batchfilename, source, destination):
        outputfile = open(batchfilename, "w")
        outputfile.write('@echo off' + '\n'
                         + 'robocopy "' + source + '" "' + destination + '" ' + '/MIR')
        outputfile.close()

    # Reads existing batchfile if it exists and stores the source and destination directories in the variable previous
    # folders.  If file does exist, it creates a batchfile with placeholders for both source and destination directories
    def readBatchFile(self, batchfilename):
        if self.batchFileDoesExist(batchfilename):
            try:
                inputfile = open(batchfilename)
                print "File Found: " + batchfilename
                i=1
                for line in inputfile:
                    if line.startswith("robocopy"):
			self.previousfolders = [line.split('"')[1], line.split('"')[3]]
                        # print self.previousfolders
                i+=1
                inputfile.close()
            except Exception, e:
                print e
        else:
            print "Creating File: " + batchfilename
            self.writeBatchFile(batchfilename, "None", "None")
            self.readBatchFile(batchfilename)

    # Runs the batchfile
    def runBatchFile(self, filename):
        runBatch = subprocess.Popen(filename)
        stdout, stderr = runBatch.communicate()

# All GUI relate stuff is here
class GUI:

    # Create the GUI window with buttons, text, etc...
    def createWindow(self):

        root = Tk()
        f = Folders()
        bf = BatchFile()

        # Name of the batchfile
        nameofbatchfile = "runRobocopy.bat"

        # Get prewiously used Directories
        bf.readBatchFile(nameofbatchfile)

        f.sourcefolder = bf.previousfolders[0]
        f.destinationfolder = bf.previousfolders[1]
        sourcelabeltext = StringVar()
        destinationlabeltext = StringVar()

        # Window title
        root.title("Easy Mirror of two folders")

        # Source Directory text display
        sourcelabeltext.set(f.sourcefolder)
        sourceLabel = Label(root,
                            fg="saddle brown",
                            font="Arial 16",
                            textvariable=sourcelabeltext)
        sourceLabel.pack(padx=0, pady=(10, 10))

        # Button to launch window to choose source
        sourceButton = Button(root,
                              bg="khaki",
                              text='Select Source',
                              height=2,
                              width=22,
                              font="Arial 16",
                              command=lambda: self.sourceButtonClicked(root, f, bf, nameofbatchfile, sourcelabeltext))
        sourceButton.pack(padx=20, pady=0)

        # Destination Directory text display
        destinationlabeltext.set(f.destinationfolder)
        destinationLabel = Label(root,
                                 fg="dark green",
                                 font="Arial 16",
                                 textvariable=destinationlabeltext)
        destinationLabel.pack(padx=0, pady=(50, 10))

        # Button to launch window to choose destination
        destinationButton = Button(root,
                                   fg="white",
                                   bg="olive drab",
                                   text='Select Destination',
                                   height=2,
                                   width=22,
                                   font="Arial 16",
                                   command=lambda: self.destinationButtonClicked(root, f, bf, nameofbatchfile, destinationlabeltext))
        destinationButton.pack(padx=20, pady=0)

        # Button to run Batchfile
        runButton = Button(root,
                           fg="white",
                           bg="dark red",
                           text='RUN',
                           height=2,
                           width=10,
                           font="Arial 16",
                           command=lambda: self.runButtonClicked(bf, nameofbatchfile, root))
        runButton.pack(padx=0, pady=(30, 30))
        root.mainloop()

    # Actions for when sourcebutton is clicked
    def sourceButtonClicked(self, root, folders, batchfile, bfname, text):
        folders.pickSourceFolder(root)
        batchfile.writeBatchFile(bfname, folders.sourcefolder, folders.destinationfolder)
        text.set(folders.sourcefolder)

    # Action for when destinationbutton is clicked
    def destinationButtonClicked(self, root, folders, batchfile, bfname, text):
        folders.pickDestinationFolder(root)
        batchfile.writeBatchFile(bfname, folders.sourcefolder, folders.destinationfolder)
        text.set(folders.destinationfolder)

    # Action for when runbutton is clicked
    def runButtonClicked(self, batchfile, bfname, root):
        batchfile.runBatchFile(bfname)
        root.quit()



# Run the program
class main:

    def __init__(self):
        pass

    # Program is run here
    def start(self):
        g = GUI()
        g.createWindow()

m = main()
m.start()

