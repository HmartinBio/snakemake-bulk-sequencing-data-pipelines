#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""MarkDuplicates.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to filter the PCR duplicates with "picard MarkDuplicates". 

All the parameters are given by the Snakefile 
when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ATACAnalysisMamba" is required to
launch this module

This file contains the following function:
    * markduplciates - Take the BAM files to filter the PCR duplicates with "picard MarkDuplicates"
"""


# Importing librairies

from concurrent.futures import ThreadPoolExecutor
from snakemake import shell


# Creating the pool for multithreading

pool = ThreadPoolExecutor(max_workers=snakemake.threads)


def markduplicates(bamfile, outputbamfile, outputmetricsfile, outputbamindexedfiles):
    """
    Take the BAM files to filter the PCR duplicates with "picard MarkDuplicates"

    Parameters
    ----------
    bamfile : str
        Pathname to the input BAM file to filter
    outputbamfile : str
        Pathname to the filtered output BAM file
    outputmetricsfile : str
        Pathname to the output file containing the filtering summary
    outputbamindexedfiles : str
        Pathname to the filtered output indexed BAM file
    Returns
    -------
    None
    """

    shell(f"picard MarkDuplicates I={bamfile} O={outputbamfile} M={outputmetricsfile} REMOVE_DUPLICATES=true && samtools index {outputbamfile} {outputbamindexedfiles}")


# Iterating all the files in the folders to filter PCR duplicates accross all the bam files

for inputFile, outputBamFile, outputMetricsFile, outputBamIndexedFiles in\
    zip(snakemake.input, snakemake.output.bamFiles,
    snakemake.output.metricsFiles, snakemake.output.indexedBamFiles):

    # Filtering duplictaes reads

    pool.submit(markduplicates, inputFile, outputBamFile, outputMetricsFile, outputBamIndexedFiles)

pool.shutdown(wait=True)

