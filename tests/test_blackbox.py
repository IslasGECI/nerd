import numpy as np
import pandas as pd
import pytest

import nerd
import nerd.density_functions


@pytest.fixture()
def density_profile():
    return pd.read_csv("tests/data/profile.csv")


@pytest.fixture()
def distance(density_profile):
    return density_profile.distance.values


@pytest.fixture()
def density(density_profile):
    density_kg_per_ha = density_profile.density.values
    return density_kg_per_ha / 1e4  # Convert densities to kg per square metter


@pytest.fixture()
def flow_data():
    flow_data = pd.read_csv("tests/data/flow.csv")
    return flow_data[flow_data.bait_status == "new"][["aperture", "flow"]]


@pytest.fixture()
def aperture_diameters(flow_data):
    return flow_data.aperture.values


@pytest.fixture()
def flow_rates(flow_data):
    return flow_data.flow.values


@pytest.fixture()
def swath_width():
    return 60


@pytest.fixture()
def flow_rate_function():
    return np.poly1d([0.0007, -0.06, 1.7])


@pytest.fixture()
def aperture_diameter():
    return 75


@pytest.fixture()
def helicopter_speed():
    return 25


@pytest.fixture()
def funcion_densidad():
    return nerd.density_functions.uniform


def test_fit_flow_rate(aperture_diameters, flow_rates):
    length = 3
    flow_rate_function = nerd.calibration.fit_flow_rate(aperture_diameters, flow_rates)

    x = np.linspace(min(aperture_diameters), max(aperture_diameters), length)
    expected_flow_rate = np.array([0.39375461, 0.93991342, 2.03559656])
    obtained_flow_rate = flow_rate_function(x)
    np.testing.assert_allclose(obtained_flow_rate, expected_flow_rate)


def test_swath_width(distance, density):
    expected_swath_width = 64.64625
    obtained_swath_width = nerd.calibration.get_swath_width(distance, density)
    np.testing.assert_allclose(obtained_swath_width, expected_swath_width)


def test_select_best_density_function(distance, density, swath_width, flow_rate_function):
    length = 3
    aperture_diameter_data = 55  # Milimetres
    helicopter_speed_data = 20.5778  # Meters per second (40 knots)

    density_function = nerd.calibration.get_best_density_function(
        distance,
        density,
        aperture_diameter_data,
        helicopter_speed_data,
        swath_width,
        flow_rate_function,
    )
    estimated_profile = nerd.solver(
        aperture_diameter_data,
        helicopter_speed_data,
        swath_width,
        density_function,
        flow_rate_function,
    )

    x = np.linspace(min(distance), max(distance), length)
    estimated_density = estimated_profile(x)
    expected_density = np.array([0, 0.00041914, 0])
    np.testing.assert_allclose(estimated_density, expected_density, rtol=1e-5)


def test_calibration_model(aperture_diameters, swath_width, flow_rate_function):
    length = 3
    aperture_diameters_domain = np.linspace(
        min(aperture_diameters), max(aperture_diameters), length
    )
    helicopter_speeds_domain = np.linspace(10, 40, length)
    density_matrix = nerd.calibration.model(
        aperture_diameters_domain,
        helicopter_speeds_domain,
        swath_width,
        nerd.density_functions.uniform,
        flow_rate_function,
    )
    matrix_expected = np.array(
        [
            [0.0008625, 0.00189583, 0.0038625],
            [0.000345, 0.00075833, 0.001545],
            [0.00021563, 0.00047396, 0.00096563],
        ]
    )
    np.testing.assert_allclose(density_matrix, matrix_expected, rtol=1e-4)


def test_get_rmse(
    aperture_diameter, helicopter_speed, swath_width, funcion_densidad, flow_rate_function
):
    distance = 10
    density = 3
    rmse_expected = 2.999241666666667
    rmse_obtained = nerd.calibration.get_rmse(
        distance,
        density,
        aperture_diameter,
        helicopter_speed,
        swath_width,
        funcion_densidad,
        flow_rate_function,
    )
    print(rmse_obtained)
    np.testing.assert_almost_equal(rmse_obtained, rmse_expected)


def test_solver(aperture_diameter, helicopter_speed, swath_width, flow_rate_function):
    funcion_densidad = nerd.density_functions.normal
    fitted_function = nerd.solver(
        aperture_diameter, helicopter_speed, swath_width, funcion_densidad, flow_rate_function
    )
    distance = 0
    evaluated_function_expected = 0.0012678106357132415
    evaluated_function_obtained = fitted_function(distance)
    np.testing.assert_almost_equal(evaluated_function_obtained, evaluated_function_expected)
