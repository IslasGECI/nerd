from nerd.io import Nerd
from unittest import TestCase
import hashlib
import os
import numpy as np
import pandas as pd


class TestNerd(TestCase):
    def setUp(self) -> None:
        self.expected_config_json_type_option = "series"
        self.expected_config_file: str = "tests/data/expected_nerd_config.json"
        self.config_json = pd.read_json(
            self.expected_config_file, typ=self.expected_config_json_type_option
        )  # type: ignore
        self.input_calibration_data = "tests/data/expected_calibration_data.csv"
        self.expected_results_filename = "outputs/nerd_geojson.json"
        self.imported_concatenated_csv = "outputs/input_concatenated_data.csv"

    def test_full_workflow(self):
        expected_levels = np.array([0.01, 0.019, 0.021, 0.04, 1.576378, 7.295223])
        self.teardown()
        nerd_model = Nerd(self.expected_config_file)
        nerd_model.calculate_total_density()
        obtained_json_type = nerd_model.config_json_type_option
        assert obtained_json_type == self.expected_config_json_type_option
        nerd_model.export_results_geojson(target_density=0.02)
        self.assert_exist_the_file(self.expected_results_filename)
        np.testing.assert_array_almost_equal(
            nerd_model.calculated_levels, expected_levels, decimal=2
        )
        self.assert_exist_the_file(self.imported_concatenated_csv)
        self.teardown()

    def teardown(self):
        self._remove_path(self.expected_results_filename)
        self._remove_path(self.imported_concatenated_csv)
        self._remove_directory("outputs")

    def _remove_directory(self, file):
        if os.path.exists(file):
            os.rmdir(file)

    def _remove_path(self, file):
        if os.path.exists(file):
            os.remove(file)

    def assert_exist_the_file(self, filename):
        assert os.path.isfile(filename)


def assess_hash(test_csv_filename, expected_hash):
    md5_hash = hashlib.md5()
    a_file = open(test_csv_filename, "rb")
    content = a_file.read()
    md5_hash.update(content)
    obtained_hash = md5_hash.hexdigest()
    assert expected_hash == obtained_hash
