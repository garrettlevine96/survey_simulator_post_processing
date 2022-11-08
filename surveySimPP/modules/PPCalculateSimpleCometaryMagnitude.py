#!/usr/bin/python

from surveySimPP.lsstcomet import Comet
import numpy as np

# Author: Grigori Fedorets and Steph Merritt
# Using lsstcomet code by Mike Kelley
# (C)  LSST Solar System Scientific Collaboration 2019


def PPCalculateSimpleCometaryMagnitude(padain, mainfilter, othercolours, colname='TrailedSourceMag'):
    """
    PPCalculateSimpleCometaryMagnitude.py

    Description: This task calculates the brightness of the comet at a given pointing
    according to a simple model by A'Hearn et al. (1984).

    The brightness is calculated first in the main filter, and the colour offset is
    applied afterwards.

    Mandatory input:      string, padain, name of input pandas dataframe
                          string, mainfilter, name of the main filter in which
                                  the brightness is calculated
                          list, othercolours, list of colour offsets present in input files
                          colname, string, name of output column for apparent magnitude

    Output:

    usage: padaout=PPCalculateSimpleCometaryMagnitude(padain)


    """
    # calculate rho and delta in au
    delta = padain['AstRange(km)'].values / 1.495978707e8

    try:
        rho = padain["Ast-Sun(km)"].values / 1.495978707e8
    except KeyError:
        rho = np.sqrt(padain["Ast-Sun(J2000x)(km)"].values**2
                      + padain["Ast-Sun(J2000y)(km)"].values**2
                      + padain["Ast-Sun(J2000z)(km)"].values**2) / 1.495978707e8

    com = Comet(Hv=padain.H, afrho1=padain.afrho1, q=padain.q, k=padain.k)

    g = {'rh': rho, 'delta': delta, 'phase': padain['Sun-Ast-Obs(deg)']}

    padain['coma'] = com.mag(g, mainfilter, rap=1, nucleus=False)

    # The contribution of the nucleus is taken from the absolute brightness
    padain[colname] = -2.5 * np.log10(10 ** (-0.4 * padain['coma']) + 10 ** (-0.4 * padain['H']))

    # We then calculate the colour offset.
    padain[mainfilter + "-" + mainfilter] = np.zeros(len(padain))
    padain[colname] = padain.apply(lambda row: row[colname] + row[row['optFilter'] + "-" + mainfilter], axis=1)
    padain.drop(mainfilter + "-" + mainfilter, axis=1, inplace=True)

    if othercolours != '':
        padain.drop(othercolours, axis=1, inplace=True)

    return padain
