# GeoAssetAI — Asset-Level Structural Protection Proxy

<p align="center">
  <img src="figure/final_map_rescored_fast_dark_filtered_highres.png" width="900">
</p>

<p align="center">
  <em>Asset-level adaptation score across the Netherlands, combining flood-defense proximity, local defense density, and coastal exposure.</em>
</p>

<p align="center">
  <img src="figure/final_map_rescored_fast_zoom_rotterdam_antwerpen_extended.PNG" width="900">
</p>

<p align="center">
  <em>Zoomed view of the Rotterdam–Antwerpen corridor highlighting defended, partially defended, and non-defended assets.</em>
</p>


# gienahData-GeoAssetAI-Asset-Level-Adaptation-Readiness

# GeoAssetAI — Asset-Level Adaptation Readiness

This repository contains a reproducible, geospatial AI pipeline for computing an
asset-level **adaptation / structural protection proxy** using elevation data,
hydrology, and flood defense infrastructure.

The project is designed to support climate and physical-risk analytics by
transforming heterogeneous geospatial inputs into **model-ready, auditable
asset-level metrics**.

## Repository structure
notebooks/
01_data_prep.ipynb
02_sea_land_masks.ipynb
03_defense_sampling.ipynb
04_scoring_and_mapping.ipynb
05_report_and_exports.ipynb


## How to run

1. Install dependencies:
pip install -r requirements.txt

2. Place required input data in a local `data/` folder (not tracked in Git):
- `merged_dem_rd_crop.tif` (EPSG:28992)
- Natural Earth land mask (raster or vector)
- Geofabrik water polygons & waterways
- Flood defense geometries
- Asset point dataset

3. Run notebooks in order:
   `01_data_prep.ipynb`
   `02_sea_land_masks.ipynb`
   `03_defense_sampling.ipynb`
   `04_scoring_and_mapping.ipynb`
   `05_report_and_exports.ipynb`

## Outputs

- Asset-level scores and categories (`assets_scored_rescored_fast.geojson`)
- Summary CSV by defense category
- High-quality dark-theme maps (national + Rotterdam–Antwerpen zoom)

## Notes

Large data files are intentionally excluded from version control.
The notebooks are deterministic and reproducible given the same inputs.

Commit change
