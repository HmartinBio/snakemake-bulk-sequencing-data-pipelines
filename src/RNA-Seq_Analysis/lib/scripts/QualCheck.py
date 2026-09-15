#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""QualCheck.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to compute 
Quality control metrics with "RSeQC" from input BAM files. 
All the parameters are given by the Snakefile when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "RNASeqAnalysis" is required to
launch this module

This file contains the following functions:
    * determinestrandness - Take the input BAM file to compute reads strandness information results
    * checkmappingchromosome - Take the input BAM file to compute chromosome mapping information results
    * checkbodycoverage - Take the input BAM file to compute gene body coverage information results
    * checkgenesdistribution - Take the input BAM file to compute reads distribution results
"""

# Importing librairies

from concurrent.futures import ThreadPoolExecutor
from snakemake import shell


# Creating the pool for multithreading

pool = ThreadPoolExecutor(max_workers=snakemake.threads)


referencebedgenefile = snakemake.params.bedGenesFiles


def determinestrandness(bamfile, outputmetricsfile, bedgenefile):
    """
    Take the input BAM file to compute reads strandness information results

    Parameters
    ----------
    bamfile : str
        The file location to the BAM file
    outputmetricsfile : str
        The file location to the output text file
    bedgenefile : str
        The file location to the reference BED gene file
    
    Returns
    -------
    None
    """

    shell(f"infer_experiment.py -r {bedgenefile} -i {bamfile} 2>&1> {outputmetricsfile}")


def checkmappingchromosome(bamfile, outputmetricsfile):
    """
    Take the input BAM file to compute chromosome mapping information results

    Parameters
    ----------
    bamfile : str
        The file location to the BAM file
    outputmetricsfile : str
        The file location to the output text file
    
    Returns
    -------
    None
    """

    shell(f"samtools idxstats {bamfile} 2>&1> {outputmetricsfile}")



def checkbodycoverage(bamfile, outputmetricsfile):
    """
    Take the input BAM file to compute gene body coverage information results

    Parameters
    ----------
    bamfile : str
        The file location to the BAM file
    outputmetricsfile : str
        The file location to the output text file
    
    Returns
    -------
    None
    """

    shell(f"geneBody_coverage.py -i {bamfile} 2>&1> {outputmetricsfile}")




def checkgenesdistribution(bamfile, outputmetricsfile, bedgenefile):
    """
    Take the input BAM file to compute reads distribution results

    Parameters
    ----------
    bamfile : str
        The file location to the BAM file
    outputmetricsfile : str
        The file location to the output text file
    bedgenefile : str
        The file location to the reference BED gene file

    Returns
    -------
    None
    """

    shell(f"read_distribution.py -i {bamfile} -r {bedgenefile} 2>&1> {outputmetricsfile}")


# Iterating all the files in the folders to filter PCR duplicates accross all the bam files


for inputFile, outputStrandMetricsFile, outpuCheckCoverageMetricsFile,\
    outputMappingCoverageMetricsFile, outputGenesDistributionMetricsFile in zip(
        snakemake.input, snakemake.output.strandnessOutputFiles,
        snakemake.output.checkCoverageOutputFiles, snakemake.output.mappingCoverageOutputFiles,
        snakemake.output.genesDistribOutputFiles):


    # Checking quality control metrics from samples

    pool.submit(determinestrandness, inputFile, outputStrandMetricsFile, referencebedgenefile)
    pool.submit(checkmappingchromosome, inputFile, outpuCheckCoverageMetricsFile)
    pool.submit(checkbodycoverage, inputFile, outputMappingCoverageMetricsFile)
    pool.submit(checkgenesdistribution, inputFile, outputGenesDistributionMetricsFile, referencebedgenefile)

pool.shutdown(wait=True)
