#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""CountingGenes.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to counts the reads under the genes
with "featureCounts" from BAM files and a reference GTF file

All the parameters are given by the Snakefile 
when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "RNASeqAnalysis" is required to
launch this module

This file contains the following functions:
    * computereadscounts - Take the input BAM file and GTF file to count the reads under genes loci 
"""


# Importing librairies

from concurrent.futures import ThreadPoolExecutor
from snakemake import shell


# Creating the pool for multithreading

pool = ThreadPoolExecutor(max_workers=snakemake.threads)


def computereadscounts(gtffile, bamfile, outputtextfile):
    """
    Take the input BAM file and GTF file to count the reads under genes loci 

    Parameters
    ----------
    gtffile : str
        Pathname to the input GTF file
    bamfile : str
        Pathname to the input BAM file
    outputtextfile : str
        Pathname to the output counts file
    
    Returns
    -------
    None
    """

    if snakemake.params.readsstrandness == "sense":
        shell(f"featureCounts -p -s 1 -a {gtffile} -o {outputtextfile} {bamfile}")
    elif snakemake.params.readsstrandness == "antisense":
        shell(f"featureCounts -p -s 2 -a {gtffile} -o {outputtextfile} {bamfile}")
    else:
        shell(f"featureCounts -p -s 0 -a {gtffile} -o {outputtextfile} {bamfile}")



# Iterating all the files to compute
# the reads counts


for bamfile, outputtextfile in zip(snakemake.input, snakemake.output):

    pool.submit(computereadscounts, snakemake.params.referenceGTF, bamfile, outputtextfile)


pool.shutdown(wait=True)
