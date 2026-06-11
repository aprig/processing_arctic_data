# Author: Arthur Prigent
# Email: arthur.prigent@univ-brest.fr
# 04/03/2026
##########################################################################################
##########################################################################################
##########################################################################################
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import netCDF4
import datetime as dt
from mpl_toolkits.basemap import Basemap
import gsw
import glob
import pandas as pd

import numpy as np
import matplotlib.path as mpath
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
##########################################################################################
##########################################################################################
##########################################################################################
def concat_netcdf_psal(file_list):
    if len(file_list)>1:
        ds = xr.open_dataset(file_list[0],decode_times=False)

        param = ds.salinity.data
        param1 = ds.sum_salinity.data
        param2 = ds.sum_levels.data
        param3 = ds.nb_levels.data
        param4 = ds.prof_descr.data
        lon = np.round(ds.longitude.data,4)
        lat = np.round(ds.latitude.data,4)
        time = np.floor(ds.time.data)
        depth = ds.depth.data

        for f in file_list[1:]:
            ds = xr.open_dataset(f,decode_times=False)
            param = np.concatenate((param, ds.salinity.data),axis=0)
            param1 = np.concatenate((param1, ds.sum_salinity.data),axis=0)
            param2 = np.concatenate((param2, ds.sum_levels.data),axis=0)
            param3 = np.concatenate((param3, ds.nb_levels.data),axis=0)
            param4 = np.concatenate((param4, ds.prof_descr.data),axis=0)
            lon = np.concatenate((lon, np.round(ds.longitude.data,4)),axis=0)
            lat = np.concatenate((lat, np.round(ds.latitude.data,4)),axis=0)
            time = np.concatenate((time, np.floor(ds.time.data)),axis=0)
    else:        
        ds = xr.open_dataset(file_list[0],decode_times=False)
        param = ds.salinity.data
        param1 = ds.sum_salinity.data
        param2 = ds.sum_levels.data
        param3 = ds.nb_levels.data
        param4 = ds.prof_descr.data
        lon = np.round(ds.longitude.data,4)
        lat = np.round(ds.latitude.data,4)
        time = np.floor(ds.time.data)
        depth = ds.depth.data
        
        
    return param,param1,param2,param3,param4,lon,lat,time,depth

##########################################################################################
def concat_netcdf_temp(file_list):
    if len(file_list)>1:
        ds = xr.open_dataset(file_list[0],decode_times=False)
        param = ds.temperature.data
        param1 = ds.sum_temperature.data
        param2 = ds.sum_levels.data
        param3 = ds.nb_levels.data
        param4 = ds.prof_descr.data
        
        lon = np.round(ds.longitude.data,4)
        lat = np.round(ds.latitude.data,4)
        time = np.floor(ds.time.data)
        depth = ds.depth.data

        for f in file_list[1:]:
            ds = xr.open_dataset(f,decode_times=False)
            param = np.concatenate((param, ds.temperature.data),axis=0)
            param1 = np.concatenate((param1, ds.sum_temperature.data),axis=0)
            param2 = np.concatenate((param2, ds.sum_levels.data),axis=0)
            param3 = np.concatenate((param3, ds.nb_levels.data),axis=0)
            param4 = np.concatenate((param4, ds.prof_descr.data),axis=0)
            lon = np.concatenate((lon, np.round(ds.longitude.data,4)),axis=0)
            lat = np.concatenate((lat, np.round(ds.latitude.data,4)),axis=0)
            time = np.concatenate((time, np.floor(ds.time.data)),axis=0)
    else:
        ds = xr.open_dataset(file_list[0],decode_times=False)
        param = ds.temperature.data
        param1 = ds.sum_temperature.data
        param2 = ds.sum_levels.data
        param3 = ds.nb_levels.data
        param4 = ds.prof_descr.data
        lon = np.round(ds.longitude.data,4)
        lat = np.round(ds.latitude.data,4)
        time = np.floor(ds.time.data)
        depth = ds.depth.data
        
        
    return param,param1,param2,param3,param4,lon,lat,time,depth
