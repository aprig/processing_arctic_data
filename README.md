# Arctic In-Situ Hydrographic Data Processing Pipeline

This repository contains a collection of Jupyter notebooks for loading, cleaning, interpolating, quality controlling, and processing Arctic Ocean in-situ hydrographic observations from multiple observational programs and databases.

The workflow is designed to create harmonized temperature (`TEMP`) and salinity (`PSAL`) profile datasets of the Arctic Ocean.

---

# Repository Structure

The processing pipeline is organized into multiple levels.

---

## 1. Data Loading and Interpolation

These notebooks load raw observational datasets and interpolate profiles onto a common vertical grid and concatenate the data.

| Notebook | Description |
|---|---|
| `load_interp_ARGO_data_clean.ipynb` | Load and preprocess ARGO profiles |
| `load_interp_ARGO_data_interp.ipynb` | Load and preprocess ARGO profiles with a lot of QC==b'8' and for which we have under ice trajectories|
| `read_BGEP_CTD_to_netcdf.ipynb` | Read BGEP .cnv file and save to yearly .nc files  |
| `load_interp_BGEP_CTD.ipynb` | Process Beaufort Gyre Exploration Project (BGEP) CTD data |
| `load_interp_CORA_data.ipynb` | Load and interpolate CORA hydrographic profiles |
| `read_ICES_CTD_to_netcdf.ipynb` | Read ICES .csv file and save to yearly .nc files  |
| `load_interp_ICES_data.ipynb` | Process ICES Arctic hydrographic observations |
| `load_interp_ITP_data.ipynb` | Load and interpolate Ice-Tethered Profiler (ITP) data |
| `load_interp_NABOS_CTD.ipynb` | Process NABOS CTD observations |
| `load_interp_UDASH_data.ipynb` | Load and interpolate UDASH Arctic observations |
| `load_interp_WOD23_data.ipynb` | Process World Ocean Database 2023 (WOD23) profiles |
| `load_interp_MEOP_data.ipynb` | Process Marine Mammals Exploring the Oceans Pole to Pole (MEOP) profiles |

---

## 2. Level-1 Processing: Duplicate Detection

Initial quality-control procedures to identify and remove duplicate temperature and salinity profiles.

Duplicate profiles originating from multiple observational databases are resolved using the following source priority hierarchy:

```python
SOURCE_PRIORITY = {

    "ARGO":      0,
    "ITP":       1,
    "NABOS_ctd": 2,
    "BGEP_ctd":  3,
    "MEOP":      4,
    "UDASH":     5,
    "ICES":      6,
    "WOD":       7,
    "CORA":      8,
}
```

Lower priority values indicate datasets that are preferentially retained when duplicate profiles are detected.

| Notebook | Description |
|---|---|
| `process_data_level1_check_for_duplicates_psal_new_final.ipynb` | Detect duplicate salinity profiles |
| `process_data_level1_check_for_duplicates_temp_new_final.ipynb` | Detect duplicate temperature profiles |

---

## 3. Level-2 Processing: Quality Control

 Quality control and removal of suspicious or bad profiles. The QC is done first on the profiles within 3˚ by 150 km boxes. Outliers or bad profiles are identified if they fall outside median +/- 5 std. Then the QC is per basins. 

| Notebook | Description |
|---|---|
| `process_data_level2_PSAL.ipynb` | Remove outliers |
| `process_data_level2_PSAL_remove_bad_profile.ipynb` | Remove problematic salinity profiles |
| `process_data_level2_TEMP.ipynb` | Remove outliers |
| `process_data_level2_TEMP_remove_bad_profiles.ipynb` | Remove problematic temperature profiles |
| `define_mask.ipynb` | Generate masks for the different regions and basins of the Arctic Ocean |

---

## 4. Level-3 Processing: Common Temperature–Salinity Dataset

Construction of a consistent dataset containing common temperature and salinity profiles. Common profiles are found using lon, lat, time.

| Notebook | Description |
|---|---|
| `process_data_level3_take_common_TS_profiles.ipynb` | Generate common T/S profiles after outlier filtering |
| `process_data_level3_take_common_TS_bad_profiles_removed.ipynb` | Generate common T/S dataset after profile filtering |

---

## 5. Level-4 Processing: Anomaly Computation

Compute anomalies relative to the ISAS climatology/reference dataset. The climatology is colocated to the position of each profile using bi-linear interpolation.

| Notebook | Description |
|---|---|
| `process_data_level4_compute_anomalies_relative_ISAS_psal.ipynb` | Compute salinity anomalies |
| `process_data_level4_compute_anomalies_relative_ISAS_temp.ipynb` | Compute temperature anomalies |

---

## 6. Level-5 Processing: Detrending

Remove long-term trends from anomaly fields for variability analysis. Only significant trends are removed.

| Notebook | Description |
|---|---|
| `process_data_level5_detrend_anomalies_psal.ipynb` | Detrend salinity anomalies |
| `process_data_level5_detrend_anomalies_temp.ipynb` | Detrend temperature anomalies |

---

# Datasets Included (Links accessed on the 29/06/2026 )

The repository integrates observations from several major Arctic observing systems:

- ARGO
- BGEP https://www2.whoi.edu/site/beaufortgyre/data/ctd-and-geochemistry/
- MEOP https://meop.net/database/
- CORA https://data.marine.copernicus.eu/product/INSITU_GLO_PHY_TS_DISCRETE_MY_013_001/description
- ICES https://www.ices.dk/Pages/default.aspx
- ITP https://www2.whoi.edu/site/itp/data/
- NABOS https://uaf-iarc.org/nabos/data/
- UDASH https://doi.pangaea.de/10.1594/PANGAEA.872931
- WOD23 https://www.ncei.noaa.gov/products/world-ocean-database


