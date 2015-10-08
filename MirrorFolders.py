__author__ = 'Dev'
from Tkinter import *
import tkFileDialog
import os.path
import subprocess
import re


class Folders:

    sourcefolder = "Nothing"
    destinationfolder = "Nothing"

    def pickSourceFolder(self, root):
        # root.withdraw()
        self.sourcefolder = tkFileDialog.askdirectory(parent=root, title='Choose SOURCE folder')
        print self.sourcefolder

    def pickDestinationFolder(self, root):
        # root.withdraw()
        self.destinationfolder = tkFileDialog.askdirectory(parent=root, title='Choose DESTINATION folder')
        print self.destinationfolder


class BatchFile:

    previousfolders = "None"

    def getCurrentlocation(self):
        return os.getcwd()

    def batchFileDoesExist(self, batchfilename):
        return os.path.isfile(batchfilename)

    def writeBatchFile(self, batchfilename, source, destination):
        outputfile = open(batchfilename, "w")
        outputfile.write("@echo off" + "\n"
                         + "robocopy " + source + " " + destination + " " + "/MIR")
        outputfile.close()

    def readBatchFile(self, batchfilename):
        if self.batchFileDoesExist(batchfilename):
            try:
                inputfile = open(batchfilename)
                print "File Found: " + batchfilename
                i=1
                for line in inputfile:
                    if line.startswith("robocopy"):
                        line = re.sub('robocopy ', '', line)
                        line = re.sub('/MIR', '', line)
                        self.previousfolders = line.split()
                        print self.previousfolders
                i+=1
                inputfile.close()
            except Exception, e:
                print e
        else:
            print "Creating File: " + batchfilename
            self.writeBatchFile(batchfilename, "None", "None")
            self.readBatchFile(batchfilename)

    def runBatchFile(self, filename):
        runBatch = subprocess.Popen(filename)
        stdout, stderr = runBatch.communicate()


class GUI:

    def createWindow(self):

        root = Tk()
        f = Folders()
        bf = BatchFile()

        nameofbatchfile = "runRobocopy.bat"
        bf.readBatchFile(nameofbatchfile)

        f.sourcefolder = bf.previousfolders[0]
        f.destinationfolder = bf.previousfolders[1]
        sourcelabeltext = StringVar()
        destinationlabeltext = StringVar()

        root.title("Easy Mirror of two folders")

        sourcelabeltext.set(f.sourcefolder)
        sourceLabel = Label(root,
                            fg="saddle brown",
                            font="Arial 16",
                            textvariable=sourcelabeltext)
        sourceLabel.pack(padx=0, pady=(10, 10))

        sourceButton = Button(root,
                              bg="khaki",
                              text='Select Source',
                              height=2,
                              width=22,
                              font="Arial 16",
                              command=lambda: self.sourceButtonClicked(root, f, bf, nameofbatchfile, sourcelabeltext))
        sourceButton.pack(padx=20, pady=0)

        destinationlabeltext.set(f.destinationfolder)
        destinationLabel = Label(root,
                                 fg="dark green",
                                 font="Arial 16",
                                 textvariable=destinationlabeltext)
        destinationLabel.pack(padx=0, pady=(50, 10))

        destinationButton = Button(root,
                                   fg="white",
                                   bg="olive drab",
                                   text='Select Destination',
                                   height=2,
                                   width=22,
                                   font="Arial 16",
                                   command=lambda: self.destinationButtonClicked(root, f, bf, nameofbatchfile, destinationlabeltext))
        destinationButton.pack(padx=20, pady=0)

        runButton = Button(root,
                           fg="white",
                           bg="dark red",
                           text='RUN',
                           height=2,
                           width=10,
                           font="Arial 16",
                           command=lambda: self.runButtonClicked(bf, nameofbatchfile))
        runButton.pack(padx=0, pady=(30, 30))
        root.mainloop()

    def sourceButtonClicked(self, root, folders, batchfile, bfname, text):
        folders.pickSourceFolder(root)
        batchfile.writeBatchFile(bfname, folders.sourcefolder, folders.destinationfolder)
        text.set(folders.sourcefolder)

    def destinationButtonClicked(self, root, folders, batchfile, bfname, text):
        folders.pickDestinationFolder(root)
        batchfile.writeBatchFile(bfname, folders.sourcefolder, folders.destinationfolder)
        text.set(folders.destinationfolder)

    def runButtonClicked(self, batchfile, bfname):
        batchfile.runBatchFile(bfname)


class main:

    def __init__(self):
        pass

    def start(self):
        g = GUI()
        g.createWindow()

m = main()
m.start()

