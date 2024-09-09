import numpy as np


def get_swath_width(distance: np.ndarray, density: np.ndarray, alpha: float = 0.05) -> float:
    """
    Get swath width (m) from density profile using data points with density greater than zero
    :param distance: Perpendicular distance in meters (m) from flight path
    :param density: Density of bait in kilograms per square meter (kg/m^2)
    :param alpha: Proportion (0<alpha<1) of discarded data points (to avoid outliers)
    :return: Swath width (m)
    """
    distancias_con_cebo = distance[density > 0]
    return np.diff(np.quantile(distancias_con_cebo, [alpha / 2, 1 - alpha / 2]))[0]
