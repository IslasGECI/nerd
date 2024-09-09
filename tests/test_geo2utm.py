import pandas as pd
from nerd.io import _geo2utm
from pandas._testing import assert_frame_equal


def test_geo2utm():
    expected_utm_data = pd.read_csv("tests/data/expected_utm_data.csv")
    obtained_utm_data = _geo2utm(csv_filename="tests/data/expected_utm_data.csv")
    assert_frame_equal(expected_utm_data, obtained_utm_data)
