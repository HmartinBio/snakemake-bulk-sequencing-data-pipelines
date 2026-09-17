#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""FripScore.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to counts the reads under the peaks
with "featureCounts" from BAM files and SAF files (converted BED files from MACS2) 

All the parameters are given by the Snakefile 
when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ATACAnalysisMamba" is required to
launch this module

This file contains the following function:
    * computefripscore - Take the input BAM file and SAF file to count the reads under peaks 
"""

# Loading librairies

from concurrent.futures import ThreadPoolExecutor
from snakemake import shell


# Creating the pool for multithreading

pool = ThreadPoolExecutor(max_workers=snakemake.threads)


def computefripscore(saffile, bamfile, outputtextfile):
    """
    Take the input BAM file and SAF file to count the reads under peaks 

    Parameters
    ----------
    saffile : str
        Pathname to the input SAF file
    bamfile : str
        Pathname to the input BAM file
    outputtextfile : str
        Pathname to the output counts file
    Returns
    -------
    None
    """

    shell(f"featureCounts -p -a {saffile} -F SAF -o {outputtextfile} {bamfile}")


# Iterating all the files to convert bed files in SAF files
# and computing the reads fractions in peaks


for bamFile, outputTextFile in zip(snakemake.input.bamFiles, snakemake.output):
    pool.submit(computefripscore, snakemake.input.safFiles, bamFile, outputTextFile)


pool.shutdown(wait=True)
