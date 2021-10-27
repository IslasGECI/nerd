from matplotlib import path
from nerd import solver
from nerd.density_functions import uniform
from scipy.interpolate import griddata
from shapely import geometry
from tqdm import tqdm

import fiona
import matplotlib.pyplot as plt
import numpy as np


def slope_between_two_points(y2, y1, x2, x1):
    return safe_divition(y2 - y1, x2 - x1)


def orthogonal_slope(slope):
    return safe_divition(-1, slope)


def safe_divition(numerator, denominator):
    if denominator == 0:
        return np.inf
    return numerator / denominator


def cell_edges_slopes(x, y, node_index):
    start_slope = orthogonal_slope(
        slope_between_two_points(
            y[node_index + 1], y[node_index - 1], x[node_index + 1], x[node_index - 1]
        )
    )
    end_slope = orthogonal_slope(
        slope_between_two_points(y[node_index + 2], y[node_index], x[node_index + 2], x[node_index])
    )
    return start_slope, end_slope


def calculate_cell_y_limits(slope, limit_x, x_coord, y_coord):
    return slope * (limit_x - x_coord) + y_coord


def cell_y_coordinates(start_orthogonal_slope, end_orthogonal_slope, x_rect, x, y, node):
    start_y1 = calculate_cell_y_limits(start_orthogonal_slope, x_rect[0], x[node], y[node])
    start_y2 = calculate_cell_y_limits(start_orthogonal_slope, x_rect[1], x[node], y[node])
    end_y2 = calculate_cell_y_limits(end_orthogonal_slope, x_rect[2], x[node + 1], y[node + 1])
    end_y1 = calculate_cell_y_limits(end_orthogonal_slope, x_rect[3], x[node + 1], y[node + 1])
    return [start_y1, start_y2, end_y2, end_y1, start_y1]


def calculate_cell_x_limits(r, orthogonal_slope, x_coord):
    return r / np.sqrt(1 + orthogonal_slope ** 2) + x_coord


def cell_x_coordinates(r, start_orthogonal_slope, end_orthogonal_slope, x, node):
    start_x1 = calculate_cell_x_limits(r, start_orthogonal_slope, x[node])
    start_x2 = calculate_cell_x_limits(-r, start_orthogonal_slope, x[node])
    end_x1 = calculate_cell_x_limits(r, end_orthogonal_slope, x[node + 1])
    end_x2 = calculate_cell_x_limits(-r, end_orthogonal_slope, x[node + 1])
    return [start_x1, start_x2, end_x2, end_x1, start_x1]


def generate_cell_from_coordinates(x, y, node, stripe_width, spatial_resolution):
    r = stripe_width / 2
    start_orthogonal_slope, end_orthogonal_slope = cell_edges_slopes(x, y, node)
    x_rect = cell_x_coordinates(r, start_orthogonal_slope, end_orthogonal_slope, x, node)
    y_rect = cell_y_coordinates(start_orthogonal_slope, end_orthogonal_slope, x_rect, x, y, node)
    x_rect, y_rect = check_directions(x_rect, y_rect)
    return x_rect, y_rect


def calculate_cell_density_in_border(x_rect, y_rect, n_point):
    startX = np.linspace(x_rect[0], x_rect[1], n_point)
    startY = np.linspace(y_rect[0], y_rect[1], n_point)
    endX = np.linspace(x_rect[3], x_rect[2], n_point)
    endY = np.linspace(y_rect[3], y_rect[2], n_point)
    xx = np.append(startX, endX)
    yy = np.append(startY, endY)
    return xx, yy


def density_in_tile(x_rect, y_rect, density_profile, n_point):
    xx, yy = calculate_cell_density_in_border(x_rect, y_rect, n_point)
    mean_xx = np.mean(xx)
    mean_yy = np.mean(yy)
    return lambda xq, yq: griddata(
        np.array([xx - mean_xx, yy - mean_yy]).T,
        np.tile(density_profile, 2),
        (xq - mean_xx, yq - mean_yy),
    )


def is_inside_tile(x_rect, y_rect, points):
    polygon_tile = [[x_rect[i], y_rect[i]] for i in range(len(x_rect))]
    poly = path.Path(polygon_tile)
    return poly.contains_points(points)


def calculate_directions(x_rect, y_rect):
    u, v = generate_tile_direction_arrays(x_rect, y_rect)
    theta1 = sign_of_direction(u, v)
    return theta1


def generate_tile_direction_arrays(x_rect, y_rect):
    u = np.array([x_rect[1] - x_rect[0], y_rect[1] - y_rect[0]])
    v = np.array([x_rect[2] - x_rect[3], y_rect[2] - y_rect[3]])
    return u, v


def sign_of_direction(u, v):
    inner = np.inner(u, v)
    norms = np.linalg.norm(u) * np.linalg.norm(v)
    return np.arccos(np.clip(inner / norms, -1.0, 1.0))


