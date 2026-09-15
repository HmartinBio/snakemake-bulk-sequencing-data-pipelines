#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""FASTQC.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to compute a first FASTQC from the
input FASTQ files to check the control quality metrics from the FASTQ files

All the parameters are given by the Snakefile when the workflow is running.

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ChIPAnalysisMamba" is required to
launch this module

This file contains the following functions:
    * fastqc - Take the input FASTQ files to generate first FASTQC reports before Trimming
"""

# Importing librairies

from concurrent.futures import ThreadPoolExecutor
from snakemake import shell


# Creating a pool of threads

threadsNumb = int(snakemake.threads / snakemake.params.cpusPerTasks)

pool = ThreadPoolExecutor(max_workers=threadsNumb)


def fastqc(inputfile, outputfolder):
    """
    Take the input FASTQ files to generate first FASTQC reports before Trimming

    Parameters
    ----------
    inputfile : str
        The file location to the FASTQ files
    outputfolder : str
        The file location to the output file in a SAF format
    
    Returns
    -------
    None
    """

    threads = snakemake.params.cpusPerTasks
    shell(f"fastqc {inputfile} -o {outputfolder} -t {threads}")


# Iterating all the files in the folders to make the FASTQC report

for inputFile, outputFolder in zip(snakemake.input, snakemake.params.outputFolders):

    pool.submit(fastqc, inputFile, outputFolder)

pool.shutdown(wait=True)