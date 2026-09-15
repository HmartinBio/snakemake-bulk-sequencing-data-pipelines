#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""MACS2.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to call peaks from BAM files with "macs2"

All the parameters are given by the Snakefile 
when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ATACAnalysisMamba" is required to
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


'''Creating the function to apply the peaks calling'''

def macs2(bamfile, outputdirectory, peakscallingtype):
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
    
    Returns
    -------
    None
    """

    organism = snakemake.params.organism

    shell(f"macs2 callpeak -t {bamfile} -g {organism} -f BAMPE --nomodel --outdir {outputdirectory}")


bamFiles = snakemake.input.datasetFiles




# Iterating all the files in the folders to make the peaks calling

for bamFile, outputDirs in zip(bamFiles, snakemake.params.outDirs):
    pool.submit(macs2, bamFile, outputDirs, snakemake.params.peaksCallingType)

pool.shutdown(wait=True)
