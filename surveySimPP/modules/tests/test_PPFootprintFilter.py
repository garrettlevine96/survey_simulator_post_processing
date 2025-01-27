import numpy as np
import pandas as pd
from numpy.testing import assert_equal, assert_almost_equal

from surveySimPP.tests.data import get_test_filepath
from surveySimPP.modules.PPFootprintFilter import Detector


def dummy_detector():
    # making a square, 0.01 radians a side, bottom left corner at origin.
    # as it's quite small, projection onto focal plane causes minimal distortion (easier to test)
    # previous tests used a 1rad x 1rad unit square, which does not work well.
    return Detector(np.array(((0, 0.01, 0.01, 0), (0, 0, 0.01, 0.01))))


def test_ison():

    detector = dummy_detector()

    points = np.array([np.linspace(0.0, 0.01, 10), np.linspace(0.0, 0.01, 10)])
    points_ison = detector.ison(points)

    assert points_ison.shape == (10,)
    assert_equal(points_ison, np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))


def test_areas():

    from surveySimPP.modules.PPFootprintFilter import radec2focalplane

    detector = dummy_detector()
    pointsin = np.array([np.linspace(0.0, 0.01, 10), np.linspace(0.0, 0.01, 10)])
    pointsout = np.array([np.linspace(0.0, 0.01, 10), np.linspace(0.0, 0.01, 10)]) + 1

    for p in pointsin.T:
        pi = np.array(radec2focalplane(p[0], p[1], 0, 0))
        assert np.abs(detector.segmentedArea(pi) - detector.trueArea()) < 1e-12  # these are stricter tolerances than currently demanded in current use
    for p in pointsout.T:
        pi = np.array(radec2focalplane(p[0], p[1], 0, 0))
        assert np.abs(detector.segmentedArea(pi) - detector.trueArea()) > 1e-12


def test_trueArea():

    detector = dummy_detector()
    assert_almost_equal(detector.trueArea(), 0.0001, decimal=6)


def test_segmentedArea():

    detector = dummy_detector()

    points = np.array([np.linspace(0.0, 0.01, 10), np.linspace(0.0, 0.01, 10)])

    for p in points.T:
        assert_almost_equal(0.0001, detector.segmentedArea(p), decimal=6)


def test_sortCorners():

    # have to rearrange the points for this one
    test_detector = Detector(np.array(((0.01, 0.01, 0, 0), (0, 0.01, 0.01, 0))))
    test_detector.sortCorners()

    assert_almost_equal(test_detector.x, np.array([0., 0.01, 0.01, 0.]), decimal=5)
    assert_almost_equal(test_detector.y, np.array([0., 0., 0.01, 0.01]), decimal=5)


def test_rotateDetector():

    detector = dummy_detector()
    detector_360 = detector.rotateDetector(2. * np.pi)

    assert_almost_equal(detector_360.x, detector.x, decimal=5)
    assert_almost_equal(detector_360.y, detector.y, decimal=5)

    detector_180 = detector.rotateDetector(np.pi)

    assert_almost_equal(detector_180.x, [0, -0.01, -0.01, 0], decimal=5)
    assert_almost_equal(detector_180.y, [0., 0., -0.01, -0.01], decimal=5)


def test_rad2deg_deg2rad():

    detector = dummy_detector()

    original_x = detector.x
    original_y = detector.y

    detector.rad2deg()

    degx_expected = np.array([0., 0.57297689, 0.57297689, 0.])
    degy_expected = np.array([0., 0., 0.57300554, 0.57297689])

    assert_almost_equal(detector.x, degx_expected)
    assert_almost_equal(detector.y, degy_expected)

    detector.deg2rad()

    assert_almost_equal(detector.x, original_x)
    assert_almost_equal(detector.y, original_y)


def test_plots():

    from surveySimPP.modules.PPFootprintFilter import Footprint

    detector = dummy_detector()
    detector.plot()

    footprintf = Footprint(get_test_filepath('detectors_corners.csv'))
    footprintf.plot()


def test_radec2focalplane():

    from surveySimPP.modules.PPFootprintFilter import radec2focalplane

    out = radec2focalplane(1., 1., 0., 0.)
    out_expected = (1.5574077, 2.8824746)

    assert len(out) == 2
    assert_almost_equal(out, out_expected, decimal=6)


def test_applyFootprint():

    from surveySimPP.modules.PPFootprintFilter import Footprint

    observations = pd.read_csv(get_test_filepath('test_input_fullobs.csv'), nrows=10)

    footprintf = Footprint(get_test_filepath('detectors_corners.csv'))
    onSensor, detectorIDs = footprintf.applyFootprint(observations)

    assert_equal(onSensor, [1, 0, 2, 3, 8, 7, 4, 5, 6, 9])
    assert_equal(detectorIDs, [59., 66., 87., 87., 100., 106., 127., 131., 144., 152.])

    return