def reorder_end_tile(x_rect, y_rect):
    tempx1 = x_rect[3]
    x_rect[3] = x_rect[2]
    x_rect[2] = tempx1
    tempy1 = y_rect[3]
    y_rect[3] = y_rect[2]
    y_rect[2] = tempy1
    return x_rect, y_rect


def check_directions(x_rect, y_rect):
    startangle = calculate_directions(x_rect, y_rect)
    if startangle > np.pi / 2:
        x_rect, y_rect = reorder_end_tile(x_rect, y_rect)
    return x_rect, y_rect


def generate_contours(x_grid, y_grid, total_density, *args):
    contour = plt.contourf(x_grid, y_grid, total_density, *args)
    return contour, dict(zip(contour.collections, contour.levels))


def create_contour_polygon_list(contour, contour_dict):
    # Original code in https://github.com/chrishavlin/learning_shapefiles/blob/master/src/contourf_to_shp.py
    PolyList = []
    for col in contour.collections:
        z = contour_dict[col]
        for contour_path in col.get_paths():
            for ncp, cp in enumerate(contour_path.to_polygons()):
                lons = cp[:, 0]
                lats = cp[:, 1]
                new_shape = geometry.Polygon([(i[0], i[1]) for i in zip(lons, lats)])
                if ncp == 0:
                    poly = new_shape
                else:
                    poly = poly.difference(new_shape)

                PolyList.append({"poly": poly, "props": {"z": z}})
    return PolyList


def export_contour_list_as_shapefile(PolyList, output_path):
    schema = {"geometry": "Polygon", "properties": {"z": "float"}}
    with fiona.collection(output_path, "w", "ESRI Shapefile", schema) as output:
        for poly_list in PolyList:
            output.write(
                {"properties": poly_list["props"], "geometry": geometry.mapping(poly_list["poly"])}
            )


def generate_grid_density(x_coordinates, y_coordinates, spatial_resolution):
    x = np.arange(min(x_coordinates), max(x_coordinates), spatial_resolution)
    y = np.arange(min(y_coordinates), max(y_coordinates), spatial_resolution)
    x_grid, y_grid = np.meshgrid(x, y)
    return x_grid, y_grid

class Tracks():
    def __init__(self, track_data):
        self.track_data = track_data

    @property
    def x_coordinates(self):
        return self.track_data["easting"].to_numpy()
    @property
    def y_coordinates(self):
        return self.track_data["northing"].to_numpy()
    @property
    def bucket_logger(self):
        return self.track_data["Logging_on"].to_numpy()
    @property
    def helicopter_speed(self):
        return self.track_data["Speed"].to_numpy()
    @property
    def n_data(self):
        return len(self.track_data)



def calculate_total_density(
    track_data,
    stripe_width,
    spatial_resolution,
    aperture_diameter,
    density_function,
    flow_rate_function,
):
    tracks = Tracks(track_data)
    x_grid, y_grid = generate_grid_density(tracks.x_coordinates, tracks.y_coordinates, spatial_resolution)
    x_grid_ravel = np.ravel(x_grid)
    y_grid_ravel = np.ravel(y_grid)
    total_density = np.zeros_like(x_grid_ravel)
    n = int(np.floor(stripe_width / spatial_resolution))
    array_for_density = np.linspace(-stripe_width / 2, stripe_width / 2, n)

    for i in tqdm(range(tracks.n_data - 2)):
        if tracks.bucket_logger[i] == 0:
            continue
        else:
            density_function_lambda = solver(
                aperture_diameter,
                tracks.helicopter_speed[i],
                stripe_width,
                density_function,
                flow_rate_function,
            )
            density_array = density_function_lambda(array_for_density)
            x_rect, y_rect = generate_cell_from_coordinates(
                tracks.x_coordinates, tracks.y_coordinates, i, stripe_width, spatial_resolution
            )
            inside_mask = is_inside_tile(x_rect, y_rect, np.array([x_grid_ravel, y_grid_ravel]).T)
            sub_grid_x = x_grid_ravel[inside_mask]
            sub_grid_y = y_grid_ravel[inside_mask]
            cell_density = density_in_tile(x_rect, y_rect, density_array, n)(sub_grid_x, sub_grid_y)
            total_density[inside_mask] = total_density[inside_mask] + cell_density
    total_density_grid = np.reshape(total_density, x_grid.shape)
    return x_grid, y_grid, total_density_grid


def generate_uniform_density_array(density_value, stripe_width, spatial_resolution):
    r = int(stripe_width / 2)
    n = int(np.floor(stripe_width / spatial_resolution))
    rr = np.linspace(-r, r, n)
    normal_density_array = uniform(rr, stripe_width, density_value)
    return normal_density_array, n


def density_contours_intervals(density_value, total_density):
    mask_zeros = total_density != 0
    total_density_masked = total_density[mask_zeros]
    return np.unique(
        [
            total_density_masked.min() / 2,
            density_value / 2,
            density_value * 0.95,
            density_value * 1.05,
            np.min([2 * density_value, np.max(total_density)]),
            np.max(total_density),
        ]
    )