##########################################################################################
def create_merged_dataset_psal(list_psal,source,variable):
    psal,sum_psal,sum_dep,nb_dep,prof_description,lon_psal,lat_psal,time_psal, dep_psal = concat_netcdf_psal(list_psal)


    nprof = len(lat_psal)
    ndepth = len(dep_psal)
    source_array = np.full(nprof, source)  # array of 'UDASH' repeated nprof times
    duplicate_array = np.full(nprof, False)  # array of 'UDASH' repeated nprof times

    ds = xr.Dataset(
        data_vars=dict(
            longitude=("profile", lon_psal),
            latitude=("profile", lat_psal),
            time=("profile",time_psal),
            source=("profile",source_array),
            dataset_index=("profile", np.arange(nprof)),
            is_duplicate = ("profile",duplicate_array),
            salinity=(("profile", "depth"), psal),
            sum_salinity = ("profile",sum_psal),
            sum_depth = ("profile",sum_dep),
            nb_depth = ("profile",nb_dep),
            prof_descr = ("profile",prof_description)
            
        ),
        coords=dict(
            profile=np.arange(nprof),
            depth=("depth", dep_psal)
        ),
        attrs=dict(
            title=source+" salinity profiles",
            source=source,
            featureType="profile"
        )
    )
    ds.attrs['Comments'] = source+' temperature profiles interpolated on ISAS vertical levels using a Akima 1D interpolator scheme (scipy)'
    ds["longitude"].attrs = {
        "standard_name": "longitude",
        "units": "degrees_east"
    }

    ds["latitude"].attrs = {
        "standard_name": "latitude",
        "units": "degrees_north"
    }

    ds["time"].attrs = {
        "long_name": "time",
        "description": "Python ordinal day count",
        "units": "days since 0001-01-01 00:00:00",
        "calendar": "proleptic_gregorian"
    }


    ds["depth"].attrs = {
        "standard_name": "depth",
        "units": "m",
        "positive": "down"
    }

    ds["salinity"].attrs = {
        "standard_name": "sea_water_practical_salinity",
        "long_name": "Practical salinity",
        "units": "1e-3"
    }
    ## Ensure that the profile are made north of 65N ##
    ds = ds.where(ds.latitude>65,drop=True)
    return ds


##########################################################################################


def create_merged_dataset_temp(list_psal,source,variable):
    psal,sum_psal,sum_dep,nb_dep,prof_description,lon_psal,lat_psal,time_psal, dep_psal = concat_netcdf_temp(list_psal)


    nprof = len(lat_psal)
    ndepth = len(dep_psal)
    source_array = np.full(nprof, source)  # array of 'UDASH' repeated nprof times
    duplicate_array = np.full(nprof, False)  # array of 'UDASH' repeated nprof times

    ds = xr.Dataset(
        data_vars=dict(
            longitude=("profile", lon_psal),
            latitude=("profile", lat_psal),
            time=("profile",time_psal),
            source=("profile",source_array),
            dataset_index=("profile", np.arange(nprof)),
            is_duplicate = ("profile",duplicate_array),
            temperature=(("profile", "depth"), psal),
            sum_temperature = ("profile",sum_psal),
            sum_depth = ("profile",sum_dep),
            nb_depth = ("profile",nb_dep),
            prof_descr = ("profile",prof_description)
            
        ),
        coords=dict(
            profile=np.arange(nprof),
            depth=("depth", dep_psal)
        ),
        attrs=dict(
            title=source+" temperature profiles",
            source=source,
            featureType="profile"
        )
    )
    ds.attrs['Comments'] = source+' temperature profiles interpolated on ISAS vertical levels using a Akima 1D interpolator scheme (scipy)'
    ds["longitude"].attrs = {
        "standard_name": "longitude",
        "units": "degrees_east"
    }

    ds["latitude"].attrs = {
        "standard_name": "latitude",
        "units": "degrees_north"
    }

    ds["time"].attrs = {
        "long_name": "time",
        "description": "Python ordinal day count",
        "units": "days since 0001-01-01 00:00:00",
        "calendar": "proleptic_gregorian"
    }


    ds["depth"].attrs = {
        "standard_name": "depth",
        "units": "m",
        "positive": "down"
    }

    ds["temperature"].attrs = {
        "standard_name": "sea_water_temperature",
        "units": "degC"
    }
    ## Ensure that the profile are made north of 65N ##
    ds = ds.where(ds.latitude>65,drop=True)
    return ds

##########################################################################################


import numpy as np
import gsw

