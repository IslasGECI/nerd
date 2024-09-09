from typing import Callable
import numpy as np
from nerd import solver


def _get_rmse_from_function_array(
    distance: np.ndarray,
    density: np.ndarray,
    aperture_diameter: float,
    helicopter_speed: float,
    swath_width: float,
    density_functions_array: list,
    flow_rate_function: Callable,
) -> np.ndarray:
    rmse = []
    for funcion_densidad in density_functions_array:
        rmse_auxiliar = _get_rmse(
            distance,
            density,
            aperture_diameter,
            helicopter_speed,
            swath_width,
            funcion_densidad,
            flow_rate_function,
        )
        rmse.append(rmse_auxiliar)
    return np.array(rmse)


def _get_rmse(
    distance: np.ndarray,
    density: np.ndarray,
    aperture_diameter: float,
    helicopter_speed: float,
    swath_width: float,
    density_function: Callable,
    flow_rate_function: Callable,
) -> float:
    density_profile_function = solver(
        aperture_diameter, helicopter_speed, swath_width, density_function, flow_rate_function
    )
    estimated_density = density_profile_function(distance)
    rmse = np.sqrt(np.mean((estimated_density - density) ** 2))
    return rmse
