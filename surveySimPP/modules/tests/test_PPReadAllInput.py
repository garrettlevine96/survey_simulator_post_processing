import numpy as np
from numpy.testing import assert_equal

from surveySimPP.tests.data import get_test_filepath


def test_PPReadAllInput():

    from surveySimPP.modules.PPReadAllInput import PPReadAllInput
    from surveySimPP.modules.PPReadPointingDatabase import PPReadPointingDatabase

    cmd_args = {'paramsinput': get_test_filepath('PPReadAllInput_params.txt'),
                'orbinfile': get_test_filepath('PPReadAllInput_orbits.des'),
                'oifoutput': get_test_filepath('PPReadAllInput_oif.txt'),
                'configfile': get_test_filepath('test_PPConfig.ini'),
                'outpath': './',
                'makeTemporaryEphemerisDatabase': False,
                'readTemporaryEphemerisDatabase': None,
                'verbose': False}

    configs = {'comet_activity': 'none',
               'aux_format': 'whitespace',
               'ephemerides_type': 'oif',
               'eph_format': 'csv',
               'pointing_database': get_test_filepath('baseline_10klines_2.0.db'),
               'observing_filters': ['u', 'g', 'r', 'i', 'z', 'y'],
               'pointing_sql_query': 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId'}

    filterpointing = PPReadPointingDatabase(configs['pointing_database'], configs['observing_filters'], configs['pointing_sql_query'])

    observations = PPReadAllInput(cmd_args, configs, filterpointing, 0, 10)

    expected_first_line = np.array(['356450', 5829, 60225.290116, 5709680780.633022, 2.95, 11.320281,
                                    -0.020243, -2.295485, -0.008657, 5738902320.406, 1154027739.313,
                                    -213890855.795, -1.124, 4.256, 1.338, 144794459.312,
                                    34155591.729, 14799446.73, -8.201, 26.631, 11.433, 0.20886, 7.99,
                                    2.55, 0.92, -0.38, -0.59, -0.7, 0.15, 54466.0, 90480.35745, 7.89,
                                    144.25849, 8.98718, 0.09654, 33.01305, 'z', 0.7299771787487132,
                                    0.8247897551687507, 23.007819521794538, 11.104605793427162,
                                    -1.2000819393055593, 273.9055664032884], dtype=object)

    expected_columns = np.array(['ObjID', 'FieldID', 'FieldMJD', 'AstRange(km)',
                                 'AstRangeRate(km/s)', 'AstRA(deg)', 'AstRARate(deg/day)',
                                 'AstDec(deg)', 'AstDecRate(deg/day)', 'Ast-Sun(J2000x)(km)',
                                 'Ast-Sun(J2000y)(km)', 'Ast-Sun(J2000z)(km)',
                                 'Ast-Sun(J2000vx)(km/s)', 'Ast-Sun(J2000vy)(km/s)',
                                 'Ast-Sun(J2000vz)(km/s)', 'Obs-Sun(J2000x)(km)',
                                 'Obs-Sun(J2000y)(km)', 'Obs-Sun(J2000z)(km)',
                                 'Obs-Sun(J2000vx)(km/s)', 'Obs-Sun(J2000vy)(km/s)',
                                 'Obs-Sun(J2000vz)(km/s)', 'Sun-Ast-Obs(deg)', 'H_r', 'u-r', 'g-r',
                                 'i-r', 'z-r', 'y-r', 'GS', 't_0', 't_p', 'argperi', 'node', 'incl',
                                 'e', 'q', 'optFilter', 'seeingFwhmGeom', 'seeingFwhmEff',
                                 'fiveSigmaDepth', 'fieldRA', 'fieldDec', 'rotSkyPos'], dtype=object)

    assert_equal(observations.columns.values, expected_columns)
    assert_equal(expected_first_line, observations.iloc[0].values)

    assert len(observations) == 10

    return
