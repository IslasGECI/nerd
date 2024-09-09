from nerd.io.import_data import (
    import_calibration_data,
    import_multifile_tracmap,
    check_output_directory,
)
from nerd.mapping.tiling import (
    calculate_total_density,
    density_contours_intervals,
    generate_contours,
)
import geojsoncontour
import json
import pandas as pd


class Nerd:
    """
    NERD generates bait density maps automatically from a probability density function that describes bait density on
    the ground as a function of the bucket aperture diameter and helicopter tracks.

    Attributes:
    -----------
    config_file : str
        Path to the configuration file that contains parameters for density calculation (e.g., aperture diameter,
        swap width).

    Methods:
    -----------
    calculate_total_density()
        Calculate the total density distribution over a grid based on helicopter tracks and flow rates.

    export_results_geojson(target_density)
        Export the calculated density contours as a GeoJSON file.
    """

    def __init__(self, config_file_path):
        """
            Parameters:
        -----------
        config_file_path: str
            Path to the configuration file that contains parameters for density calculation (e.g., aperture diameter,
            swap width).
        """
        self.config_json_type_option = "series"
        self.config_file = pd.read_json(config_file_path, typ=self.config_json_type_option)
        self._tracmap_data = import_multifile_tracmap(
            self.config_file, "input_concatenated_data.csv"
        )
        self._spatial_resolution = self.config_file.get("spatial_resolution")
        self._flow_rate_function = import_calibration_data(
            self.config_file.get("input_calibration_data")
        )

    def calculate_total_density(self) -> None:
        """
        Calculate the total density distribution over a grid based on helicopter tracks and flow rates.

        This function takes in helicopter track data and configuration parameters to compute the density distribution over
        a spatial grid. The process involves selecting parameters for each segment of the tracks, solving the density
        function, and summing up the density values within the corresponding grid cells.
        """
        self._x_grid, self._y_grid, self._total_density = calculate_total_density(
            self._tracmap_data,
            self.config_file,
            self._spatial_resolution,
            self._flow_rate_function,
        )

    def export_results_geojson(self, target_density: float) -> None:
        """
        Export the calculated density contours as a GeoJSON file.

        This method generates contour levels based on a target density, computes the corresponding contours,
        and exports them in GeoJSON format. The GeoJSON file is saved to the output directory specified in the
        configuration file.

        Parameters:
        -----------
        target_density : float
            The density value used to determine the contour levels for the density distribution.

        Returns:
        -----------
        None
         The output GeoJSON file is saved in the directory specified by the `output_path` in the configuration file.

        Notes:
        ------
        - The method also stores the calculated contour levels as an attribute (`calculated_levels`) of the class.
        """
        self.calculated_levels = density_contours_intervals(target_density, self._total_density)
        contours, _ = generate_contours(
            self._x_grid, self._y_grid, self._total_density, self.calculated_levels
        )
        geojson = geojsoncontour.contourf_to_geojson(contourf=contours, unit="m")
        geojson = json.loads(geojson)
        check_output_directory(self.config_file.get("output_path"))
        with open(
            "{}/nerd_geojson.json".format(self.config_file.get("output_path")), "w"
        ) as outfile:
            json.dump(geojson, outfile)
