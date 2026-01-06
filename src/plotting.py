"""Plotting helpers for the dark-theme map. Returns Matplotlib figures so tests can inspect objects."""
from typing import Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from matplotlib.lines import Line2D


def build_dark_map(shaded_dem_plot: np.ndarray, extent: Tuple[float, float, float, float],
                   assets_gdf: gpd.GeoDataFrame, sea_gdf: Optional[gpd.GeoDataFrame] = None,
                   lakes_gdf: Optional[gpd.GeoDataFrame] = None, hydro_lines: Optional[gpd.GeoDataFrame] = None,
                   defs_polys: Optional[gpd.GeoDataFrame] = None, defs_pts: Optional[gpd.GeoDataFrame] = None,
                   category_colors: dict = None, visible_categories=None,
                   bg_color: str = '#141414'):
    """Return fig,ax with the dark map plotted.

    extent = (left,right,bottom,top)
    shaded_dem_plot: h x w x 3 RGB array in [0,1] or uint8
    """
    if category_colors is None:
        category_colors = {}
    if visible_categories is None:
        visible_categories = []
    left, right, bottom, top = extent
    fig, ax = plt.subplots(figsize=(14, 12), facecolor=bg_color)
    ax.set_facecolor(bg_color)
    ax.imshow(shaded_dem_plot, origin='lower', extent=(left, right, bottom, top), interpolation='nearest', zorder=0)
    if sea_gdf is not None and not sea_gdf.empty:
        sea_gdf.plot(ax=ax, facecolor=(18/255,33/255,64/255,1.0), edgecolor=(1,1,1,0.04), linewidth=0.08, zorder=3)
    if lakes_gdf is not None and not lakes_gdf.empty:
        lakes_gdf.plot(ax=ax, facecolor=(70/255,120/255,160/255,0.92), edgecolor=(1,1,1,0.04), linewidth=0.08, zorder=4)
    if hydro_lines is not None and not hydro_lines.empty:
        hydro_lines.plot(ax=ax, linewidth=0.1, edgecolor=(0.45,0.65,0.86,0.95), zorder=5)
    if defs_polys is not None and not defs_polys.empty:
        defs_polys.plot(ax=ax, facecolor=(0.78,0.52,0.36,0.32), edgecolor=(0.50,0.28,0.18,0.98), linewidth=0.6, zorder=6)
    if defs_pts is not None and not defs_pts.empty:
        defs_pts.plot(ax=ax, markersize=10, color=(0.50,0.28,0.18,0.98), zorder=7)
    # assets
    for cat in visible_categories:
        grp = assets_gdf[assets_gdf['defense_category'] == cat]
        if grp.empty:
            continue
        col = category_colors.get(cat, '#9d9d9d')
        grp.plot(ax=ax, markersize=grp.get('plot_size', 36), color=col, edgecolor='white', linewidth=0.22, alpha=0.95, zorder=8)
    # legend
    legend_handles = []
    for cat in visible_categories:
        legend_handles.append(Line2D([0], [0], marker='o', color='w', label=cat,
                                     markerfacecolor=category_colors.get(cat, '#999999'), markersize=8))
    if hydro_lines is not None and not hydro_lines.empty:
        legend_handles.append(Line2D([0], [0], color=(0.45,0.65,0.86,0.95), lw=2, label='Rivers'))
    if defs_pts is not None and not defs_pts.empty:
        legend_handles.append(Line2D([0], [0], marker='s', color='w', label='Flood defenses', markerfacecolor=(0.78,0.52,0.36,0.32), markersize=8))
    leg = ax.legend(handles=legend_handles, loc='upper left', fontsize=12, facecolor="#1a1a1a", framealpha=0.7)
    for txt in leg.get_texts():
        txt.set_color('white')
    ax.set_xlim(left, right); ax.set_ylim(bottom, top); ax.set_axis_off()
    plt.tight_layout()
    return fig, ax

