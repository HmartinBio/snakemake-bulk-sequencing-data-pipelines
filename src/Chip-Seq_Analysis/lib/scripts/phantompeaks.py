#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""phantompeaks.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to compute Strand-Cross correlation 
information from BAM files". 

All the parameters are given by the Snakefile 
when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ChIPAnalysisMamba" is required to
launch this module

This file contains the following function:
    * phantompeaks - Take the input BAM file and compute a plot of the Strand-Cross correlation
"""

# Importing librairies

from concurrent.futures import ThreadPoolExecutor
from snakemake import shell


# Creating the pool for multithreading

pool = ThreadPoolExecutor(max_workers=snakemake.threads)

condaenvpathname = snakemake.params.CondaEnvPathName



def phantompeaks(bamfile, outputplotfigure, outputfileresults):
    """
    Take the input BAM file and compute a plot of the Strand-Cross correlation

    Parameters
    ----------
    bamfile : str
        The file location to the BAM file
    outputplotfigure : str
        The file location to the output figure
    outputfileresults : str
        The file location to the output text file
    Returns
    -------
    None
    """

    shell(f"Rscript {condaenvpathname}/bin/run_spp.R -c={bamfile} -savp={outputplotfigure} -rf -out={outputfileresults}")


# Iterating all the files in the folders to get the Strand-Cross correlation results

for inputFile, outputPlotFigure, outputFileResults in zip(snakemake.input,
    snakemake.output.phantomPeaksPictures, snakemake.output.phantomPeaksResults):

    # Getting the results

    pool.submit(phantompeaks, inputFile, outputPlotFigure, outputFileResults)


pool.shutdown(wait=True)