def find_duplicates(lon, lat, time, profiles,
                                       time_thresh_days=1, 
                                       lon_thresh=0.02, lat_thresh=0.02, 
                                       dist_thresh_km=2):
    """
    Find duplicates using gsw.distance and return both:
      - boolean mask of duplicate profiles
      - list of duplicate pairs (i, j)
    
    """
    
    
    n = len(lon)
    duplicate_mask = np.zeros(n, dtype=bool)
    duplicate_pairs = []

    # Truncate time to integer days
    time_days = np.floor(time)
    finite_counts = np.sum(np.isfinite(profiles), axis=1)
    for i in range(n):
        j = np.arange(i+1, n)

        # Time threshold
        time_ok = np.abs(time_days[j] - time_days[i]) < time_thresh_days

        
        # Coordinate thresholds
        lon_ok = np.abs(lon[j] - lon[i]) <= lon_thresh
        lat_ok = np.abs(lat[j] - lat[i]) <= lat_thresh
        
        # Finite-value condition
        finite_ok = finite_counts[j] == finite_counts[i]

        candidates = j[time_ok & lon_ok & lat_ok & finite_ok]
        if len(candidates) == 0:
            continue
        
        # Compute geodesic distances using gsw.distance
        d_km = np.array([
            gsw.distance(np.array([[lon[i], lon[c]]]), np.array([[lat[i], lat[c]]])) / 1000.0
            for c in candidates
        ]).flatten()
        
        candidates = np.array(candidates)
        duplicates = candidates[d_km <= dist_thresh_km]

        if len(duplicates) > 0:
            # mark duplicate profiles
            duplicate_mask[duplicates] = True
            # save duplicate pairs
            duplicate_pairs.extend([(i, dup) for dup in duplicates])

    return duplicate_mask, duplicate_pairs

##########################################################################################

def find_duplicates_new(lon, lat, time, profiles, source,
                    time_thresh_days=1, 
                    lon_thresh=0.05, lat_thresh=0.01, 
                    dist_thresh_km=2):
    """
    Find duplicates using gsw.distance and return:
      - boolean mask of duplicate profiles
      - list of duplicate pairs (i, j)

    Duplicate profiles must also come from different source datasets.
    """
    
    n = len(lon)
    duplicate_mask = np.zeros(n, dtype=bool)
    duplicate_pairs = []

    # Truncate time to integer days
    time_days = np.floor(time)
    finite_counts = np.sum(np.isfinite(profiles), axis=1)
    
    
    # Pre-sort by time
    order = np.argsort(time_days)
    lon       = lon[order]
    lat       = lat[order]
    
    lon = np.round(lon,4)
    lat = np.round(lat,4)
    time_days = time_days[order]
    finite_counts = finite_counts[order]
    source    = source[order]
    
    

    for i in range(n):
        if i % 10000 == 0:
            print("Processing", i)
        j = np.arange(i + 1, n)
        time_diff = np.abs(time_days[j] - time_days[i])
        # Since sorted, once time_diff exceeds threshold we can stop
        exceeds = np.where(time_diff > time_thresh_days)[0]
        
        if len(exceeds) > 0:
            j = j[:exceeds[0]]   # keep only the contiguous valid window
        if len(j) == 0:
            continue


        lon_ok    = np.abs(lon[j]          - lon[i])          <= lon_thresh
        lat_ok    = np.abs(lat[j]          - lat[i])          <= lat_thresh
        finite_ok = np.abs(finite_counts[j] - finite_counts[i]) <= 3
        source_ok = source[j] != source[i]

        candidates = j[lon_ok & lat_ok & finite_ok & source_ok]
        if len(candidates) == 0:
            continue
        
        # Compute geodesic distances using gsw.distance
        d_km = np.array([
            gsw.distance(np.array([[lon[i], lon[c]]]), np.array([[lat[i], lat[c]]])) / 1000.0
            for c in candidates
        ]).flatten()
        
        candidates = np.array(candidates)
        duplicates = candidates[d_km <= dist_thresh_km]

        if len(duplicates) > 0:
            duplicate_mask[duplicates] = True
            duplicate_pairs.extend([(i, dup) for dup in duplicates])
    # --- Remap indices back to original order before returning ---
    original_duplicate_mask = np.zeros(n, dtype=bool)
    original_duplicate_mask[order[duplicate_mask]] = True
    original_duplicate_pairs = [(order[i], order[j]) for i, j in duplicate_pairs]

    return original_duplicate_mask, original_duplicate_pairs

