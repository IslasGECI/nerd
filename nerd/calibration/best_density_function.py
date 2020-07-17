from typing import Callable
import inspect
import numpy as np
from . import get_rmse_from_function_array
from .. import density_functions as df


def get_density_functions_array():
    return [
        getattr(df, elemento) for elemento in dir(df) if inspect.isfunction(getattr(df, elemento))
    ]


def select_best_density_function_from_array(
    distance,
    density,
    aperture_diameter_data,
    helicopter_speed_data,
    swath_width,
    density_functions,
    flow_rate_function,
):
    rmse = get_rmse_from_function_array(
        distance,
        density,
        aperture_diameter_data,
        helicopter_speed_data,
        swath_width,
        density_functions,
        flow_rate_function,
    )
    es_mejor_funcion = rmse == rmse.min()
    return density_functions[np.where(es_mejor_funcion)[0][0]]


def get_best_density_function(
    distance: np.array,
    density: np.array,
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
    density_functions = get_density_functions_array()
    return select_best_density_function_from_array(
        distance,
        density,
        aperture_diameter_data,
        helicopter_speed_data,
        swath_width,
        density_functions,
        flow_rate_function,
    )
