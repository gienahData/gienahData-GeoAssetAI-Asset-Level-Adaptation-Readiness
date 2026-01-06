from shapely.geometry import LineString, Point
from src.vector_utils import sample_line_points, sample_defenses
import geopandas as gpd

def test_sample_line_points():
    ls = LineString([(0,0),(0,1000)])
    pts = sample_line_points(ls, spacing=200)
    assert len(pts) >= 5

def test_sample_defenses_aggregate():
    line_gdf = gpd.GeoDataFrame({'geometry':[LineString([(0,0),(0,1000)])]}, crs="EPSG:28992")
    poly_gdf = gpd.GeoDataFrame({'geometry':[]}, crs="EPSG:28992")
    pts_gdf = gpd.GeoDataFrame({'geometry':[Point(5,5)]}, crs="EPSG:28992")
    sampled = sample_defenses(line_gdf, poly_gdf, pts_gdf, spacing=250)
    assert not sampled.empty

