#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""MACS2.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to call peaks from BAM files with "macs2"

All the parameters are given by the Snakefile 
when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ChIPAnalysisMamba" is required to
launch this module

This file contains the following function:
    * macs2 - Take the input BAM files to call peaks for each sample
"""

# Importing librairies

from snakemake import shell
from concurrent.futures import ThreadPoolExecutor
import os
import re
import tempfile


# Creating the pool for multithreading

pool = ThreadPoolExecutor(max_workers=snakemake.threads)



def macs2(bamfile, outputdirectory, peakscallingtype, inputbamfile = False):
    """
    Take the input BAM files to call peaks for each sample

    Parameters
    ----------
    bamfile : str
        Pathname to the input BAM file
    outputdirectory : str
        Pathname to output directory to save the outputs
    peakscallingtype : str
        Type of peaks calling to use (None/Input)
    inputbamfile : bool, str
        Pathname to input BAM file (Defaut: None)
    Returns
    -------
    None
    """

    organism = snakemake.params.organism

    if peakscallingtype == 'None': # {organism} =hs
        shell(f"macs2 callpeak -t {bamfile} -g hs -f BAMPE --nomodel --outdir {outputdirectory}")
    else:
        shell(f"macs2 callpeak -t {bamfile} -g hs -f BAMPE --nomodel -c {inputbamfile} --outdir {outputdirectory}")



# Selecting BAM files and Input files according Input files to use

if snakemake.params.peaksCallingType == 'Control':

    inputBamFiles = snakemake.input.datasetFilesCtrl
    bamFiles = snakemake.input.datasetFilesTreat


if snakemake.params.peaksCallingType == "Input":

    if not snakemake.params.peaksCallingOnMergedBam:

        # If Input files are not in the same number relative to
        # the samples files

        if (len(snakemake.params.AssembledFilesPeaksCalling) != 0):
            
            # Creating new lists to save inputBamFiles and bamFiles
            # in a new order

            inputBamFiles = []
            bamFiles = []

            # Creating a dictionnary of bam files in the aim to retrieve the
            # absolute pathway of bam files

            dictionnaryOfAbsoluteBamFilesPathways = {}

            for absolutePathFiles in snakemake.input.datasetFiles:
                dictionnaryOfAbsoluteBamFilesPathways[os.path.basename(absolutePathFiles)] = absolutePathFiles

            for absolutePathIgGFiles in snakemake.input.Inputfiles:
                dictionnaryOfAbsoluteBamFilesPathways[os.path.basename(absolutePathIgGFiles)] = absolutePathIgGFiles


            # Associating Input files and sample files for the peaks calling

            for associatedValues in snakemake.params.AssembledFilesPeaksCalling:
            
                for indexFiles, file in enumerate(associatedValues):

                    fileBasename = file + '_filtered_nodup.bam'

                    if (indexFiles % 2 == 0):
                    
                        bamFiles.append(dictionnaryOfAbsoluteBamFilesPathways[fileBasename])
                    
                    else:
                        inputBamFiles.append(dictionnaryOfAbsoluteBamFilesPathways[fileBasename])


    else:
        inputBamFiles = snakemake.input.Inputfiles
        bamFiles = snakemake.input.datasetFiles


else:
    bamFiles = snakemake.input.datasetFiles



# If no input files are used

if snakemake.params.peaksCallingType == 'None':

    # Iterating all the files in the folders to make the peaks calling

    for bamFile, outputDirs in zip(bamFiles, snakemake.params.outDirs):
        pool.submit(macs2, bamFile, outputDirs, snakemake.params.peaksCallingType)

else:

    # Iterating all the files in the folders to make the peaks calling

    for bamFile, inputBamFile, outputDirs in zip(bamFiles, inputBamFiles, snakemake.params.outDirs):
        pool.submit(macs2, bamFile, outputDirs, snakemake.params.peaksCallingType, inputBamFile)

pool.shutdown(wait=True)
