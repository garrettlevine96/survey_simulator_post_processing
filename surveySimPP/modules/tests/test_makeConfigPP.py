import os
import configparser

from surveySimPP.utilities.makeConfigPP import makeConfigFile
from surveySimPP.tests.data import get_test_filepath


class args:
    def __init__(self, filename):
        args.filename = filename
        self.ephemeridestype = 'oif'
        self.pointingdatabase = get_test_filepath('baseline_10klines_2.0.db')
        self.ephformat = 'whitespace'
        self.auxformat = 'whitespace'
        self.sizeserialchunk = 10
        self.cometactivity = 'none'
        self.observingfilters = 'r,u,g,i,z,y'
        self.brightlimit = 16.0
        self.phasefunction = 'HG'
        self.cameramodel = 'footprint'
        self.footprintpath = 'detectors_corners.csv'
        self.fillfactor = None
        self.circleradius = None
        self.fadingfunction = True
        self.fadingwidth = 0.1
        self.fadingpeak = 1.
        self.detectionefficiency = 0.95
        self.numobservations = 2.
        self.numtracklets = 3
        self.trackwindow = 15.0
        self.septhreshold = 0.5
        self.outputformat = 'csv'
        self.outputsize = 'default'
        self.positiondecimals = 7
        self.magnitudedecimals = 3
        self.snrlimit = None
        self.maglimit = None
        self.sqlquery = 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId'
        self.trailinglosseson = True


def test_makeConfigPP(tmp_path):

    arg_test = args(os.path.join(tmp_path, 'testconfig.ini'))

    makeConfigFile(arg_test)

    config_expected = configparser.ConfigParser()
    config_expected.read(get_test_filepath('makeConfigPP_config.ini'))

    config_test = configparser.ConfigParser()
    config_test.read(os.path.join(tmp_path, 'testconfig.ini'))

    config_test.set('INPUT', 'pointing_database', '../tests/data/baseline_10klines_2.0.db')

    assert config_expected == config_test

    return
