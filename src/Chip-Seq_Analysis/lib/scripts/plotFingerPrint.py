#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""plotFingerPrint.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to compute Lorenz curves
from input bamFiles. All the parameters are given by the Snakefile 
when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ChIPAnalysisMamba" is required to
launch this module

This file contains the following functions:
    * computingbasenamefile - Take the pathname to the input BAM file and return its basename
    * plotfingerprint - Take the Control and Treated BAM files to compute the Lorenz curves with "plotFingerprint" function
"""

# Importing librairies

from snakemake import shell


def computingbasenamefile(filecompletepath):
    """
    Take the pathname to the input BAM file and return its basename

    Parameters
    ----------
    filecompletepath : str
        The file location to the BAM file

    Returns
    -------
    str
        Basename of the entire pathname given as input
    """

    basenamefile = filecompletepath.split('/')

    if len(basenamefile) == 1:
        basenamefile = basenamefile.split('\\')

    return basenamefile[-1]



def plotfingerprint(datasetbamfilectrl, datasetbamfiletreat, outputplotfigure,
    outputrawcounts, inputbamfilectrl=False, inputbamfiletreat=False):
    """
    Take the Control and Treated BAM files to compute the Lorenz curves with
    "plotFingerprint" function

    Parameters
    ----------
    datasetbamfilectrl : str
        Space-separated pathnames to the Control BAM files  
    datasetbamfiletreat : str
        Space-separated pathnames to the Treated BAM files
    outputplotfigure : str
        The file location to the output figure
    outputrawcounts : str
        The file location to the output text file
    inputbamfilectrl : bool,str, optional
        Space-separated pathnames to the Input Control BAM files  
    inputbamfiletreat : bool,str, optional
        Space-separated pathnames to the Input Treated BAM files 
    Returns
    -------
    None
    """

    if not inputbamfilectrl and not inputbamfiletreat:

        if not snakemake.params.singleDataset:
            concatenatedbamfile = f"{' '.join(datasetbamfilectrl)} {' '.join(datasetbamfiletreat)}"

        else:
            concatenatedbamfile = ' '.join(datasetbamfilectrl)

    else:
        concatenatedbamfile = f"{' '.join(datasetbamfilectrl)} {' '.join(datasetbamfiletreat)} {' '.join(inputbamfilectrl)} {' '.join(inputbamfiletreat)}"


    # Creating lists to save the basename of each files

    listdatasetbambasenamectrl = []

    if datasetbamfiletreat:
        listdatasetbambasenametreat = []

    if inputbamfilectrl and inputbamfiletreat:
        listinputbambasenamectrl = []
        listinputbambasenametreat = []


    # Computing the basename of each files


    for fullnamedatasetctrl in datasetbamfilectrl:
        listdatasetbambasenamectrl.append(computingbasenamefile(fullnamedatasetctrl))

    if not snakemake.params.singleDataset:
        for fullnamedatasettreat in datasetbamfiletreat:
            listdatasetbambasenametreat.append(computingbasenamefile(fullnamedatasettreat))


    if inputbamfilectrl and inputbamfiletreat:
        for fullnameinputctrl in inputbamfilectrl:
            listinputbambasenamectrl.append(computingbasenamefile(fullnameinputctrl))

        for fullnameinputtreat in inputbamfiletreat:
            listinputbambasenametreat.append(computingbasenamefile(fullnameinputtreat))



    # Creating a strings from lists

    if not inputbamfilectrl and not inputbamfiletreat:

        if not snakemake.params.singleDataset:
            concatenatedbasenamebamfiles = f"{' '.join(listdatasetbambasenamectrl)} {' '.join(listdatasetbambasenametreat)}"
        else:
            concatenatedbasenamebamfiles = ' '.join(listdatasetbambasenamectrl)


    else:
        concatenatedbasenamebamfiles = f"{' '.join(listdatasetbambasenamectrl)} {' '.join(listdatasetbambasenametreat)} \
            {' '.join(listinputbambasenamectrl)} {' '.join(listinputbambasenametreat)}"


    # Creating the plot

    shell(f"plotFingerprint --binSize=250 --ignoreDuplicates -b {concatenatedbamfile} -plot {outputplotfigure} \
        -l {concatenatedbasenamebamfiles} -p {snakemake.threads} --outRawCounts {outputrawcounts}")


# Plotting the Lorenz curve

if snakemake.params.InputFilesCtrl == "False" and snakemake.params.InputFilesTreat == "False":

    if snakemake.params.singleDataset:

        plotfingerprint(datasetbamfilectrl=snakemake.input.datasetFilesCtrl, datasetbamfiletreat=False,
                        outputplotfigure=snakemake.output.plotFingerprintPicture, outputrawcounts=snakemake.output.plotFingerprintRawCounts)


    else:
        plotfingerprint(datasetbamfilectrl=snakemake.input.datasetFilesCtrl, datasetbamfiletreat=snakemake.input.datasetFilesTreat,
                        outputplotfigure=snakemake.output.plotFingerprintPicture, outputrawcounts=snakemake.output.plotFingerprintRawCounts)


else:
    plotfingerprint(datasetbamfilectrl=snakemake.input.datasetFilesCtrl, datasetbamfiletreat=snakemake.input.datasetFilesTreat,
        inputbamfilectrl=snakemake.params.InputFilesCtrl, inputbamfiletreat=snakemake.params.InputFilesTreat,
        outputplotfigure=snakemake.output.plotFingerprintPicture, outputrawcounts=snakemake.output.plotFingerprintRawCounts)
