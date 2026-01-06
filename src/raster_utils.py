"""Raster utility functions for GeoAssetAI.

Contains DEM loading, hillshade, EDT generation helpers, raster <-> vector helpers.
"""

from typing import Tuple, Optional
import numpy as np
import rasterio
from rasterio.features import rasterize
from scipy import ndimage as ndi
from shapely.geometry import box, mapping
import geopandas as gpd


def load_dem(path: str) -> Tuple[np.ndarray, rasterio.Affine, rasterio.crs.CRS]:
    """Load a single-band DEM and return array, transform and CRS.
    Returns masked array (np.ndarray) with nodata kept as np.nan if necessary.
    """
    with rasterio.open(path) as src:
        arr = src.read(1, masked=False).astype(float)
        transform = src.transform
        crs = src.crs
    # convert rasterio nodata values to np.nan if present
    with rasterio.open(path) as src:
        nd = src.nodatavals[0]
    if nd is not None:
        arr[arr == nd] = np.nan
    return arr, transform, crs


def compute_hillshade(dem: np.ndarray, res_x: float, res_y: float,
                      az_deg: float = 315.0, alt_deg: float = 65.0,
                      exponent: float = 0.8, scale: float = 1.0) -> np.ndarray:
    """Return normalized hillshade in [0,1] based on gradient approach.

    dem: 2D array with np.nan for nodata
    res_x,res_y: pixel size in map units
    exponent: gamma to apply to hillshade for contrast control
    scale: multiplier to overall brightness
    """
    dem_f = dem.copy().astype(float)
    mask = np.isnan(dem_f)
    dem_f[mask] = 0.0
    gx, gy = np.gradient(dem_f, res_x, res_y)
    # remove gradient contribution for nodata
    gx[mask] = 0.0
    gy[mask] = 0.0
    slope = np.pi / 2.0 - np.arctan(np.sqrt(gx * gx + gy * gy))
    aspect = np.arctan2(-gx, gy)
    az = np.deg2rad(az_deg)
    alt = np.deg2rad(alt_deg)
    hill = (np.sin(alt) * np.sin(slope) +
            np.cos(alt) * np.cos(slope) * np.cos(az - aspect))
    # normalize
    mn, mx = np.nanmin(hill), np.nanmax(hill)
    if mx > mn:
        hs = (hill - mn) / (mx - mn)
    else:
        hs = np.zeros_like(hill)
    hs = np.clip((hs ** exponent) * scale, 0, 1)
    # set nodata to a dark value e.g., 0
    hs[mask] = 0.0
    return hs


def edt_from_sea_bool(sea_bool: np.ndarray, pixel_size_m: float) -> np.ndarray:
    """Compute Euclidean Distance Transform (in meters) from boolean sea raster.

    sea_bool: True where sea, False elsewhere
    pixel_size_m: approximate pixel resolution in meters (assumes square pixels)
    """
    inv = ~sea_bool
    # distance_transform_edt returns distance in pixels; multiply by pixel_size
    dist_px = ndi.distance_transform_edt(inv)
    return dist_px * float(pixel_size_m)


def rasterize_geometries(geoms, out_shape: Tuple[int, int], transform, all_touched: bool = False) -> np.ndarray:
    """Rasterize an iterable of shapely geometries (or (geom, value)) to a boolean mask."""
    shapes_iter = ((g, 1) if not isinstance(g, tuple) else g for g in geoms)
    r = rasterize(shapes_iter, out_shape=out_shape, transform=transform, fill=0, all_touched=all_touched, dtype='uint8')
    return r.astype(bool)


def polygon_from_mask(mask: np.ndarray, transform, min_pixels: int = 10):
    """Extract polygons from boolean mask. Returns GeoDataFrame of polygons."""
    from rasterio.features import shapes as rio_shapes
    polys = []
    px_area = abs(transform.a * transform.e)
    for shp, val in rio_shapes(mask.astype('uint8'), transform=transform):
        if val == 1:
            poly = mapping(shp)
            # approximate area filter using transform pixel area not necessary to parse exact area here
            # we return as GeoDataFrame for convenience
            polys.append(shape(shp))
    if not polys:
        return gpd.GeoDataFrame({'geometry': []})
    return gpd.GeoDataFrame({'geometry': polys}, crs=None)

