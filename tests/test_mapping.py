from nerd.mapping import (
    _calculate_cell_density_in_border,
    _calculate_directions,
    _cell_edges_slopes,
    check_directions,
    _density_in_tile,
    _generate_cell_from_coordinates,
    _generate_tile_direction_arrays,
    _orthogonal_slope,
    _reorder_end_tile,
    _safe_divition,
    _sign_of_direction,
    _slope_between_two_points,
    _is_inside_tile,
    generate_contours,
    create_contour_polygon_list,
    export_contour_list_as_shapefile,
    calculate_total_density,
    generate_grid_density,
    density_contours_intervals,
    generate_uniform_density_array,
)
from nerd.density_functions import uniform, normal
from unittest import TestCase
from shapely import geometry

import hashlib
import matplotlib as mpl
import numpy as np
import pandas as pd
import types

random_state = np.random.RandomState(1)


class TestMapping(TestCase):
    def setUp(self) -> None:
        self.stripe_width = 60
        self.b = 2
        self.c = 0
        self.x = [-1, 2, 3, 4, 5, 6]
        self.y = [2, 4, 6, 8, 10, 12]
        self.node = 2
        self.spatial_resolution = 5
        self.uniform_density_value = 10
        self.half_stripe_width = int(self.stripe_width / 2)
        self.density_domain = np.linspace(
            -self.half_stripe_width, self.half_stripe_width, self.spatial_resolution
        )
        self.uniform_density = uniform(self.density_domain, self.stripe_width, 10)
        self.n_contours = 2
        self.x_coordinates = np.linspace(0, 10, 10)
        self.y_coordinates = np.linspace(0, 10, 10)
        self.helicopter_speed = [20, 21, 20, 18, 17, 15, 15, 15, 15, 15, 10, 5]
        self.bucket_logger = np.array([1, 1, 1, 1, 0, 0, 0, 1, 1, 1])
        self.total_density_reshaped = np.eye(10, 10)
        self.aperture_diameter = 90
        self.density_function = normal
        self.flow_rate_function = lambda x: x / 50
        self.total_density_random = random_state.rand(5, 5) * 50
        self.x_grid, self.y_grid = np.meshgrid(self.x_coordinates, self.y_coordinates)
        self.x_tile_coordinates = [
            29.832815729997474,
            -23.832815729997474,
            -22.832815729997474,
            30.832815729997474,
            29.832815729997474,
        ]

        self.y_tile_coordinates = [
            -7.416407864998737,
            19.41640786499874,
            21.41640786499874,
            -5.416407864998737,
            -7.416407864998737,
        ]
        self.flipped_x_tile_coordinates = [
            29.832815729997474,
            -23.832815729997474,
            30.832815729997474,
            -22.832815729997474,
            29.832815729997474,
        ]

        self.flipped_y_tile_coordinates = [
            -7.416407864998737,
            19.41640786499874,
            -5.416407864998737,
            21.41640786499874,
            -7.416407864998737,
        ]
        self.trackmap_data = pd.DataFrame(
            {
                "easting": self.x_coordinates,
                "northing": self.y_coordinates,
                "Logging_on": self.bucket_logger,
                "Speed": self.helicopter_speed[:10],
            }
        )
        self.expected_config_file = "tests/data/expected_nerd_config.json"
        self.config_json = pd.read_json(self.expected_config_file)
        self.input_calibration_data = "tests/data/expected_calibration_data.csv"

    def test_safe_divition(self):
        expected = 60 / 2
        obtained = _safe_divition(self.stripe_width, self.b)
        assert expected == obtained

    def test_safe_divition_by_zero(self):
        expected = np.inf
        obtained = _safe_divition(self.stripe_width, self.c)
        assert expected == obtained

    def test_slope_between_two_points(self):
        expected = 1.0
        obtained = _slope_between_two_points(2, 1, 2, 1)
        assert expected == obtained

    def test_orthogonal_slope(self):
        expected = -1
        obtained = _orthogonal_slope(1)
        assert expected == obtained

    def test_slopes_from_coordinates(self):
        expected = (-0.5, -0.5)
        obtained = _cell_edges_slopes(self.x, self.y, self.node)
        assert expected == obtained

    def test_generate_tile_from_coordinates(self):
        obtained_x_tile, obtained_y_tile = _generate_cell_from_coordinates(
            self.x, self.y, self.node, self.stripe_width
        )
        assert self.x_tile_coordinates == obtained_x_tile
        assert self.y_tile_coordinates == obtained_y_tile

    def test_density_in_tile(self):
        obtained_lambda_density_function = _density_in_tile(
            self.x_tile_coordinates,
            self.y_tile_coordinates,
            self.uniform_density,
            self.spatial_resolution,
        )
        assert isinstance(obtained_lambda_density_function, types.FunctionType)
        obtained_density = obtained_lambda_density_function(1, 8)
        expected_density = np.array(10)
        np.testing.assert_array_almost_equal(expected_density, obtained_density)

    def test_calculate_cell_density_in_border(self):
        xx, yy = _calculate_cell_density_in_border(
            self.x_tile_coordinates, self.y_tile_coordinates, self.spatial_resolution
        )
        expexted_xx_array = np.array(
            [
                29.83281573,
                16.41640786,
                3.0,
                -10.41640786,
                -23.83281573,
                30.83281573,
                17.41640786,
                4.0,
                -9.41640786,
                -22.83281573,
            ]
        )
        expected_yy_array = np.array(
            [
                -7.41640786,
                -0.70820393,
                6.0,
                12.70820393,
                19.41640786,
                -5.41640786,
                1.29179607,
                8.0,
                14.70820393,
                21.41640786,
            ]
        )
        np.testing.assert_array_almost_equal(xx, expexted_xx_array)
        np.testing.assert_array_almost_equal(yy, expected_yy_array)

    def test_calculate_directions(self):
        obtained_angle = _calculate_directions([0, 0, 1, 1, 0], [0, 1, 0, 1, 0])
        second_obtained_angle = _calculate_directions(
            self.x_tile_coordinates, self.y_tile_coordinates
        )
        assert obtained_angle == np.pi
        assert second_obtained_angle == 0

    def test_sign_of_direction(self):
        obtained_angle = _sign_of_direction([1, 0], [1, 0])
        second_obtained_angle = _sign_of_direction([1, 0], [0, 1])
        third_obtained_angle = _sign_of_direction([5, 3], [4, 2])
        assert obtained_angle == 0
        assert second_obtained_angle == np.pi / 2
        self.assertAlmostEqual(
            third_obtained_angle,
            0.07677189126977908,
            16,
            "third_obtained_angle are not almost equal.",
        )

    def test_generate_tile_direction_arrays(self):
        obtained_directions_arrays = _generate_tile_direction_arrays(
            self.x_tile_coordinates, self.y_tile_coordinates
        )
        expected_u_array = np.array([-53.665631, 26.832816])
        expected_v_array = np.array([-53.665631, 26.832816])
        np.testing.assert_array_almost_equal(obtained_directions_arrays[0], expected_u_array)
        np.testing.assert_array_almost_equal(obtained_directions_arrays[1], expected_v_array)

    def test_reorder_end_tile(self):
        obtained_x_tile_coordinates, obtained_y_tile_coordinates = _reorder_end_tile(
            self.x_tile_coordinates, self.y_tile_coordinates
        )
        assert obtained_x_tile_coordinates == self.flipped_x_tile_coordinates
        assert obtained_y_tile_coordinates == self.flipped_y_tile_coordinates

    def test_check_directions(self):
        obtained_x_tile_coordinates, obtained_y_tile_coordinates = check_directions(
            self.flipped_x_tile_coordinates, self.flipped_y_tile_coordinates
        )
        assert obtained_x_tile_coordinates == self.x_tile_coordinates
        assert obtained_y_tile_coordinates == self.y_tile_coordinates

    def test_check_directions_2(self):
        x_tile_test = [0, 1, 0.32020140, 0, 0]
        y_tile_test = [0, 0, 0.93962620, 0, 0]
        obtained_x_tile_coordinates, obtained_y_tile_coordinates = check_directions(
            x_tile_test.copy(), y_tile_test.copy()
        )
        assert obtained_x_tile_coordinates == x_tile_test
        assert obtained_y_tile_coordinates == y_tile_test

    def test_check_directions_3(self):
        x_tile_test = [0, 0, 1, 0, 0]
        y_tile_test = [0, 1, 1, 1, 0]
        obtained_x_tile_coordinates, obtained_y_tile_coordinates = check_directions(
            x_tile_test.copy(), y_tile_test.copy()
        )
        assert obtained_x_tile_coordinates == x_tile_test
        assert obtained_y_tile_coordinates == y_tile_test

    def test_is_inside_tile(self):
        points_to_tests = np.array([np.array([1, 0]), np.array([8, 1])]).T
        obtained_boolean_mask = _is_inside_tile(
            self.x_tile_coordinates, self.y_tile_coordinates, points_to_tests
        )
        assert obtained_boolean_mask[0]
        assert not obtained_boolean_mask[1]

    def test_generate_contours(self):
        expected_density_values = [0.0, 0.4, 0.8]
        contour, contour_dict = generate_contours(
            self.x_grid, self.y_grid, self.total_density_reshaped, self.n_contours
        )
        for key in contour_dict.keys():
            assert isinstance(key, mpl.collections.PathCollection)
        assert list(contour_dict.values()) == expected_density_values
        assert isinstance(contour, mpl.contour.QuadContourSet)

    def test_create_contour_polygon_list(self):
        contour, contour_dict = generate_contours(
            self.x_grid, self.y_grid, self.total_density_reshaped, self.n_contours
        )
        obtained_polygon_list = create_contour_polygon_list(contour, contour_dict)
        expected_poligon_list_element_keys = ["poly", "props"]
        obtained_poligon_list_element_keys = list(obtained_polygon_list[0].keys())
        expected_props_dict_keys = ["z"]
        obtained_props_dict_keys = list(obtained_polygon_list[0]["props"].keys())
        assert isinstance(obtained_polygon_list, list)
        for polygon_dict in obtained_polygon_list:
            assert isinstance(polygon_dict, dict)
            assert isinstance(polygon_dict["poly"], geometry.polygon.Polygon)
            assert isinstance(polygon_dict["props"], dict)
            assert isinstance(polygon_dict["props"]["z"], float)
        assert obtained_poligon_list_element_keys == expected_poligon_list_element_keys
        assert obtained_props_dict_keys == expected_props_dict_keys

    def test_export_contour_list_as_shapefile(self):
        contour, contour_dict = generate_contours(
            self.x_grid, self.y_grid, self.total_density_reshaped, self.n_contours
        )
        obtained_polygon_list = create_contour_polygon_list(contour, contour_dict)
        output_path = "tests/test_shapefile.shp"
        export_contour_list_as_shapefile(obtained_polygon_list, output_path)
        expected_hash = "1124067914ab62d8c5cc0d3cc70742b7"
        assess_hash(output_path, expected_hash)

    def test_calculate_total_density(self):
        spatial_resolution = 2
        x_grid_obtained, y_grid_obtained, total_density_grid_obtained = calculate_total_density(
            self.trackmap_data,
            self.config_json,
            spatial_resolution,
            self.flow_rate_function,
        )
        total_density_expected = np.array(
            [
                [0.0, 0.00488313, 0.00441656, 0.00427116, 0.00417423],
                [0.00488313, 0.00477668, 0.00488313, 0.00515265, 0.0],
                [0.00441656, 0.00488313, 0.00557279, 0.0, 0.0],
                [0.00427116, 0.00515265, 0.0, 0.0, 0.0],
                [0.00417423, 0.0, 0.0, 0.0, 0.00668735],
            ],
        )
        x_grid_expected = np.array(
            [
                [0.0, 2.0, 4.0, 6.0, 8.0],
                [0.0, 2.0, 4.0, 6.0, 8.0],
                [0.0, 2.0, 4.0, 6.0, 8.0],
                [0.0, 2.0, 4.0, 6.0, 8.0],
                [0.0, 2.0, 4.0, 6.0, 8.0],
            ]
        )
        y_grid_expected = np.array(
            [
                [0.0, 0.0, 0.0, 0.0, 0.0],
                [2.0, 2.0, 2.0, 2.0, 2.0],
                [4.0, 4.0, 4.0, 4.0, 4.0],
                [6.0, 6.0, 6.0, 6.0, 6.0],
                [8.0, 8.0, 8.0, 8.0, 8.0],
            ]
        )
        np.testing.assert_array_equal(x_grid_obtained, x_grid_expected)
        np.testing.assert_array_equal(y_grid_obtained, y_grid_expected)
        np.testing.assert_array_almost_equal(total_density_grid_obtained, total_density_expected)
        assert total_density_grid_obtained is not None

    def test_calculate_total_density_2(self):
        spatial_resolution = 2
        x_grid_obtained, y_grid_obtained, total_density_grid_obtained = calculate_total_density(
            self.trackmap_data,
            self.config_json,
            spatial_resolution,
            self.flow_rate_function,
        )
        total_density_expected = np.array(
            [
                [0.0, 0.00488313, 0.00441656, 0.00427116, 0.00417423],
                [0.00488313, 0.00477668, 0.00488313, 0.00515265, 0.0],
                [0.00441656, 0.00488313, 0.00557279, 0.0, 0.0],
                [0.00427116, 0.00515265, 0.0, 0.0, 0.0],
                [0.00417423, 0.0, 0.0, 0.0, 0.00668735],
            ],
        )
        np.testing.assert_array_almost_equal(total_density_grid_obtained, total_density_expected)

    def test_generate_grid_density(self):
        x_grid_obtained, y_grid_obtained = generate_grid_density(
            self.x_coordinates[:10],
            self.y_coordinates[:10],
            self.spatial_resolution,
        )
        x_grid_expected = np.array([[0.0, 5.0], [0.0, 5.0]])
        y_grid_expected = np.array([[0.0, 0.0], [5.0, 5.0]])
        np.testing.assert_array_equal(x_grid_obtained, x_grid_expected)
        np.testing.assert_array_equal(y_grid_obtained, y_grid_expected)

    def test_density_contours_intervals_1(self):
        contours_array_obtained = density_contours_intervals(1, self.total_density_reshaped)
        contours_array_expected = np.array([0.5, 0.95, 1.0, 1.05])
        np.testing.assert_array_equal(contours_array_obtained, contours_array_expected)

    def test_density_contours_intervals_2(self):
        contours_array_obtained = density_contours_intervals(20, self.total_density_random)
        contours_array_expected = np.array([0.388332, 10.0, 19.0, 21.0, 40.0, 47.005374])
        np.testing.assert_array_almost_equal(contours_array_obtained, contours_array_expected)

    def test_generate_uniform_density_array(self):
        uniform_density_obtained, n_obtained = generate_uniform_density_array(
            self.uniform_density_value, self.stripe_width, self.spatial_resolution
        )
        uniform_density_expected = np.array(
            [0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0]
        )
        n_expected = 12
        np.testing.assert_array_equal(uniform_density_obtained, uniform_density_expected)
        assert n_obtained == n_expected


def assess_hash(test_csv_filename, expected_hash):
    md5_hash = hashlib.md5()
    a_file = open(test_csv_filename, "rb")
    content = a_file.read()
    md5_hash.update(content)
    obtained_hash = md5_hash.hexdigest()
    assert expected_hash == obtained_hash
