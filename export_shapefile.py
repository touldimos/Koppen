import rasterio
from osgeo import gdal,ogr

def export_tif(profile, koppen_map, out):
    with rasterio.open('{}/Koppen.tif'.format(out), 'w', **profile) as dst:
        print ("creating tif...")
        dst.write(koppen_map, 1)

def tiff_to_shp(exp, out):
    type_mapping = { gdal.GDT_Byte: ogr.OFTInteger,
                     gdal.GDT_UInt16: ogr.OFTInteger,   
                     gdal.GDT_Int16: ogr.OFTInteger,    
                     gdal.GDT_UInt32: ogr.OFTInteger,
                     gdal.GDT_Int32: ogr.OFTInteger,
                     gdal.GDT_Float32: ogr.OFTReal,
                     gdal.GDT_Float64: ogr.OFTReal,
                     gdal.GDT_CInt16: ogr.OFTInteger,
                     gdal.GDT_CInt32: ogr.OFTInteger,
                     gdal.GDT_CFloat32: ogr.OFTReal,
                     gdal.GDT_CFloat64: ogr.OFTReal}
    
    gdal.UseExceptions()
    ds = gdal.Open(exp)
    srcband = ds.GetRasterBand(1)
    
    print ("creating shapefile...")
    dst_layername = "Shape"
    drv = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = drv.CreateDataSource("{}/poly_out.shp".format(out))
    dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )
    raster_field = ogr.FieldDefn('Koppen', type_mapping[srcband.DataType])
    dst_layer.CreateField(raster_field)
    gdal.Polygonize(srcband, None, dst_layer, 0, [], callback=None)