##########################################################################################
def find_duplicates_new2(lon, lat, time, profiles, source,
                    time_thresh_days=1, 
                    lon_thresh=0.1, lat_thresh=0.05, 
                    dist_thresh_km=2):
    n = len(lon)
    duplicate_mask = np.zeros(n, dtype=bool)
    duplicate_pairs = []

    time_days = np.floor(time)
    finite_counts = np.sum(np.isfinite(profiles), axis=1)

    order = np.argsort(time_days, kind='stable')
    lon         = np.round(lon[order], 4)
    lat         = np.round(lat[order], 4)
    time_days   = time_days[order]
    finite_counts = finite_counts[order]
    source      = source[order]

    R = 6371.0
    lat_rad = np.deg2rad(lat)
    lon_rad = np.deg2rad(lon)

    for i in range(n):
        if i % 10000 == 0:
            print("Processing", i)

        j = np.arange(i + 1, n)

        # Correct time filter: keep all valid, not just up to first exceed
        time_ok   = np.abs(time_days[j] - time_days[i]) <= time_thresh_days

        # if the MINIMUM time_diff already exceeds threshold,
        # and time is sorted, we can safely break the outer loop entirely
        if len(j) > 0 and (time_days[j[0]] - time_days[i]) > time_thresh_days:
            break  # all future j will also exceed — safe because array is sorted

        j = j[time_ok]
        if len(j) == 0:
            continue

        lon_ok    = np.abs(lon[j]           - lon[i])           <= lon_thresh
        lat_ok    = np.abs(lat[j]           - lat[i])           <= lat_thresh
        finite_ok = np.abs(finite_counts[j] - finite_counts[i]) <= 3
        source_ok = source[j] != source[i]

        candidates = j[lon_ok & lat_ok & finite_ok & source_ok]
        if len(candidates) == 0:
            continue

        d_km = np.array([
            gsw.distance(np.array([[lon[i], lon[c]]]), np.array([[lat[i], lat[c]]])) / 1000.0
            for c in candidates
        ]).flatten()

        duplicates = candidates[d_km <= dist_thresh_km]
        if len(duplicates) > 0:
            duplicate_mask[duplicates] = True
            duplicate_pairs.extend([(i, dup) for dup in duplicates])

    original_duplicate_mask = np.zeros(n, dtype=bool)
    original_duplicate_mask[order[duplicate_mask]] = True
    original_duplicate_pairs = [(order[i], order[j]) for i, j in duplicate_pairs]

    return original_duplicate_mask, original_duplicate_pairs
##########################################################################################



def profile_similarity(x, y):
    """
    Check similarity between two profiles using both RMSE and correlation.
    Correlation catches profiles with same shape but constant offset.
    RMSE catches profiles with small absolute differences.
    """
    mask = np.isfinite(x) & np.isfinite(y)
    
    if mask.sum() < 5: # minimum of 6 points overlap
        return np.nan, np.nan
    
    x0 = x[mask]
    y0 = y[mask]
    
    rmse = np.sqrt(((x0 - y0) ** 2).mean())
    
    # Pearson correlation
    corr = np.corrcoef(x0, y0)[0, 1]
    
    return rmse, corr



##########################################################################################
        


def plot_arctic_ax_map_new(
    ax,
    ftz=15,
    extent=(-180, 180, 65, 90),
    add_land=True,
    add_coast=True,
    gridlines=True,
    add_river=True

):

    # Arctic extent
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    # ---- Make map circular ----
    theta = np.linspace(0, 2*np.pi, 100)
    center = [0.5, 0.5]
    radius = 0.5

    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)

    ax.set_boundary(circle, transform=ax.transAxes)
    # ---------------------------

    # Map features
    if add_land:
        ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=0)
    if add_coast:
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=3)
    if add_river:
        ax.add_feature(cfeature.RIVERS, linewidth=1)

    # Gridlines
    if gridlines:
        gl = ax.gridlines(
            crs=ccrs.PlateCarree(),
            draw_labels=True,
            linewidth=0.5,
            color='black',
            alpha=0.8,
            linestyle='-',
            zorder=4
        )
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': ftz, 'color': 'black'}
        gl.ylabel_style = {'size': ftz, 'color': 'black'}
        gl.xlocator = mticker.FixedLocator(np.arange(-180,185,30))
        gl.ylocator = mticker.FixedLocator(np.arange(65,86,10))

    return ax



##########################################################################################

