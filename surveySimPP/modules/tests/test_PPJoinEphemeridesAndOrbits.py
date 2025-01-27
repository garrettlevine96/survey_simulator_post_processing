from surveySimPP.tests.data import get_test_filepath
from numpy.testing import assert_equal


def test_PPJoinEphemeridesAndOrbits():

    from surveySimPP.modules.PPJoinEphemeridesAndOrbits import PPJoinEphemeridesAndOrbits
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile

    oif_file = PPReadOif(get_test_filepath('oiftestoutput.txt'), 'whitespace')
    orbit_file = PPReadOrbitFile(get_test_filepath('testorb.des'), 0, 5, 'whitespace')

    joined_df = PPJoinEphemeridesAndOrbits(oif_file, orbit_file)

    first_row = ['S00000t', 379, 59853.205174, 283890475.515, -1.12, 11.969664,
                 -0.280799, -0.19939, -0.132793, 426166274.581, 77286024.759,
                 6987943.309, -2.356, 11.386, 4.087, 148449956.422, 18409281.409,
                 7975891.432, -4.574, 27.377, 11.699, 2.030016, 0.952105479028,
                 0.504888475701, 4.899098347472, 148.881068605772, 39.949789586436,
                 54486.32292808, 54466.0]

    assert_equal(joined_df.iloc[0].values[1:], first_row[1:])
    assert first_row[0] == 'S00000t'
    assert len(joined_df.columns) == 29

    return
