#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""SamStats.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to compute 
Quality control metrics with "samtools" from input SAM/BAM files. 
All the parameters are given by the Snakefile when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "RNASeqAnalysis" is required to
launch this module

This file contains the following functions:
    * samstatsreports - Take the input SAM file to compute statistics with "samtools stats"
    * samflagreports - Take the input SAM file to compute statistics with "samtools flagstat"
    * plotbamstats - Take the output "samtools stats" results to compute a plot
    * generatingreports - Launch the functions (samstatsreports,samflagreports,plotbamstats) to generate stats and plots
"""

# Importing librairies

from concurrent.futures import ThreadPoolExecutor
from snakemake import shell



# Creating the pool for multithreading

pool = ThreadPoolExecutor(max_workers=snakemake.threads)


def samstatsreports(samfile, outputreportfile):
    """
    Take the input SAM file to compute statistics with "samtools stats"

    Parameters
    ----------
    samfile : str
        The file location to the SAM/BAM file
    outputreportfile : str
        The file location to the output text file
    
    Returns
    -------
    None
    """

    shell(f'samtools stats -d {samfile} > {outputreportfile}')


def samflagreports(samfile, outputreportfile):
    """
    Take the input SAM file to compute statistics with "samtools flagstat"

    Parameters
    ----------
    samfile : str
        The file location to the SAM/BAM file
    outputreportfile : str
        The file location to the output text file
    
    Returns
    -------
    None
    """

    shell(f'samtools flagstat {samfile} > {outputreportfile}')


def plotbamstats(reportfile, outputdirectory):
    """
    Take the output "samtools stats" results to compute a plot

    Parameters
    ----------
    samfile : str
        The file location to the SAM/BAM file
    outputdirectory : str
        The folder location to save the outputs
    
    Returns
    -------
    None
    """

    shell(f'plot-bamstats -p {outputdirectory} {reportfile}')


def generatingreports(samfile, outputreportfilesamstats, outputreportfileflagstats, outputdirectory):
    """
    Launch the functions (samstatsreports,samflagreports,plotbamstats) to generate stats and plots

    Parameters
    ----------
    samfile : str
        The file location to the SAM/BAM file
    outputreportfilesamstats : str
        The file location to the "samtools stat" output text file
    outputreportfileflagstats: str
        The file location to the "samtools flagstat" output text file
    outputdirectory : str
        The folder location to the output directory to save the plot from "plot-bamstats"
    
    Returns
    -------
    None
    """

    samstatsreports(samfile=samfile, outputreportfile=outputreportfilesamstats)
    samflagreports(samfile=samfile, outputreportfile=outputreportfileflagstats)
    plotbamstats(reportfile=outputreportfilesamstats, outputdirectory=outputdirectory)


# Iterating all the files in the folders to get the reports results

for samFile, outputReportSamStats, outputReportSamFlag, outputFolder in\
    zip(snakemake.input, snakemake.output.SamStatsReports,
    snakemake.output.SamFlagsReports, snakemake.params.plotFolder):

    # Getting the results

    pool.submit(generatingreports, samFile, outputReportSamStats,
        outputReportSamFlag, outputFolder)

   
pool.shutdown(wait=True)

