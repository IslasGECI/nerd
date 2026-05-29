from typing import Callable
from scipy.integrate import quad
from scipy.optimize import fsolve
import numpy as np


def solver(
    aperture_diameter: float,
    helicopter_speed: float,
    swath_width: float,
    density_function: Callable,
    flow_rate_function: Callable,
) -> Callable:
    """
    Fit model for bait density as a function of perpendicular distance in meters
        (m) from flight path
    :param aperture_diameter: Diameter (mm) of the dispersion bucket aperture
    :param helicopter_speed: Speed (m/s) of the helicopter during dispersion of
        bait
    :param swath_width: Width (m) of dispersion swath
    :param density_function: Function for density (kg/m^2) profile with respect
        to perpendicular distance (m) to flight path, swath width (m), and scale
        factor
    :param flow_rate_function: Function of mass flow rate (kg/s) with respect to
        aperture diameter (mm)
    :return: Function for bait density (kg/m^2) profile with respect to
        perpendicular distance (m) from flight path
    """

    def mass_conservation(parametro_libre):
        def sigma(distance):
            return density_function(distance, swath_width, parametro_libre)[0]

        integrations_limits = swath_width / 2
        integral = quad(sigma, -integrations_limits, integrations_limits)[0]
        return integral - flow_rate_function(aperture_diameter) / helicopter_speed

    starting_root = np.random.rand()
    parametro_ajustado = fsolve(mass_conservation, starting_root)[0]
    return lambda x: density_function(x, swath_width, parametro_ajustado)
