#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""Mapping.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to map the reads from FASTQ files
with "Bowtie2"

All the parameters are given by the Snakefile 
when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ChIPAnalysisMamba" is required to
launch this module

This file contains the following function:
    * bowtiealignment - Take the paired-end FASTQ files to map the reads
"""

# Importing librairies

from concurrent.futures import ThreadPoolExecutor
import re
import os
from snakemake import shell


# Creating the pool for multithreading

threadsNumb = int(snakemake.threads / snakemake.params.cpusPerTasks)

pool = ThreadPoolExecutor(max_workers=threadsNumb)


# Building the bowtie2 database from reference genome

threadsnumber = snakemake.threads
cpuspertasks = snakemake.params.cpusPerTasks
referencegenome = snakemake.params.referenceGenome
genomeindexfolder = snakemake.params.genomeIndexFolder
organismname = snakemake.params.organism

if len(os.listdir(snakemake.params.genomeIndexFolder)) == 0:

    shell(f"bowtie2-build --threads {threadsnumber} {referencegenome} {genomeindexfolder}/{organismname}")


pathToGenomeIndexed = f"{genomeindexfolder}/{organismname}"

# Creating the list of files to get from input folders

fastqFiles = []



def bowtiealignment(forwardfile, reversefile, outputfile):
    """
    Take the paired-end FASTQ files to map the reads

    Parameters
    ----------
    forwardfile : str
        Pathname to the forward paired-end FASTQ file
    reversefile : str
        Pathname to the reverse paired-end FASTQ file
    outputfile : str
        Pathname to the output SAM file
    Returns
    -------
    None
    """

    shell(f"bowtie2 --threads {cpuspertasks} -x {pathToGenomeIndexed} -1 {forwardfile} -2 {reversefile} --no-unal -S {outputfile}")


# Iterating all the files in the folders to make the mapping against the reference genome

for inputFolder, outputFile in zip(snakemake.input, snakemake.output):

    listOfFilesInsideDirectory = os.listdir(inputFolder)

    # Iterating all the files in the folders

    for file in listOfFilesInsideDirectory:

        if file.endswith('.fq.gz'):
            fastqFiles.append(file)

    if re.match('_val_1', fastqFiles[0]):
        pool.submit(bowtiealignment, f"{inputFolder}/{fastqFiles[0]}", f"{inputFolder}/{fastqFiles[1]}", outputFile)

    else:
        pool.submit(bowtiealignment, f"{inputFolder}/{fastqFiles[1]}", f"{inputFolder}/{fastqFiles[0]}", outputFile)

    fastqFiles = []

pool.shutdown(wait=True)
