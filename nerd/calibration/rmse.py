import numpy as np
from nerd import solver


def get_rmse_from_function_array(
    distance,
    density,
    aperture_diameter,
    helicopter_speed,
    swath_width,
    density_functions_array,
    flow_rate_function,
):
    rmse = []
    for funcion_densidad in density_functions_array:
        rmse_auxiliar = get_rmse(
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


def get_rmse(
    distance,
    density,
    aperture_diameter,
    helicopter_speed,
    swath_width,
    density_function,
    flow_rate_function,
):
    density_profile_function = solver(
        aperture_diameter, helicopter_speed, swath_width, density_function, flow_rate_function
    )
    estimated_density = density_profile_function(distance)
    rmse = np.sqrt(np.mean((estimated_density - density) ** 2))
    return rmse
