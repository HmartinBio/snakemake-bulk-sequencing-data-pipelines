#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""FileManagement.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to manage the file and foldernames
to distribute them to each rules. 

This file contains the following class:
    * FileManagement - A class to manage the filenames extentions and foldernames 
    during the pipeline processing
"""



# Importing librairies

import os
import pathlib
import re

# Designing the class template

class FileManagement():
    """
    A class to manage the filenames extentions and foldernames 
    during the pipeline processing
    ...

    Attributes
    ----------
    dataset : str
        Folder name of the protein containing the folders names saved in the list "datasetype"
    datasetype : list
        List containing the folder names of the conditions containing directly the FASTQ filenames
    listofsamples : list
        List containing the filenames of the FASTQ files to analyse
    listofsamplesandfolderswithoutpeassign : list
        List containing the filenames without the extension R1.fastq.gz or R2.fastq.gz
    listoffolders : list
        List containing the entire folder names where the FASTQ files are saved 
    outputfolderspelength : list
        List containing folder names to save output folder for each paired-end
        FASTQ where to save output results
    trimmingfiles : list
        List containing the output filenames after Trimming step 
    outputfolders : list
        List containing the output folder for each FASTQ where to save output results
    inputpathway : str
        Entire pathname to the protein name containing the folders names 
        saved in the list "datasetype"
    outputpathway : str
        Entire pathname to the output folder containing preprocessed results
    pairedend : bool
        Flag to indicate if data are paired-end or not

    Methods
    -------
    samplenameswithoutpairedendas(): 
        Take the entire filenames from "listofsamples" and returns the filenames without the extension 
        associated to paired-end format (R1.fastq.gz, R2.fastq.gz)
    computingdatasettypefileinformation(): 
        Take the list of condition names "datasetype" 
        to create the input and output folders for each sample 
        based on the foldernames given to the workflow
    computingpairedendlengthoutputfoldernames(): 
        Take the list of output folders and compute one folder
        for both paired-end files. Only for paired-end data
    computingtrimmingfastqnames(trimmingextension=False, pairedend=True):
        Take the list of FASTQ filenames without the paired-end extension "listofsamplesandfolderswithoutpeassign"
        to add them the TrimmGalore extension
    listingfiles():
        Running several functions (computingdatasettypefileinformation, samplenameswithoutpairedendas, 
        computingpairedendlengthoutputfoldernames, computingtrimmingfastqnames) 
        from the Class to create suitable filenames and foldernames to use by the pipeline
    sortingbyconditions(ctrlcondition, files):
        Take the files given in parameter "files" and sort them in two conditions
        according the regex matching pattern "ctrlcondition"
    balancenumberfilespeakscalling(files, inputfiles):
        Take the file and input base filenames to associate them together
        If there is not the same number of input and IP files for a specific sample 
        Then samples or input are iterated for this specific sample to fullfill the 
        correct number and avoid raising an error message
    controllingfilepairementforpeakscalling(ctrlconditionsfiles, treatconditionsfiles, 
        inputfilesctrl, inputfilestreat):
        Run the function "balancenumberfilespeakscalling" for each condition
        and return a tuple of list containing samples and input base filenames
        in alternate positions
    creatingpeakscallingfolders(ctrlcondition, files, peakscallingtype, inputfiles=False):
        Take the base filenames sorted by condition to generate 
        peaks calling folders for each sample by condition 
        According if peaks calling is run with or without input
        peaks calling foldernames are written with or without input 
        names
    returningoutputfolders():
        Return the list of output folder per sample
    returningpairedendlengthoutputfolders():
        Return the list of output folder per paired-end sample
    returningtrimmingsamples():
        Return the list of trimmed sample filenames
    returninglistofsamples(extension=''):
        Return the list of samples names
    returnlistofsampleswthoutpe():
        Return the list of samples names without the paired-end extension
    returninputfolders():
        Return the entire pathnames to the input folders
    """

    def __init__(self, dataset, datasetype, inputpath, outputpath, pairedend):
        """
        Parameters
        ----------
        dataset : str
            Folder name of the protein containing the folders names saved in the list "datasetype"
        datasetype : str
            List containing the folder names of the conditions containing directly the FASTQ filenames
        inputpath : str
            Root pathname given to the Snakemake workflow to take the input samples 
        outputpath : str
            Root pathname given to the Snakemake workflow to save the output results
        pairedend : bool
            Flag from the workflow to indicate if data to preprocess are paired or single-end
        """

        self.dataset = dataset
        self.datasetype = datasetype
        self.listofsamples = []
        self.listofsamplesandfolderswithoutpeassign = []
        self.listoffolders = []
        self.outputfolderspelength = []
        self.trimmingfiles = []
        self.outputfolders = []
        self.inputpathway = inputpath + self.dataset + "/"
        self.outputpathway = outputpath + self.dataset + "/"
        self.pairedend = pairedend

        self.listingfiles()



    def samplenameswithoutpairedendas(self,):
        """
        Take the entire filenames from "listofsamples" and returns the filenames without the extension 
        associated to paired-end format (R1.fastq.gz, R2.fastq.gz)

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """

        # Deleting the content existing in listofsamplesandfolderswithoutpeassign

        self.listofsamplesandfolderswithoutpeassign = []

        # Creating an iteration counter

        iterationcounter = 0

        # Iterating the filenames to keep only
        # the ID and not the paired end information

        for filenames in self.listofsamples:

            if iterationcounter % 2 == 0:
                filenamesplitted = filenames.split('_')
                filenamesplitted = filenamesplitted[0:len(filenamesplitted) - 2]

                newfilename = '_'.join(filenamesplitted)
                self.listofsamplesandfolderswithoutpeassign.append(newfilename)

                iterationcounter += 1

            else:
                iterationcounter += 1





    def computingdatasettypefileinformation(self,):
        """
        Take the list of condition names "datasetype" 
        to create the input and output folders for each sample 
        based on the foldernames given to the workflow

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """

        for typeofdataset in self.datasetype:

            # Saving the actual pathway

            srcpathway = os.getcwd()

            # Changing the pathway

            pathway = pathlib.Path(self.inputpathway + "/" + typeofdataset).resolve()
            os.chdir(pathway)

            # Listing files, datasetType and folders

            listofsampleswithext = os.listdir()

            # Sorting the files for paired end filenames

            listofsampleswithext = sorted(listofsampleswithext)

            self.listoffolders += [str(pathway)] * len(listofsampleswithext)

            # Computing a new list of files without extensions from the previous one

            self.listofsamples += [oldFile.split('.fastq.gz')[0]
                for oldFile in listofsampleswithext]

            # Returning in the previous pathway

            os.chdir(srcpathway)

            # Computing output folders

            pathway = pathlib.Path(self.outputpathway + typeofdataset).resolve()
            self.outputfolders += [str(pathway)] * len(listofsampleswithext)





    def computingpairedendlengthoutputfoldernames(self):
        """
        Take the list of output folders and compute one folder
        for both paired-end files. Only for paired-end data 

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """

        # Defining an iterative counter

        iterativecounter = 0

        for folder in self.outputfolders:

            if iterativecounter % 2 == 0:
                self.outputfolderspelength.append(folder)
                iterativecounter += 1

            else:
                iterativecounter += 1





    def computingtrimmingfastqnames(self, trimmingextension=False, pairedend=True):
        """
        Take the list of FASTQ filenames without the paired-end extension "listofsamplesandfolderswithoutpeassign"
        to add them the TrimmGalore extension

        Parameters
        ----------
        trimmingextension : bool
            Flag to indicate if output trimming filenames should be returned 
            with the TrimmGalore extension
        pairedend : bool
            Flag to indicate if data are paired-end
        
        Returns
        -------
        None
        """

        # Defining an iterative counter

        iterativecounter = 0

        for folder in self.outputfolders:

            # If files are paired end files, we add the good extenstion to each paired files
            # which is attributed by TrimmGalore. If files are single end files, so we give the
            # .fq.gz extension

            if pairedend:

                if iterativecounter % 2 == 0:

                    foldernamewithoutpe = self.listofsamplesandfolderswithoutpeassign[
                        int(iterativecounter - (iterativecounter / 2))]

                    extensionfile = '_val_1.fq.gz'

                else:
                    extensionfile = '_val_2.fq.gz'


                if trimmingextension:

                    self.trimmingfiles.append(folder + "/" + "Trimming" +
                    "/" + foldernamewithoutpe + 
                    "/" + self.listofsamples[iterativecounter] + extensionfile)

                else:
                    self.trimmingfiles.append(folder + "/" + "Trimming" +
                    "/" + foldernamewithoutpe + 
                    "/" + self.listofsamples[iterativecounter])




            else:
                foldername = self.listofsamples[iterativecounter]
                extensionfile = '.fq.gz'

                if trimmingextension:

                    self.trimmingfiles.append(folder + "/" + "Trimming" +
                    "/" + foldername + 
                    "/" + foldername + extensionfile)

                else:
                    self.trimmingfiles.append(folder + "/" + "Trimming" +
                    "/" + foldername + 
                    "/" + foldername)


            iterativecounter += 1






    def listingfiles(self,):
        """
        Running several functions (computingdatasettypefileinformation, samplenameswithoutpairedendas, 
        computingpairedendlengthoutputfoldernames, computingtrimmingfastqnames) 
        from the Class to create suitable filenames and foldernames to use by the pipeline
 
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """

        # Computing files informations for all the dataset types

        self.computingdatasettypefileinformation()

        # Computing paired-end file names

        self.samplenameswithoutpairedendas()

        # Computing a list of trimmed folders

        self.computingpairedendlengthoutputfoldernames()

         # Computing a list of trimmed samples

        self.computingtrimmingfastqnames(trimmingextension=True, pairedend=self.pairedend)




    def sortingbyconditions(self, ctrlcondition, files):
        """
        Take the files given in parameter "files" and sort them in two conditions
        according the regex matching pattern "ctrlcondition"
 
        Parameters
        ----------
        ctrlcondition : str
            Regex pattern matching samples characterized as Control
        files : list
            List of FASTQ filenames
        
        Returns
        -------
        tuple
            tuple containing in the first index samples classified as Control
            and the Treated in a second position
        """


        # Creating two lists

        ctrlconditionsfiles = []
        treatconditionsfiles = []


        # Sorting files according the pattern

        for file in files:

            if len(re.findall(ctrlcondition, file)) != 0:
                ctrlconditionsfiles.append(file)

            else:
                treatconditionsfiles.append(file)

        # Returning both lists

        if not treatconditionsfiles:
            treatconditionsfiles = "empty"


        return((ctrlconditionsfiles, treatconditionsfiles))




    def balancenumberfilespeakscalling(self, files, inputfiles):
        """
        Take the file and input base filenames to associate them together
        If there is not the same number of input and IP files for a specific sample 
        Then samples or input are iterated for this specific sample to fullfill the 
        correct number and avoid raising an error message
 
        Parameters
        ----------
        files : str
            List of base filenames for samples ChIP
        inputfiles : list
            List of base filenames for inputs
        
        Returns
        -------
        list
            List containing the names for the samples and the inputs
            Position of samples are paired indexed and impair indexed for the 
            inputs in the list
        """

        # Building dictionnaries of sample numbers associated to files
        # for Input and other samples

        dictionnaryindexfilesinput = {}
        dictionnaryindexfiles = {}

        # Filling the dictionnaries by looking for
        # the sample number in filenames

        for inputfilenames in inputfiles:
            fileindex = re.findall('[0-9]+', inputfilenames)[0]

            if fileindex not in dictionnaryindexfilesinput:
                dictionnaryindexfilesinput[fileindex] = []

            dictionnaryindexfilesinput[fileindex].append(inputfilenames)


        for samplefilenames in files:
            fileindex = re.findall('[0-9]+', samplefilenames)[0]

            if fileindex not in dictionnaryindexfiles:
                dictionnaryindexfiles[fileindex] = []

            dictionnaryindexfiles[fileindex].append(samplefilenames)


        # Creating a list to associate Input files with sample files

        listassociatedfilessamples = []

        # Iterating both dictionnaries and taking the associated files
        # If there is not the same number of samples and input for a same sample number
        # Then the samples or the inputs are taken until the size of lists are equal
        # Firstly, samples filenames are appended to the list then it is
        # the Input filenames which are appended in second place each time

        for indexfile, filenameslistsample in dictionnaryindexfiles.items():
            if len(filenameslistsample) != len(dictionnaryindexfilesinput[indexfile]):

                numberoffiledifference = len(filenameslistsample) -\
                    len(dictionnaryindexfilesinput[indexfile])

                if numberoffiledifference < 0:
                    for numberfileinput in range(0, len(dictionnaryindexfilesinput[indexfile]) -
                        abs(numberoffiledifference)):

                        listassociatedfilessamples.append(filenameslistsample[numberfileinput])

                        listassociatedfilessamples.append(
                            dictionnaryindexfilesinput[indexfile][numberfileinput])

                else:
                    for numberfilesamples in range(
                        0, len(filenameslistsample) - abs(numberoffiledifference)):

                        listassociatedfilessamples.append(filenameslistsample[numberfilesamples])

                        listassociatedfilessamples.append(
                            dictionnaryindexfilesinput[indexfile][numberfilesamples])

            else:
                for numberfilesamples, filenamesample in enumerate(filenameslistsample):
                    listassociatedfilessamples.append(filenamesample)

                    listassociatedfilessamples.append(
                        dictionnaryindexfilesinput[indexfile][numberfilesamples])


        return listassociatedfilessamples



    def controllingfilepairementforpeakscalling(self, ctrlconditionsfiles, treatconditionsfiles,
        inputfilesctrl, inputfilestreat):
        """
        Run the function "balancenumberfilespeakscalling" for each condition
        and return a tuple of list containing samples and input base filenames
        in alternate positions
 
        Parameters
        ----------
        ctrlconditionsfiles : list
            List of base filenames for Control samples ChIP
        treatconditionsfiles : list
            List of base filenames for Treated samples ChIP
        inputfilesctrl : list
            List of base filenames for Control Input
        inputfilestreat : list
            List of base filenames for Treated Input

        Returns
        -------
        tuple
            Tuple containing basename filenames for samples and input 
            for each condition. Control condition is associated to the first index
            and Treated condition is associated to the last one from the tuple 
        """

        # Associating the Input files and samples files by samples numbers

        ctrlsamplesassociatedinput = self.balancenumberfilespeakscalling(files=ctrlconditionsfiles,
            inputfiles=inputfilesctrl)

        treatsamplesassociatedinput = self.balancenumberfilespeakscalling(
            files=treatconditionsfiles,
            inputfiles=inputfilestreat)

        # Returning the associated filenames

        return((ctrlsamplesassociatedinput, treatsamplesassociatedinput))




    def creatingpeakscallingfolders(self, ctrlcondition, files,
        peakscallingtype, inputfiles = False):
        """
        Take the base filenames sorted by condition to generate 
        peaks calling folders for each sample by condition 
        According if peaks calling is run with or without input
        peaks calling foldernames are written with or without input 
        names

 
        Parameters
        ----------
        ctrlcondition : str
            Regex pattern matching samples characterized as Control
        files : list
            List of base filenames
        peakscallingtype : str
            Type of peaks calling to perform
        inputfiles : bool,list, optional
            List of base input filenames (default is False)

        Returns
        -------
        tuple
            Tuple containing the list of peaks folders names and the tuple containing 
            basename filenames for samples and input for each condition. If no imput are 
            precised then only the filenames are returned
        """

        if peakscallingtype != 'None': #( == "Input")

            # Sorting files by conditions

            ctrlconditionsfiles = self.sortingbyconditions(ctrlcondition=ctrlcondition,
                files=files)[0]

            treatconditionsfiles = self.sortingbyconditions(ctrlcondition=ctrlcondition,
                files=files)[1]


            # Creating a new list of files

            mergedlistoffiles = []


            # If we apply a peaks calling without input

            if not inputfiles:

                for ctrlfiles, treatedfiles in zip(ctrlconditionsfiles, treatconditionsfiles):

                    concatenatedfilename = ctrlfiles + '_' + treatedfiles

                    mergedlistoffiles.append(concatenatedfilename)

                # Returning the filenames

                return((mergedlistoffiles, 0))


            # Sorting Input files by conditions

            inputfilesctrl = self.sortingbyconditions(ctrlcondition=ctrlcondition,
                files=inputfiles)[0]

            inputfilestreat = self.sortingbyconditions(ctrlcondition=ctrlcondition,
                files=inputfiles)[1]

            tupleofassociatedsamples = self.controllingfilepairementforpeakscalling(
                ctrlconditionsfiles=ctrlconditionsfiles,
                treatconditionsfiles=treatconditionsfiles,
                inputfilesctrl=inputfilesctrl,
                inputfilestreat=inputfilestreat)

            for associatedfiles in tupleofassociatedsamples:

                for indexfiles, file in enumerate(associatedfiles):

                    if indexfiles % 2 == 1:

                        concatenatedfilename = f"{associatedfiles[indexfiles - 1]}_{file}"
                        mergedlistoffiles.append(concatenatedfilename)


            # Returning the filenames

            return((mergedlistoffiles, tupleofassociatedsamples))


        return((files, 0))





    def returningoutputfolders(self):
        """
        Return the list of output folder per sample

        Parameters
        ----------
        None

        Returns
        -------
        list
            List containing the pathnames to the output folders
        """

        return self.outputfolders




    def returningpairedendlengthoutputfolders(self):
        """
        Return the list of output folder per paired-end sample

        Parameters
        ----------
        None

        Returns
        -------
        list
            List containing the pathnames to one output folders per paired-end sample
        """

        return self.outputfolderspelength



    def returningtrimmingsamples(self):
        """
        Return the list of trimmed sample filenames

        Parameters
        ----------
        None

        Returns
        -------
        list
            List containing the entire filenames of the output files from TrimmGalore
        """

        return self.trimmingfiles




    def returninglistofsamples(self, extension=''):
        """
        Return the list of samples names

        Parameters
        ----------
        extension : str, optional
            Extension to add at the end of the sample name (Default: '')

        Returns
        -------
        list
            List containing the sample names
        """

        return([sample + extension for sample in self.listofsamples])




    def returnlistofsampleswthoutpe(self):
        """
        Return the list of samples names without the paired-end extension

        Parameters
        ----------
        None

        Returns
        -------
        list
            List containing the sample names without the paired-end extension
        """

        return self.listofsamplesandfolderswithoutpeassign



    def returninputfolders(self):
        """
        Return the entire pathnames to the input folders

        Parameters
        ----------
        None

        Returns
        -------
        list
            List containing the entire pathnames to the input folders
        """

        return self.listoffolders