def plot_arctic_ax_map_new2(
    ax,
    ftz=15,
    extent=(-180, 180, 65, 75),
    add_land=True,
    add_coast=True,
    gridlines=True,
    add_river=True

):

    # Arctic extent
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    # ---- Make map circular ----
    theta = np.linspace(0, 2*np.pi, 100)
    center = [0.5, 0.5]
    radius = 0.5

    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)

    ax.set_boundary(circle, transform=ax.transAxes)
    # ---------------------------

    # Map features
    if add_land:
        ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=0)
    if add_coast:
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=3)
    if add_river:
        ax.add_feature(cfeature.RIVERS, linewidth=1)

    # Gridlines
    if gridlines:
        gl = ax.gridlines(
            crs=ccrs.PlateCarree(),
            draw_labels=True,
            linewidth=0.5,
            color='black',
            alpha=0.8,
            linestyle='-',
            zorder=4
        )
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': ftz, 'color': 'black'}
        gl.ylabel_style = {'size': ftz, 'color': 'black'}
        gl.xlocator = mticker.FixedLocator(np.arange(-180,185,30))
        gl.ylocator = mticker.FixedLocator(np.arange(65,86,10))

    return ax
##########################################################################################
##########################################################################################



def concat_netcdf_psal_itp(file_list):
    if len(file_list)>1:
        ds = xr.open_dataset(file_list[0],decode_times=False)

        param = ds.salinity.data
        param1 = ds.sum_salinity.data
        param2 = ds.sum_levels.data
        param3 = ds.nb_levels.data
        param4 = ds.platform_id.data
        lon = np.round(ds.longitude.data,4)
        lat = np.round(ds.latitude.data,4)
        time = np.floor(ds.time.data)
        depth = ds.depth.data

        for f in file_list[1:]:
            ds = xr.open_dataset(f,decode_times=False)
            param = np.concatenate((param, ds.salinity.data),axis=0)
            param1 = np.concatenate((param1, ds.sum_salinity.data),axis=0)
            param2 = np.concatenate((param2, ds.sum_levels.data),axis=0)
            param3 = np.concatenate((param3, ds.nb_levels.data),axis=0)
            param4 = np.concatenate((param4, ds.platform_id.data),axis=0)
            lon = np.concatenate((lon, np.round(ds.longitude.data,4)),axis=0)
            lat = np.concatenate((lat, np.round(ds.latitude.data,4)),axis=0)
            time = np.concatenate((time, np.floor(ds.time.data)),axis=0)
    else:        
        ds = xr.open_dataset(file_list[0],decode_times=False)
        param = ds.salinity.data
        param1 = ds.sum_salinity.data
        param2 = ds.sum_levels.data
        param3 = ds.nb_levels.data
        param4 = ds.platform_id.data
        lon = np.round(ds.longitude.data,4)
        lat = np.round(ds.latitude.data,4)
        time = np.floor(ds.time.data)
        depth = ds.depth.data
        
        
    return param,param1,param2,param3,param4,lon,lat,time,depth

##########################################################################################
def concat_netcdf_temp_itp(file_list):
    if len(file_list)>1:
        ds = xr.open_dataset(file_list[0],decode_times=False)
        param = ds.temperature.data
        param1 = ds.sum_temperature.data
        param2 = ds.sum_levels.data
        param3 = ds.nb_levels.data
        param4 = ds.platform_id.data
        lon = np.round(ds.longitude.data,4)
        lat = np.round(ds.latitude.data,4)
        time = np.floor(ds.time.data)
        depth = ds.depth.data

        for f in file_list[1:]:
            ds = xr.open_dataset(f,decode_times=False)
            param = np.concatenate((param, ds.temperature.data),axis=0)
            param1 = np.concatenate((param1, ds.sum_temperature.data),axis=0)
            param2 = np.concatenate((param2, ds.sum_levels.data),axis=0)
            param3 = np.concatenate((param3, ds.nb_levels.data),axis=0)
            param4 = np.concatenate((param4, ds.platform_id.data),axis=0)
            lon = np.concatenate((lon, np.round(ds.longitude.data,4)),axis=0)
            lat = np.concatenate((lat, np.round(ds.latitude.data,4)),axis=0)
            time = np.concatenate((time, np.floor(ds.time.data)),axis=0)
    else:
        ds = xr.open_dataset(file_list[0],decode_times=False)
        param = ds.temperature.data
        param1 = ds.sum_temperature.data
        param2 = ds.sum_levels.data
        param3 = ds.nb_levels.data
        param4 = ds.platform_id.data
        lon = np.round(ds.longitude.data,4)
        lat = np.round(ds.latitude.data,4)
        time = np.floor(ds.time.data)
        depth = ds.depth.data
        
        
    return param,param1,param2,param3,param4,lon,lat,time,depth
