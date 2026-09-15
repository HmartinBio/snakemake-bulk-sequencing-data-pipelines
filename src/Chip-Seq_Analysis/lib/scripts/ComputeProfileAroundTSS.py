#!/usr/bin/env python3

# -*- coding:utf-8 -*-

"""ComputeProfileAroundTSS.py
Author: Hugo N.G.Martin

This module allows from the Snakemake workflow to compute the profile plot  
from input compressed deepTools matrix. All the parameters are given 
by the Snakefile when the workflow is running. 

This module should be run exclusively by the Snakemake workflow

The activation of the mamba environment "ChIPAnalysisMamba" is required to
launch this module

This file contains the following functions:
    * computeprofilearoundtss - Take the compressed deepTools matrix file to compute a profile with the command "plotProfile"
"""

# Importing librairies

from snakemake import shell


# Creating a function to compute the profile plot around the TSS

def computeprofilearoundtss(matrixfile, outputfile):
    """
    Take the compressed deepTools matrix file to compute a profile with the command "plotProfile"

    Parameters
    ----------
    matrixfile : str
        The file location to the compressed deepTools matrix file
    outputfile : str
        The file location to the output profile plot in pdf format
    
    Returns
    -------
    None
    """

    if snakemake.params.typeheatmap == "TSS":
        shell(f'plotProfile --matrixFile {matrixfile} --outFileName {outputfile} --refPointLabel TSS')
    else:
        shell(f'plotProfile --matrixFile {matrixfile} --outFileName {outputfile}')

# Computing the profile around TSS for Control and Treated samples

computeprofilearoundtss(matrixfile=snakemake.input[0], outputfile=snakemake.output[0])

if not snakemake.params.singleDataset:
    computeprofilearoundtss(matrixfile=snakemake.input[1], outputfile=snakemake.output[1])
