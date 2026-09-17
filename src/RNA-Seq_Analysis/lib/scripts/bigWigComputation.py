#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""bigWigComputation.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to compute bigWig 
from input bamFiles. All the parameters are given by the Snakefile 
when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "RNASeqAnalysis" is required to
launch this module

This file contains the following functions:
    * librarysizenormalisation - Take the bam files to compute a bigWig file with the command "bamCoverage"
"""

# Importing librairies

from concurrent.futures import ThreadPoolExecutor
import tempfile
import os
from snakemake import shell


# Creating the pool for multithreading

threadsNumb = int(snakemake.threads / snakemake.params.cpusPerTasks)

pool = ThreadPoolExecutor(max_workers=threadsNumb)


# Computing the effective genome size (part of the gemome which is mappable)
# for the normalisation of the library

referencegenome=snakemake.params.referenceGenome
tempFile = tempfile.NamedTemporaryFile(delete=False)

try:
    shell(f'expr "$(faCount {referencegenome} | tail -n 1 | cut -f 2)" - $(faCount {referencegenome} | tail -n 1 | cut -f 7) > {tempFile.name}')
    
    # Extracting the information written in bytes in the temp file

    effectiveGenomeSize = tempFile.readline()
    
    # Converting in string
    
    effectiveGenomeSize = effectiveGenomeSize.decode("utf-8")
    effectiveGenomeSize = effectiveGenomeSize.replace("\n", "")

finally:
    tempFile.close()

# Creating the function to normalise the library size


def librarysizenormalisation(bamfile, outputbigwig):
    """
    Take the bam files to compute a bigWig file with the command "bamCoverage"

    Parameters
    ----------
    bamfile : str
        The file location of the bamfile
    outputbigwig : str
        The file location of the output bigWig
    
    Returns
    -------
    None
    """

    threads = snakemake.params.cpusPerTasks

    shell(f"bamCoverage -p {threads} -b {bamfile} -o {outputbigwig} --binSize=25 --normalizeUsing=RPGC --effectiveGenomeSize={effectiveGenomeSize}")



# Iterating all the files in the folders to build the BigWig files

for inputFile, outputBamFile in zip(snakemake.input, snakemake.output):

    pool.submit(librarysizenormalisation, inputFile, outputBamFile)


pool.shutdown(wait=True)
