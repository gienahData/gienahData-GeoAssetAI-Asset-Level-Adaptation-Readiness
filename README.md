# GeoAssetAI — Asset-Level Adaptation Readiness

This repository contains a reproducible, geospatial AI pipeline for computing an
asset-level **adaptation / structural protection proxy** using elevation data,
hydrology, and flood defense infrastructure.

The project is designed to support climate and physical-risk analytics by
transforming heterogeneous geospatial inputs into **model-ready, auditable
asset-level metrics**.

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

# Why asset-level readiness scores matter

Climate and physical risks manifest at the asset scale, while most publicly available indicators remain aggregated at regional or national levels. This project derives asset-level adaptation readiness scores by integrating elevation models, hydrological features, and flood-defense infrastructure into a consistent spatial framework. By converting heterogeneous geospatial signals into comparable metrics, the approach supports risk differentiation within portfolios, enabling business actors to identify assets that are structurally protected versus those where exposure remains unmanaged, informing adaptation planning, insurance assessment, and capital allocation.

# Scalability and data-driven extensibility

The pipeline is built on widely available geospatial data sources and standard spatial data structures to enable scalability. Elevation is sourced from raster DEMs, land extent from Natural Earth, and surface water features from OpenStreetMap-derived Geofabrik datasets; flood defenses are ingested as vector geometries. These inputs are normalized into a single projected CRS (EPSG:28992) and processed through raster- and index-based spatial algorithms, allowing the methodology to scale to hundreds of thousands of assets and to be extended to new geographies by substituting equivalent DEMs, land masks, and hydrology layers without altering the core logic.

# Technical challenges, data risks, and mitigation strategies

Key challenges include distinguishing sea from inland water in low-elevation terrain, handling inconsistent geometry quality in open-source hydrology datasets, and computing proximity metrics efficiently at scale. These are mitigated through a rule-based sea definition combining DEM thresholds and authoritative land masks, geometry normalization and sampling of flood-defense features, and the use of Euclidean Distance Transforms and KD-Tree spatial indexing to avoid expensive pairwise spatial operations. Residual risks remain due to incompleteness or temporal mismatch in open datasets (e.g. OSM coverage variability, static DEM assumptions), which are explicitly acknowledged; the pipeline is therefore designed to be deterministic, auditable, and replaceable, allowing higher-quality or proprietary data sources to be integrated as they become available.

# Data sources and assumptions

The methodology integrates multiple geospatial data sources, each selected for coverage, consistency, and reproducibility. Elevation is derived from a raster Digital Elevation Model (DEM) projected to EPSG:28992 and treated as a static representation of terrain. Land extent is defined using Natural Earth land masks to establish authoritative separation between land and open sea. Surface water features (coastal waters, rivers, channels, lakes) are sourced from OpenStreetMap-derived Geofabrik datasets and ingested as vector geometries. Flood-defense infrastructure is provided as vector datasets representing levees, dikes, and related protection structures, normalized across geometry types.

Key assumptions include the use of elevation thresholds (DEM ≤ 0 m) combined with land masks to delineate coastal sea exposure, the treatment of hydrological features as static in time, and the interpretation of proximity to flood defenses as a proxy for structural protection effectiveness. Open-source hydrology and defense datasets may exhibit spatial incompleteness, temporal lag, or regional heterogeneity; these limitations are explicitly acknowledged. The pipeline is therefore designed to be data-source agnostic, enabling the substitution of higher-resolution, proprietary, or time-varying datasets without changing the core processing logic or scoring framework.

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
