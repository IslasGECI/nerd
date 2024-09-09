import pandas as pd
import utm


def _geo2utm(csv_filename):
    data = pd.read_csv(csv_filename)
    data["easting"], data["northing"], data["zone_number"], data["zone_letter"] = utm.from_latlon(
        data.Lat.values, data.Lon.values
    )
    return data
