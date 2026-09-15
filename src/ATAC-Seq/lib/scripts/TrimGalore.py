#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""TrimGalore.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to perform the reads
trimming on the FASTQ files with TrimmGalore 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ATACAnalysisMamba" is required to
launch this module

This file contains the following functions:
    * trimming - Take the input FASTQ files and perform the trimming with "trim_galore"
"""


# Importing librairies

from concurrent.futures import ThreadPoolExecutor
from snakemake import shell


# Creating the pool for multithreading

threadsNumb = int(snakemake.threads / snakemake.params.cpusPerTasks)

pool = ThreadPoolExecutor(max_workers=threadsNumb)

cpuspertask = snakemake.params.cpusPerTasks



def trimming(inputfile, outputdir, cpus):
    """
    Take the input FASTQ files and perform the trimming with "trim_galore"

    Parameters
    ----------
    inputfile : str
        Space-separated paired-end FASTQ files
    outputdir : str
        The location of the output folder to save the trimmed FASTQ files
    cpus : str
        Number of CPUs to give to the job

    Returns
    -------
    None
    """

    shell(f"trim_galore -j {cpus} --paired --illumina {inputfile} -o {outputdir} --fastqc")



# Iterating all the files and output folders


for iterationCounter in range(0, len(snakemake.input)):

    # If the counter points on files where position is a multiple of 2

    if iterationCounter % 2 == 0:
        LISTINPUTFILES = snakemake.input[iterationCounter:iterationCounter + 2]
        LISTINPUTFILES = ' '.join(LISTINPUTFILES)

        # If the counter is at 0, the output folder selected is the first one

        if iterationCounter == 0:
            outputDirectory = snakemake.params.outputFolders[0]

        # Giving that there are less output folders/files than input files ("2x less")
        # the iteration counter is substracted to the half of the counter

        else:
            outputDirectory = snakemake.params.outputFolders[
                int(iterationCounter - (iterationCounter / 2))]

        # Performing the trimming

        pool.submit(trimming, LISTINPUTFILES, outputDirectory, cpuspertask)

        iterationCounter += 1

    else:
        iterationCounter += 1

pool.shutdown(wait=True)
