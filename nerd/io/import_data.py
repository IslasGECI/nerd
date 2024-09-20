from nerd.io.geo2utm import _geo2utm
from nerd.calibration.fit_flow_rate import fit_flow_rate
import nerd.density_functions
import pandas as pd
import os
from typing import Callable

column_names = ["date", "time", "Lat", "Lon", "Speed", "heading", "Logging_on", "altitude"]
flux_calibation_colums = ["aperture_diameter", "flux"]


def _tracmap2csv(tracmap_filename: str, csv_filename: str) -> None:
    tracmap_data = pd.read_csv(
        tracmap_filename, header=None, names=column_names, usecols=[i for i in range(1, 9)]
    )
    tracmap_data.to_csv(csv_filename, index=False)


def _import_tracmap(tracmap_filename: str, csv_filename: str = "input_data.csv") -> pd.DataFrame:
    _tracmap2csv(tracmap_filename, csv_filename)
    return _geo2utm(csv_filename)


def _import_calibration_data(flux_filename: str) -> Callable:
    flux_data = pd.read_csv(
        flux_filename,
        header=None,
        skiprows=1,
        names=flux_calibation_colums,
        usecols=[i for i in range(0, 2)],
    )
    return fit_flow_rate(flux_data["aperture_diameter"].to_numpy(), flux_data["flux"].to_numpy())


def _check_output_directory(output_path: str) -> None:
    if not os.path.exists(output_path):
        os.mkdir(output_path)


def _import_multifile_tracmap(config_file: pd.Series, csv_filename: str) -> pd.DataFrame:
    df_list = _create_df_list(config_file)
    df_concat = pd.concat(df_list)
    output_path = str(config_file.get("output_path"))
    _check_output_directory(output_path)
    concatenated_tracmap_path = "{}/{}".format(output_path, csv_filename)
    df_concat.to_csv(concatenated_tracmap_path, index=False)
    return _geo2utm(concatenated_tracmap_path)


def _create_df_list(config_file: pd.Series) -> list:
    df_list = [
        pd.read_csv(
            resources["input_data_path"],
            header=None,
            names=column_names,
            usecols=[i for i in range(1, 9)],
        )
        for resources in config_file["resources"]
    ]
    return df_list


def _select_parameters_by_index(config_file: pd.Series, n_file: int) -> tuple:
    aperture_diameter = config_file["resources"][n_file]["aperture_diameter"]
    swap_width = config_file["resources"][n_file]["swap_width"]
    density_function = _select_density_function(
        config_file["resources"][n_file]["density_function"]
    )
    return aperture_diameter, swap_width, density_function


def _select_density_function(function_name: str) -> Callable:
    return getattr(nerd.density_functions, function_name)
