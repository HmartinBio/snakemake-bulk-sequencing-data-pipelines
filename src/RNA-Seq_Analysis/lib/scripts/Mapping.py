#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""Mapping.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to map the reads from FASTQ files
with "STAR"

All the parameters are given by the Snakefile 
when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "RNASeqAnalysis" is required to
launch this module

This file contains the following function:
    * staralignment - Take the paired-end FASTQ files to map the reads
"""

# Importing librairies

from concurrent.futures import ThreadPoolExecutor
import os
import math
import tempfile
from snakemake import shell

# Creating the pool for multithreading


threadsNumb = int(snakemake.threads / snakemake.params.cpusPerTasks)

#pool = ThreadPoolExecutor(max_workers=snakemake.threads)
pool = ThreadPoolExecutor(max_workers=10)

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


# Counting the number of sequences in the Genome fasta file

FASTASEQUENCESCOUNTER=0

with open(f"{referencegenome}", "r", encoding="utf-8") as fastaReferenceSequences:
    for lineFasta in fastaReferenceSequences:
        if lineFasta.startswith(">"):
            FASTASEQUENCESCOUNTER += 1


# Building the index from the reference genome

threadsnumber = snakemake.threads
referencegtf = snakemake.params.referenceGTF
ratiogenomereference = min(18, math.log2((int(effectiveGenomeSize))/FASTASEQUENCESCOUNTER))


shell(f"STAR --runThreadN {threadsnumber} --runMode genomeGenerate --genomeFastaFiles {referencegenome}\
    --sjdbGTFfile {referencegtf} --genomeChrBinNbits {ratiogenomereference} --limitGenomeGenerateRAM 64000000000")


# Creating the list of files to get from input folders

fastqFiles = []



def staralignment(forwardfile, reversefile, outputfile):
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

    outputfile = outputfile.split(".")[0]
    outputfile = outputfile + ".sam"

    shell(f"STAR --readFilesIn {forwardfile} {reversefile} --outFileNamePrefix {outputfile} --runThreadN {threadsNumb}")


# Iterating all the files in the folders to make the mapping against the reference genome

for inputFolder, outputFile in zip(snakemake.input, snakemake.output):

    listOfFilesInsideDirectory = os.listdir(inputFolder)

    # Iterating all the files in the folders

    for file in listOfFilesInsideDirectory:

        if file.endswith('.fq'):
            fastqFiles.append(file)

    outputFileSplitted = outputFile.split(".fq")[0]

    if fastqFiles[0].endswith('_val_1.fq'):
        pool.submit(staralignment, inputFolder + '/' + fastqFiles[0],
            inputFolder + '/' + fastqFiles[1], outputFileSplitted)

    else:
        pool.submit(staralignment, inputFolder + '/' + fastqFiles[1],
            inputFolder + '/' + fastqFiles[0], outputFileSplitted)

    fastqFiles = []

pool.shutdown(wait=True)