##########################################################################################
def create_merged_dataset_psal_itp(list_psal,source,variable):
    psal,sum_psal,sum_dep,nb_dep,platform_id,lon_psal,lat_psal,time_psal, dep_psal = concat_netcdf_psal_itp(list_psal)


    nprof = len(lat_psal)
    ndepth = len(dep_psal)
    source_array = np.full(nprof, source)  # array of 'UDASH' repeated nprof times
    duplicate_array = np.full(nprof, False)  # array of 'UDASH' repeated nprof times

    ds = xr.Dataset(
        data_vars=dict(
            longitude=("profile", lon_psal),
            latitude=("profile", lat_psal),
            time=("profile",time_psal),
            source=("profile",source_array),
            dataset_index=("profile", np.arange(nprof)),
            is_duplicate = ("profile",duplicate_array),
            salinity=(("profile", "depth"), psal),
            sum_salinity = ("profile",sum_psal),
            sum_depth = ("profile",sum_dep),
            nb_depth = ("profile",nb_dep),
            platform_id = ("profile",platform_id)
            
        ),
        coords=dict(
            profile=np.arange(nprof),
            depth=("depth", dep_psal)
        ),
        attrs=dict(
            title=source+" salinity profiles",
            source=source,
            featureType="profile"
        )
    )
    ds.attrs['Comments'] = source+' temperature profiles interpolated on ISAS vertical levels using a Akima 1D interpolator scheme (scipy)'
    ds["longitude"].attrs = {
        "standard_name": "longitude",
        "units": "degrees_east"
    }

    ds["latitude"].attrs = {
        "standard_name": "latitude",
        "units": "degrees_north"
    }

    ds["time"].attrs = {
        "long_name": "time",
        "description": "Python ordinal day count",
        "units": "days since 0001-01-01 00:00:00",
        "calendar": "proleptic_gregorian"
    }


    ds["depth"].attrs = {
        "standard_name": "depth",
        "units": "m",
        "positive": "down"
    }

    ds["salinity"].attrs = {
        "standard_name": "sea_water_practical_salinity",
        "long_name": "Practical salinity",
        "units": "1e-3"
    }
    ## Ensure that the profile are made north of 65N ##
    ds = ds.where(ds.latitude>65,drop=True)
    return ds


##########################################################################################


def create_merged_dataset_temp_itp(list_psal,source,variable):
    psal,sum_psal,sum_dep,nb_dep,platform_id,lon_psal,lat_psal,time_psal, dep_psal = concat_netcdf_temp_itp(list_psal)


    nprof = len(lat_psal)
    ndepth = len(dep_psal)
    source_array = np.full(nprof, source)  # array of 'UDASH' repeated nprof times
    duplicate_array = np.full(nprof, False)  # array of 'UDASH' repeated nprof times

    ds = xr.Dataset(
        data_vars=dict(
            longitude=("profile", lon_psal),
            latitude=("profile", lat_psal),
            time=("profile",time_psal),
            source=("profile",source_array),
            dataset_index=("profile", np.arange(nprof)),
            is_duplicate = ("profile",duplicate_array),
            temperature=(("profile", "depth"), psal),
            sum_temperature = ("profile",sum_psal),
            sum_depth = ("profile",sum_dep),
            nb_depth = ("profile",nb_dep),
            platform_id = ("profile",platform_id)
            
        ),
        coords=dict(
            profile=np.arange(nprof),
            depth=("depth", dep_psal)
        ),
        attrs=dict(
            title=source+" temperature profiles",
            source=source,
            featureType="profile"
        )
    )
    ds.attrs['Comments'] = source+' temperature profiles interpolated on ISAS vertical levels using a Akima 1D interpolator scheme (scipy)'
    ds["longitude"].attrs = {
        "standard_name": "longitude",
        "units": "degrees_east"
    }

    ds["latitude"].attrs = {
        "standard_name": "latitude",
        "units": "degrees_north"
    }

    ds["time"].attrs = {
        "long_name": "time",
        "description": "Python ordinal day count",
        "units": "days since 0001-01-01 00:00:00",
        "calendar": "proleptic_gregorian"
    }


    ds["depth"].attrs = {
        "standard_name": "depth",
        "units": "m",
        "positive": "down"
    }

    ds["temperature"].attrs = {
        "standard_name": "sea_water_temperature",
        "units": "degC"
    }
    ## Ensure that the profile are made north of 65N ##
    ds = ds.where(ds.latitude>65,drop=True)
    return ds





