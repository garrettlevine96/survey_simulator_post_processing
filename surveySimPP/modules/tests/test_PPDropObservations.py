import pandas as pd
import numpy as np
from numpy.testing import assert_equal

from surveySimPP.tests.data import get_test_filepath


def test_PPDropObservations():

    from surveySimPP.modules.PPDetectionProbability import PPDetectionProbability
    from surveySimPP.modules.PPDropObservations import PPDropObservations

    rng = np.random.default_rng(2021)

    test_data = pd.read_csv(get_test_filepath('test_input_fullobs.csv'), nrows=10)
    test_data["detection_probability"] = PPDetectionProbability(test_data, fillFactor=0.8, w=0.1)

    test_out = PPDropObservations(test_data, rng, "detection_probability")

    expected = [894816, 897478, 897521, 901987, 902035, 907363, 907416, 907470,
                909426]

    assert_equal(test_out['FieldID'].values, expected)

    return
