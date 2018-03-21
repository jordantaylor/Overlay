from osgeo import gdal

def getpoints( filename ):
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)
    geotransform = dataset.GetGeoTransform()
    data = dict()
    if len(geotransform) == 6:
        # We know it read the attributes correctly
        data["origin"] = ( geotransform[0], geotransform[3] )
        data["pixelsize"] = ( geotransform[1], geotransform[5] )
        data["topleft"] = ( geotransform[0], geotransform[3] )
        data["topright"] = ( geotransform[0] + ( geotransform[1] * dataset.RasterXSize ), geotransform[3] )
        data["btmleft"] = ( geotransform[0], geotransform[3] + ( geotransform[5] * dataset.RasterYSize ) )
        data["btmright"] = ( data["topright"][0], data["btmleft"][1] )
        return data
    else:
        return Null
