import numpy as np
from src.raster_utils import compute_hillshade, edt_from_sea_bool

def test_hillshade_constant():
    dem = np.zeros((10,10))
    hs = compute_hillshade(dem, 1.0, 1.0)
    assert hs.shape == dem.shape

def test_edt_simple():
    sea = np.zeros((5,5), dtype=bool)
    sea[2,:] = True
    edt = edt_from_sea_bool(sea, pixel_size_m=10.0)
    assert edt.shape == sea.shape
    assert np.all(edt[2,:] == 0.0)

