#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""MergeBigWig.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to merge BAM and bigWig files". 

All the parameters are given by the Snakefile 
when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "RNASeqAnalysis" is required to
launch this module

This file contains the following functions:
    * mergebamfiles - Take the input BAM files to merge them with "samtools merge"
    * computebigwigfile - Take the BAM files to compute a bigWig file with the command "bamCoverage"
    * comparebigwig - Take the Control and Treated bigWig files and generate a new bigWig with "bigwigCompare" function
"""

# Importing librairies

import os
import tempfile
from snakemake import shell


# Computing the effective genome size (part of the gemome which is mappable)
# for the normalisation of the library

referencegenome = snakemake.params.referenceGenome
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



cpuspertaks = snakemake.params.cpusPerTasks


def mergebamfiles(bamfiles, outputbamfile, outputbamindexedfiles):
    """
    Take the input BAM files to merge them with "samtools merge"

    Parameters
    ----------
    bamfiles : str
        Space-separated pathnames to the input  
    outputbamfile : str
        Pathname to the reverse paired-end FASTQ file
    outputbamindexedfiles : str
        Pathname to the output SAM file
    Returns
    -------
    None
    """

    shell(f'samtools merge --threads {cpuspertaks} {outputbamfile} {bamfiles} && samtools index {outputbamfile} {outputbamindexedfiles}')



def computebigwigfile(bamfile, outputbigwigfile):
    """
    Take the BAM files to compute a bigWig file with the command "bamCoverage"

    Parameters
    ----------
    bamfile : str
       The file location to the bamfile
    outputbigwigfile : str
        The file location to the output bigWig
    
    Returns
    -------
    None
    """

    shell(f"bamCoverage -b {bamfile} -p {cpuspertaks} -o {outputbigwigfile} --binSize=25 --normalizeUsing=RPGC --effectiveGenomeSize={effectiveGenomeSize}")



# Merging the bam files

mergebamfiles(bamfiles=snakemake.input.bamFilescontrol,
    outputbamfile=snakemake.output.bamFilesMerged[0],
    outputbamindexedfiles=snakemake.output.bamFilesIndexMerged[0])

if not snakemake.params.singleDataset:

    mergebamfiles(bamfiles=snakemake.input.bamFilestreated,
        outputbamfile=snakemake.output.bamFilesMerged[1], 
        outputbamindexedfiles=snakemake.output.bamFilesIndexMerged[1])

# Computing the bigwig files

computebigwigfile(bamfile=snakemake.output.bamFilesMerged[0],
    outputbigwigfile=snakemake.output.bigWigMergedFiles[0])

if not snakemake.params.singleDataset:
    computebigwigfile(bamfile=snakemake.output.bamFilesMerged[1],
    outputbigwigfile=snakemake.output.bigWigMergedFiles[1])
