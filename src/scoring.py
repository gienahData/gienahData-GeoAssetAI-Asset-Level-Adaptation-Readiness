"""Scoring functions for assets.
- compute_defense_scores: distance/density -> score_def & score_density
- categorize_assets: apply thresholds to assign defense_category
- compute_plot_size: map score to marker size
"""

from typing import Tuple
import numpy as np
import geopandas as gpd


def compute_defense_scores(dist_to_def_m: np.ndarray, def_count_local: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compute score_def and score_density arrays given distances and counts.

    score_def = 1 / (1 + (dist_to_def / 1000)^1.5)
    score_density = clip(def_count_local / 5, 0, 1)
    """
    d = np.array(dist_to_def_m, dtype=float)
    cnt = np.array(def_count_local, dtype=float)
    score_def = 1.0 / (1.0 + (d / 1000.0) ** 1.5)
    score_density = np.minimum(cnt / 5.0, 1.0)
    return score_def, score_density


def main_score(score_def: np.ndarray, score_density: np.ndarray, w_def: float = 0.6, w_density: float = 0.4) -> np.ndarray:
    """Combine components to produce main_score in [0,1]."""
    s = (w_def * score_def + w_density * score_density).clip(0, 1)
    return s


def categorize_assets(gdf: gpd.GeoDataFrame, coast_threshold_m: float = 5000.0) -> gpd.GeoDataFrame:
    """Apply final categories to assets GeoDataFrame.

    Rules:
      - if dist_to_coast_m > coast_threshold => 'Mainland, not exposed'
      - elif dist_to_def_m <= 1000 and def_count_local >= 5 => 'Defended'
      - elif dist_to_def_m <= 1000 => 'Partially defended (close-low-density)'
      - else => 'Not defended'
    """
    def cat(row):
        if float(row.get('dist_to_coast_m', 0.0)) > float(coast_threshold_m):
            return 'Mainland, not exposed'
        if float(row.get('dist_to_def_m', 1e9)) <= 1000.0 and float(row.get('def_count_local', 0.0)) >= 5.0:
            return 'Defended'
        if float(row.get('dist_to_def_m', 1e9)) <= 1000.0:
            return 'Partially defended (close-low-density)'
        return 'Not defended'
    gdf = gdf.copy()
    gdf['defense_category'] = gdf.apply(cat, axis=1)
    return gdf


def compute_plot_size(scores: np.ndarray, min_size=18, max_size=220, gamma=0.7) -> np.ndarray:
    """Map scores in [0,1] to marker sizes for plotting.

    Non-linear mapping: (normalized^gamma) * (max-min) + min
    """
    arr = np.array(scores, dtype=float)
    if arr.max() == arr.min():
        norm = np.zeros_like(arr)
    else:
        norm = (arr - arr.min()) / (arr.max() - arr.min())
    sizes = np.clip((norm ** gamma) * (max_size - min_size) + min_size, min_size, max_size)
    return sizes

