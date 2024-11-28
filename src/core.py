from osgeo import gdal
from osgeo import ogr
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
import os
import time
import geopandas as gpd
from tqdm import tqdm


shp_path = r"newWaterShp"
rs_path = r"distance\distance90.tif"
out_dir = r"dataV2\distance"


def getXYbyGpd(gdf: gpd.GeoDataFrame, epsg):
    if epsg is not None:
        gdf = gdf.to_crs(epsg=epsg)
    gdf = gdf.to_crs(epsg=epsg)
    x = gdf.geometry.centroid.x
    y = gdf.geometry.centroid.y
    return np.array(list(zip(x, y)))


def getIndex(X, Y, geotransform):
    x = geotransform[0]
    y = geotransform[3]
    dx = geotransform[1]
    dy = geotransform[5]
    i = int((X-x)/dx)
    j = int((Y-y)/dy)
    return i, j
    
    
def doit(rs, xy):
    count = rs.RasterCount
    trans = rs.GetGeoTransform()
    arr = rs.ReadAsArray()
    value = []
    if arr.ndim==2:
        for c in xy:
            i, j = getIndex(c[0], c[1], trans)
            value.append(arr[j, i])
        value = np.array(value)
    elif arr.ndim==3:
        for c in xy:
            i, j = getIndex(c[0], c[1], trans)
            value.append(arr[:, j, i])
        value = np.array(value)
    return value


# 要素中心采样提取
def sampling(shp_path, rs_path, out_path, epsg=None):
    '''
    shp_path 是shp路径\n
    rs_path 是tif路径\n
    out_path 是输出路径\n
    epsg 默认是None，指的是shp和tif的坐标系统相同的情况，如果两者不相同，请指定epsg为tif的坐标系统的epsg，代码将把shp改成和tif相同的坐标系统\n
    '''
    rs = gdal.Open(rs_path)
    shp = gpd.read_file(shp_path)
    xy = getXYbyGpd(shp, epsg=epsg)
    result = doit(rs, xy)
    df = pd.DataFrame(result)
    df.to_csv(out_path, index=False)


if __name__ == "__main__":
    
    pass

