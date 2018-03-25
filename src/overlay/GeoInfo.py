from osgeo import gdal
from usng import USNGtoLL, LLtoUSNG
import math


def compute_gridlines( data ):
	# Goal: Given GPS coords of the four corners of the image, the dimensions, and the pixelsize
	# compute the coordinates of the 1000-meter grid lines to be drawn on the tiff image
	if data is None:
		return None

	pixelscale = data["pxscale"]
	tl = data["tl"]
	tr = data["tr"]
	bl = data["bl"]
	br = data["br"]
	xdim = int(data["xdim"])
	ydim = int(data["ydim"])

	usng_tl = LLtoUSNG( tl[0], tl[1], 5 )
	usng_br = LLtoUSNG( br[0], br[1], 5 )
	# Using the top left USNG coordinate, to find grid intersections we want to find the pixels defined by
	# a usng position of 2 decimal precision that lie within the image
	# e.g. next grid intersection for 15R TN 53713 69563 would be at 15R TN 54 70
	#"official" values are only for DMS02.tif for testing and future verification.
	or_usng = usng_tl.split()
	print( "Top left :", usng_tl, "Tl official: 15R TN 53713 69563" )
	print( "Bot right:", usng_br, "Br official: 15R TN 54383 69148" )

	# get usng values for the next grid intersection
	east = (int(or_usng[2]) // 1000) + 1
	north = (int(or_usng[3]) // 1000) + 1

	# build the usng coord for the intersection
	cur_usng = or_usng[0] + " " + or_usng[1] + "  " + str(east) + " " + str(north)

	# get the gps coords of the intersection and clamp to 1m precision
	next_cross = USNGtoLL(cur_usng)
	next_cross[0] = clamp(next_cross[0])
	next_cross[1] = clamp(next_cross[1])

	#
	print("Next cross:", next_cross[0], next_cross[1])
	print("Top left:", tl[0], tl[1] )

	# get the image coordinates for that gps location using pixelscale
	# x_span = (next_cross[0] - tl[1]) / pixelscale[0]
	x_span = abs( int( (tl[0] - next_cross[0]) / pixelscale[0] ) )
	y_span = abs( int( (tl[1] - next_cross[1]) / pixelscale[1] ) )
	print( "Cross coords px:", x_span, y_span )

	lines = []
	lines.append([ y_span, 0, y_span, ydim ])
	lines.append([ 0, x_span, xdim, x_span ])

	return lines

def get_points( filename = "C:\\Users\\jordan\\Documents\\dev\\DMS02.tif" ):
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)
    geotransform = dataset.GetGeoTransform()
    data = {}
    if len(geotransform) == 6:
    	# Clamp the gps coordinates to 5 decimal places (this is 1m precision, highest 
    	# possible in USNG system), and any further digits are unlikely to
    	# be meaningful since the GPS reading was from a drone
    	# Note: the geotif tags come in as [ long, lat ] and are flipped here.

    	# This set uses all of the decimal places provided (13 usually- micron level precision)
    	# however there is no chance the drone has that level of accuracy, but it's unclear how to
    	# set the precision gdal uses to compute pixelScale, so either we must deal with the imprecision
    	# or get gdal to compute pixelscale using GPS coords to 5 decimal places only.
        data["pxscale"] = ( geotransform[1], geotransform[5] )
        data["tl"] = ( geotransform[3], geotransform[0] )
        data["tr"] = ( geotransform[3], geotransform[0] + ( geotransform[1] * dataset.RasterXSize )  )
        data["bl"] = ( geotransform[3] + ( geotransform[5] * dataset.RasterYSize ), geotransform[0] )
        data["br"] = ( data["bl"][0], data["tr"][1] )
        data["xdim"] = dataset.RasterXSize
        data["ydim"] = dataset.RasterYSize

        # data["pxscale"] = ( geotransform[1], geotransform[5] )
        # data["tl"] = ( geotransform[0], geotransform[3] )
        # data["tr"] = ( geotransform[0] + ( geotransform[1] * dataset.RasterXSize ), geotransform[3] )
        # data["bl"] = ( geotransform[0], geotransform[3] + ( geotransform[5] * dataset.RasterYSize ) )
        # data["br"] = ( data["tr"][0], data["bl"][1] )
        # data["xdim"] = dataset.RasterXSize
        # data["ydim"] = dataset.RasterYSize

        # data3 = {}
        # data3["tl"] = ( clamp(geotransform[0]), clamp(geotransform[3]) )
        # data3["tr"] = ( clamp( clamp(geotransform[0]) + ( geotransform[1] * dataset.RasterXSize ) ), clamp(geotransform[3]) )
        # data3["bl"] = ( clamp(geotransform[0]), clamp( clamp(geotransform[3]) + ( geotransform[5] * dataset.RasterYSize ) ) )
        # data3["br"] = ( data3["tr"][0], data3["bl"][1])
        # data3["xdim"] = dataset.RasterXSize
        # data3["ydim"] = dataset.RasterYSize
        # data3["pxsize"] = ( geotransform[1], geotransform[5] )
# 
        # print("HEY", (data['br'][0] - data['tl'][0]) / data['pxscale'][0] )
        # print("HEY", (data['br'][1] - data['tl'][1]) / data['pxscale'][1] )

        # print("HEY", (data3['br'][0] - data3['tl'][0]) / data3['pxsize'][0] )
        # print("HEY", (data3['br'][1] - data3['tl'][1]) / data3['pxsize'][1] )

        # print( geotransform[0], geotransform[3] )
        # for k in data:
        	# print( k, data[k] )

        return data
    else:
        return None

# For labeling waypoints in left widget, given image coords from a click return the USNG coordinates
def pixels_to_usng( x, y ):
	pass

# Limit gps values to 5 decimal places (1m precision) if needed
def clamp( fnum ):
	if fnum > 0:
		return math.floor( fnum * 100000 ) / 100000
	else:
		return math.ceil( fnum * 100000 ) / 100000
