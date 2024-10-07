from src.core import sampling


shp_path = r'test\point.shp'
rs_path = r'test\E104N24_S2MSI_2022.tif'
out_path = r'output.csv'
epsg = 4326


if __name__ == "__main__":
    sampling(shp_path, rs_path, out_path, epsg)

