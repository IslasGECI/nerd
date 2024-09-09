import numpy as np


def uniform(distance: np.ndarray, width: float, parameter: float) -> np.floating:
    """
    Uniform distribution for density profiles
    :param distance: Distance from flight path
    :param width: Swath width
    :param parameter: Free parameter to be fitted
    :return:
    """
    is_inside = np.abs(distance) < width / 2
    return np.double(is_inside) * parameter


def triangular(distance: float, width: float, parameter: float) -> float:
    """
    Triangular distribution for density profiles
    :param distance: Distance from flight path
    :param width: Swath width
    :param parameter: Free parameter to be fitted
    :return:
    """
    slope = -2 * parameter / width
    is_inside = np.abs(distance) < width / 2  # pragma: no mutate
    return (slope * np.abs(distance) + parameter) * np.double(is_inside)


def normal(distance: float, width: float, parameter: float) -> float:
    """
    Normal distribution for density profiles
    :param distance: Distance from flight path
    :param width: Swath width
    :param parameter: Free parameter to be fitted
    :return:
    """
    standard_deviation = width / 4
    return (
        parameter
        / np.sqrt(2 * np.pi * standard_deviation**2)
        * np.exp(-(distance**2) / (2 * standard_deviation**2))
    )
