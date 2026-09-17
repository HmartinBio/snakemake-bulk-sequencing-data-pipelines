#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""ComputeCoverageMatrix.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to compute the deepTools matrix 
with the command "computeMatrix"from input bigWig files and the reference bed file. 
All the parameters are given by the Snakefile when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ATACAnalysisMamba" is required to
launch this module

This file contains the following functions:
    * computecoveragematrix - Take the bigwig files and the reference bed file to compute the compressed deepTools matrix with the command "computeMatrix"
"""

# Importing librairies

from snakemake import shell


# Creating a function to compute the coverage matrix

def computecoveragematrix(bigwigfiles, bedfile, outputfile, outputfileheatmapmatrix):
    """
    Take the bigwig files and the reference bed file to compute the compressed deepTools matrix with the command "computeMatrix"

    Parameters
    ----------
    bigwigfiles : str
        The file location to the bigWig file
    bedfile : str
        The file location to the reference bed file
    outputfile : str
        The file location to the output compressed matrix
    outputfileheatmapmatrix : str
        The file location to the second uncompressed output matrix
    
    Returns
    -------
    None
    """

    threads = snakemake.threads

    if snakemake.params.typeheatmap == "TSS":
        shell(f'computeMatrix reference-point --referencePoint TSS --missingDataAsZero -p {threads} -S {bigwigfiles} -R {bedfile} -b 3000 -a 3000 -o {outputfile} --outFileNameMatrix {outputfileheatmapmatrix}')
    else:
        shell(f'computeMatrix scale-regions -m 5000 --missingDataAsZero -p {threads} -S {bigwigfiles} -R {bedfile} -b 3000 -a 3000 -o {outputfile} --outFileNameMatrix {outputfileheatmapmatrix}')


# Computing the coverage Matrix for Control and Treated samples

computecoveragematrix(bigwigfiles=snakemake.input.datasetFilesCtrl,
    bedfile=snakemake.input.bedFiles,
    outputfile=snakemake.output.gzipMatrixFile[0], 
    outputfileheatmapmatrix=snakemake.output.heatmapMatrixFile[0])

if not snakemake.params.singleDataset:
    computecoveragematrix(bigwigfiles=snakemake.input.datasetFilesTreat,
    bedfile=snakemake.input.bedFiles,
    outputfile=snakemake.output.gzipMatrixFile[1], 
    outputfileheatmapmatrix=snakemake.output.heatmapMatrixFile[1])
