#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""ComputeHeatmapAroundTSS.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to compute the heatmap  
from input compressed deepTools matrix. All the parameters are given 
by the Snakefile when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ChIPAnalysisMamba" is required to
launch this module

This file contains the following functions:
    * computeheatmaparoundtss - Take the compressed deepTools matrix file to compute a heatmap with the command "plotHeatmap"
"""

# Importing librairies

from snakemake import shell


# Creating a function to compute the heatmap plot around the TSS

def computeheatmaparoundtss(matrixfile, outputfile):
    """
    Take the compressed deepTools matrix file to compute a heatmap with the command "plotHeatmap"

    Parameters
    ----------
    matrixfile : str
        The file location to the compressed deepTools matrix file
    outputfile : str
        The file location to the output heatmap in pdf format
    
    Returns
    -------
    None
    """
    if snakemake.params.typeheatmap == "TSS":
        shell(f'plotHeatmap --matrixFile {matrixfile} --outFileName {outputfile} --refPointLabel TSS --plotFileFormat pdf')
    else:
        shell(f'plotHeatmap --matrixFile {matrixfile} --outFileName {outputfile} --plotFileFormat pdf')

# Computing the heatmap around TSS for Control and Treated samples

computeheatmaparoundtss(matrixfile=snakemake.input[0], outputfile=snakemake.output[0])

if not snakemake.params.singleDataset:
    computeheatmaparoundtss(matrixfile=snakemake.input[1], outputfile=snakemake.output[1])
