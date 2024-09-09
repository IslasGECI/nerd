from typing import Callable
import numpy as np


def fit_flow_rate(aperture_diameters: np.ndarray, flow_rates: np.ndarray) -> Callable:
    """
    Fit quadratic model for flow rate (kg/s) as a function of aperture diameter (mm)
    :param aperture_diameters: Array of diameters of the bucket aperture in
        millimetres (mm)
    :param flow_rates: Array of mass flow rate of bait in kg per second (kg/s)
    :return: Function of mass flow rate with respect to aperture diameter
    """
    coeficients = np.polyfit(aperture_diameters, flow_rates, 2)
    return np.poly1d(coeficients)
