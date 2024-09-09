from typing import Callable
import inspect
import numpy as np
from nerd.calibration.rmse import _get_rmse_from_function_array
from nerd import density_functions


def _get_density_functions_array() -> list:
    return [
        getattr(density_functions, element)
        for element in dir(density_functions)
        if inspect.isfunction(getattr(density_functions, element))
    ]


def _select_best_density_function_from_array(
    distance: np.ndarray,
    density: np.ndarray,
    aperture_diameter_data: float,
    helicopter_speed_data: float,
    swath_width: float,
    density_functions: list,
    flow_rate_function: Callable,
) -> Callable:
    rmse = _get_rmse_from_function_array(
        distance,
        density,
        aperture_diameter_data,
        helicopter_speed_data,
        swath_width,
        density_functions,
        flow_rate_function,
    )
    is_better_function = rmse == rmse.min()
    return density_functions[np.where(is_better_function)[0][0]]


def get_best_density_function(
    distance: np.ndarray,
    density: np.ndarray,
    aperture_diameter_data: float,
    helicopter_speed_data: float,
    swath_width: float,
    flow_rate_function: Callable,
) -> Callable:
    """
    Select density function with minimum RMSE among the functions defined in
        submodule nerd.density_functions
    :param distance: Perpendicular distance in meters (m) from flight path
    :param density: Density of bait in kilograms per square meter (kg/m^2)
    :param aperture_diameter_data: Diameter (mm) of the dispersion bucket
        aperture
    :param helicopter_speed_data: Speed (m/s) of the helicopter during
        dispersion of bait
    :param swath_width: Width (m) of dispersion swath
    :param flow_rate_function: Function of mass flow rate (kg/s) with respect to
        aperture diameter (mm)
    :return: Function for density (kg/m^2) profile with respect to perpendicular
        distance (m) to flight path, swath width (m), and scale factor
    """
    density_functions = _get_density_functions_array()
    return _select_best_density_function_from_array(
        distance,
        density,
        aperture_diameter_data,
        helicopter_speed_data,
        swath_width,
        density_functions,
        flow_rate_function,
    )
