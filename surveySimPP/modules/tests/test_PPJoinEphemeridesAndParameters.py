#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPJoinEphemeridesAndParameters():

    from surveySimPP.modules.PPJoinEphemeridesAndParameters import PPJoinEphemeridesAndParameters
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters

    padafr = PPReadOif(get_test_filepath('oiftestoutput.txt'), 'whitespace')
    padacl = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 5, 'whitespace')

    padare = PPJoinEphemeridesAndParameters(padafr, padacl)

    ncol = 27
    ncolre = len(padare.columns)

    assert ncol == ncolre
    return