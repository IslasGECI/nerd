import os
import pandas as pd
from nerd.density_functions.density_functions import normal
from nerd.io import _import_tracmap, _tracmap2csv, _import_calibration_data, select_density_function
from pandas._testing import assert_frame_equal
import numpy as np
from numpy.testing import assert_array_almost_equal
from nerd.density_functions import uniform
from nerd.io.geo2utm import _geo2utm
from nerd.io.import_data import (
    _check_output_directory,
    _import_multifile_tracmap,
    create_df_list,
    select_parameters_by_index,
)


def test_tracmap2csv():
    expected_csv = pd.read_csv("tests/data/expected_input_data.csv")
    _tracmap2csv(
        tracmap_filename="tests/data/tracmap_sample_data.txt",
        csv_filename="tests/data/imported_data.csv",
    )
    obtained_csv = pd.read_csv("tests/data/imported_data.csv")
    assert_frame_equal(expected_csv, obtained_csv)


def test_import_tracmap_without_csvfilename():
    expected_utm_data = pd.read_csv("tests/data/expected_utm_data.csv")
    obtained_utm_data = _import_tracmap(tracmap_filename="tests/data/tracmap_sample_data.txt")
    assert_frame_equal(expected_utm_data, obtained_utm_data)
    os.remove("input_data.csv")


def test_import_tracmap_with_csvfilename():
    test_csv_filename = "test_csv_filename.csv"
    expected_utm_data = pd.read_csv("tests/data/expected_utm_data.csv")
    obtained_utm_data = _import_tracmap(
        tracmap_filename="tests/data/tracmap_sample_data.txt", csv_filename=test_csv_filename
    )
    assert os.path.isfile(test_csv_filename)
    assert_frame_equal(expected_utm_data, obtained_utm_data)
    os.remove(test_csv_filename)


def test_import_calibration_data():
    expected_utm_data = "tests/data/expected_calibration_data.csv"
    obtained_utm_data = _import_calibration_data(expected_utm_data)
    assert_array_almost_equal(
        obtained_utm_data, np.array([6.86905404e-04, -6.19897620e-02, 1.72530268e00])
    )


def test_select_density_function():
    expected_function = uniform
    obtained_function = select_density_function("uniform")
    assert expected_function == obtained_function


def test_check_output_directory():
    output_path = "./example_dir"
    _check_output_directory(output_path)
    directory_exists = os.path.exists(output_path)
    assert directory_exists is True


def test_import_multifile_tracmap():
    config_file_path = "tests/data/expected_nerd_config.json"
    config_file = pd.read_json(config_file_path, typ="series")
    tracmap_data = _import_multifile_tracmap(config_file, "input_concatenated_data.csv")
    assert os.path.isfile(config_file_path)
    assert isinstance(tracmap_data, pd.DataFrame)
    assert_frame_equal(tracmap_data, _geo2utm("tests/data/expected_concatenated_data.csv"))


def test_create_df_list():
    config_file_path = "tests/data/expected_nerd_config.json"
    config_file = pd.read_json(config_file_path, typ="series")
    obtained_df_list = create_df_list(config_file)
    assert isinstance(obtained_df_list, list)
    for obtained_df in obtained_df_list:
        assert isinstance(obtained_df, pd.DataFrame)


def test_select_parameters_by_index():
    config_file_path = "tests/data/expected_nerd_config.json"
    config_file = pd.read_json(config_file_path, typ="series")
    expected_aperture_diameter = 95
    expected_swap_width = 70
    expected_density_function = normal
    (
        obtained_aperture_diameter,
        obtained_swap_width,
        obtained_density_function,
    ) = select_parameters_by_index(config_file, 1)
    assert expected_aperture_diameter == obtained_aperture_diameter
    assert expected_density_function == obtained_density_function
    assert expected_swap_width == obtained_swap_width
