"""Vector utilities: loading, CRS harmonization, sampling lines, and simple vector operations."""
from typing import Iterable, List, Tuple
import geopandas as gpd
from shapely.geometry import Point, LineString
import math


def load_gdf(path: str, target_crs=None) -> gpd.GeoDataFrame:
    """Load GeoDataFrame and reproject to target_crs if provided."""
    gdf = gpd.read_file(path)
    if target_crs is not None and gdf.crs is not None:
        if gdf.crs.to_string() != target_crs:
            gdf = gdf.to_crs(target_crs)
    return gdf


def sample_line_points(line: LineString, spacing: float) -> List[Point]:
    """Sample points along a LineString at approximately `spacing` meters."""
    pts = []
    if line is None or line.is_empty:
        return pts
    L = line.length
    if L == 0:
        return pts
    n = max(int(math.floor(L / spacing)), 1)
    for i in range(n + 1):
        pts.append(line.interpolate(min(i * spacing, L)))
    return pts


def sample_defenses(def_lines_gdf: gpd.GeoDataFrame, def_polys_gdf: gpd.GeoDataFrame,
                    def_points_gdf: gpd.GeoDataFrame, spacing: float = 500.0) -> gpd.GeoDataFrame:
    """Return a GeoDataFrame of sampled defense points (deduplicated)."""
    sampled = []
    # lines
    for ls in def_lines_gdf.geometry:
        sampled += sample_line_points(ls, spacing)
    # polygon boundaries
    for poly in def_polys_gdf.geometry:
        sampled += sample_line_points(poly.boundary, spacing)
    # include explicit points
    if not def_points_gdf.empty:
        sampled += [pt for pt in def_points_gdf.geometry]
    # deduplicate by rounded coords
    uniq = {}
    for p in sampled:
        key = (round(float(p.x), 3), round(float(p.y), 3))
        uniq[key] = p
    out = gpd.GeoDataFrame({'geometry': list(uniq.values())}, crs=def_lines_gdf.crs if not def_lines_gdf.empty else def_points_gdf.crs)
    return out

