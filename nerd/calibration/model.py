from typing import Callable
import numpy as np
from nerd import solver


def model(
    aperture_diameter: np.ndarray,
    helicopter_speed: np.ndarray,
    swath_width: float,
    density_function: Callable,
    flow_rate_function: Callable,
) -> np.ndarray:
    """
    Calculate the density matrix directly below the helicopter (nadir) as a
        function of the aperture diameter and the helicopter speed
    :param aperture_diameter: Diameter (mm) of the dispersion bucket aperture
    :param helicopter_speed: Speed (m/s) of the helicopter during dispersion of
        bait
    :param swath_width: Width (m) of dispersion swath
    :param density_function: Function for density (kg/m^2) profile with respect
        to perpendicular distance (m) to flight path, swath width (m), and scale
        factor
    :param flow_rate_function: Function of mass flow rate (kg/s) with respect to
        aperture diameter (mm)
    :return: Density matrix directly below the helicopter (nadir) as a function
        of aperture_diameter and helicopter_speed
    """
    distance = 0
    assert distance == 0
    densidad = np.zeros([len(helicopter_speed), len(aperture_diameter)])
    for i_diametro, diametro in enumerate(aperture_diameter):
        for i_rapidez, rapidez in enumerate(helicopter_speed):
            get_density = solver(
                diametro, rapidez, swath_width, density_function, flow_rate_function
            )
            densidad[i_rapidez][i_diametro] = get_density(distance)
    return np.array(densidad)
