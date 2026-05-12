# Arctic In-Situ Hydrographic Data Processing Pipeline

This repository contains a collection of Jupyter notebooks for loading, cleaning, interpolating, quality controlling, and processing Arctic Ocean in-situ hydrographic observations from multiple observational programs and databases.

The workflow is designed to create harmonized temperature (`TEMP`) and salinity (`PSAL`) profile datasets suitable for climate variability studies, thermohaline structure analysis, and anomaly computations in the Arctic Ocean.

---

# Repository Structure

The processing pipeline is organized into multiple levels.

---

## 1. Data Loading and Interpolation

These notebooks load raw observational datasets and interpolate profiles onto a common vertical grid.

| Notebook | Description |
|---|---|
| `load_interp_ARGO_data_clean.ipynb` | Load and preprocess cleaned ARGO profiles |
| `load_interp_ARGO_data_interp.ipynb` | Interpolate ARGO profiles onto standard depth levels |
| `load_interp_BGEP_CTD.ipynb` | Process Beaufort Gyre Exploration Project (BGEP) CTD data |
| `load_interp_CORA_data.ipynb` | Load and interpolate CORA hydrographic profiles |
| `load_interp_ICES_data.ipynb` | Process ICES Arctic hydrographic observations |
| `load_interp_ITP_data.ipynb` | Load and interpolate Ice-Tethered Profiler (ITP) data |
| `load_interp_NABOS_CTD.ipynb` | Process NABOS CTD observations |
| `load_interp_UDASH_data.ipynb` | Load and interpolate UDASH Arctic observations |
| `load_interp_WOD23_data.ipynb` | Process World Ocean Database 2023 (WOD23) profiles |

---

## 2. Level-1 Processing: Duplicate Detection

Initial quality-control procedures to identify and remove duplicate temperature and salinity profiles.

| Notebook | Description |
|---|---|
| `process_data_level1_check_for_duplicates_psal_new_final.ipynb` | Detect duplicate salinity profiles |
| `process_data_level1_check_for_duplicates_temp_new_final.ipynb` | Detect duplicate temperature profiles |

---

## 3. Level-2 Processing: Quality Control

Advanced profile-level quality control and removal of suspicious or bad profiles.

| Notebook | Description |
|---|---|
| `process_data_level2_PSAL.ipynb` | Salinity profile quality control |
| `process_data_level2_PSAL_remove_bad_profile.ipynb` | Remove problematic salinity profiles |
| `process_data_level2_TEMP.ipynb` | Temperature profile quality control |
| `process_data_level2_TEMP_remove_bad_profiles.ipynb` | Remove problematic temperature profiles |

---

## 4. Level-3 Processing: Common Temperature–Salinity Dataset

Construction of a consistent dataset containing common temperature and salinity profiles.

| Notebook | Description |
|---|---|
| `process_data_level3_take_common_TS_profiles.ipynb` | Generate common T/S profiles |
| `process_data_level3_take_common_TS_bad_profiles_removed.ipynb` | Generate common T/S dataset after QC filtering |

---

## 5. Level-4 Processing: Anomaly Computation

Compute anomalies relative to the ISAS climatology/reference dataset.

| Notebook | Description |
|---|---|
| `process_data_level4_compute_anomalies_relative_ISAS_psal.ipynb` | Compute salinity anomalies |
| `process_data_level4_compute_anomalies_relative_ISAS_temp.ipynb` | Compute temperature anomalies |

---

## 6. Level-5 Processing: Detrending

Remove long-term trends from anomaly fields for variability analysis.

| Notebook | Description |
|---|---|
| `process_data_level5_detrend_anomalies_psal.ipynb` | Detrend salinity anomalies |
| `process_data_level5_detrend_anomalies_temp.ipynb` | Detrend temperature anomalies |

---

# Scientific Objectives

This processing framework is intended for:

- Arctic Ocean hydrographic analysis
- Temperature and salinity variability studies
- Water mass transformation studies
- Thermohaline structure analysis
- Climate variability and trend detection
- Arctic freshwater content studies
- Comparison with ocean reanalyses and climate models

---

# Datasets Included

The repository integrates observations from several major Arctic observing systems:

- ARGO
- BGEP
- CORA
- ICES
- ITP
- NABOS
- UDASH
- WOD23

---

# Typical Workflow

Recommended execution order:

```text
1. Load and interpolate raw datasets
2. Remove duplicate profiles
3. Perform quality control
4. Build common T/S datasets
5. Compute anomalies relative to ISAS
6. Detrend anomalies
```

---

# Requirements

Typical Python packages used in the notebooks include:

```python
xarray
numpy
scipy
pandas
matplotlib
netCDF4
gsw
cartopy
cmocean
dask
```

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

# Output Products

The pipeline produces:

- Quality-controlled Arctic hydrographic profiles
- Interpolated temperature and salinity fields
- Common T/S datasets
- Temperature anomalies
- Salinity anomalies
- Detrended anomaly datasets

These outputs can be used for downstream climate diagnostics and oceanographic analyses.

---

# Notes

- Some notebooks may require access to locally stored observational datasets.
- Paths to raw data may need to be updated depending on your system configuration.
- Intermediate NetCDF files are generated between processing levels.

---

# Citation

If you use this repository in scientific work, please cite the relevant observational datasets and associated publications.

---

# License

Specify your preferred license here (e.g., MIT, GPL-3.0, Apache-2.0).

---

# Contact

For questions, issues, or collaboration opportunities, please open a GitHub issue or contact the repository maintainer.
