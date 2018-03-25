from osgeo import gdal
from usng import USNGtoLL, LLtoUSNG
from PyQt5.QtCore import QLineF
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

	tl_usng = LLtoUSNG( tl[0], tl[1], 5 ).split()	# USNG of form e.g. [ '15R', 'TN', '54', '69' ]
	br_usng = LLtoUSNG( br[0], br[1], 5 ).split()

	# Using the top left USNG coordinate, to find grid intersections we want to find the pixels defined by
	# a usng position of 2 decimal precision that lie within the image
	# e.g. next grid intersection for 15R TN 53713 69563 would be at 15R TN 54 70
	#"official" values are only for DMS02.tif for testing and future verification.
	# print( "Top left :", tl_usng, "Tl official: 15R TN 53713 69563" )
	# print( "Bot right:", br_usng, "Br official: 15R TN 54383 69148" )

	cur_usng = tl_usng
	# print( "cur_usng:", cur_usng )

	# The grid line to our east has a higher value, ciel to next thousand
	# east = round( int(cur_usng[2]) + 499, -3 )
	east = round( int(cur_usng[2]) + 499, -3 )
	# The grid line to our south has a lower value, floor to previous thousand
	# north = round( int(cur_usng[3]) - 500, -3 )
	north = round( int(cur_usng[3]) - 500, -3 )

	lines = []
	for i in range(0,3):
	# Compute USNG coords of next (south east) grid intersection
		# print( cur_usng[2], cur_usng[3] )

		#print( east, north )

		# If either of the grid lines goes through the scene, we want to draw it
		if (east < int(br_usng[2])) or (north > int(br_usng[3])):

			cross_usng = cur_usng[0] + " " + cur_usng[1] + " " + str(east) + " " + str(north)
			#print(cross_usng)
			next_cross = USNGtoLL(cross_usng)
			next_cross[0] = clamp(next_cross[0]) # latitude
			next_cross[1] = clamp(next_cross[1]) # longitude
			print( "top_left gps:  ", clamp(tl[0]), clamp(tl[1]) )
			tl = [ clamp(tl[0]), clamp(tl[1]) ]
			print( "next_cross gps:", next_cross[0], next_cross[1] )
			print( "x span gps:", tl[1] - next_cross[1] )
			print( "y:", next_cross[0] - tl[0] )
			print( "pixelscale lat: ", pixelscale[0] )
			print( "pixelscale long:", pixelscale[1] )
			#
			# print("Next cross:", next_cross[0], next_cross[1])
			# print("Top left:", tl[0], tl[1] )

			# get the image coordinates for that gps location using pixelscale
			# x_span = (next_cross[0] - tl[1]) / pixelscale[0]
			x_span = abs(int( (next_cross[1] - tl[1]) / pixelscale[1] ))
			y_span = int( (tl[0] - next_cross[0]) / pixelscale[0] )
			print( "Cross coords px:", x_span, y_span )
			if east < int(br_usng[2]):
				lines.append( [QLineF(x_span, 0, x_span, ydim), (east % 1000 == 0) ]) #True -> 1000m gridline, False -> 100m gridline
			if north > int(br_usng[3]):
				lines.append( [QLineF(y_span, 0, y_span, ydim), (north % 1000 == 0) ])

			# Update cur_usng to the just found grid intersection
			cur_usng = cross_usng.split()
			east += 1000
			north -= 1000
			print( "cur_usng:", cur_usng )
		else:
			print( "DONE" )
			break

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
		print("pxscale:", geotransform[5], geotransform[1] )
		data["pxscale"] = ( geotransform[5], geotransform[1] )
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
		# print((data['br'][0] - data['tl'][0]) / data['pxscale'][0] )
		# print((data['br'][1] - data['tl'][1]) / data['pxscale'][1] )

		# print("HEY", (data3['br'][0] - data3['tl'][0]) / data3['pxsize'][0] )
		# print("HEY", (data3['br'][1] - data3['tl'][1]) / data3['pxsize'][1] )

		# print( geotransform[0], geotransform[3] )
		# for k in data:
			# print( k, data[k] )

		return data
	else:
		return None

# For labeling waypoints in left widget, given image coords from a click return the USNG coordinates
#tl -> [ lat, long ], pxscale -> [ xscale, yscale ]
def pixels_to_usng( x, y, tl, pxscale ):
	# Convert the image coordinates to GPS LL
	pts = get_points
	ll = LLtoUSNG( tl[0] + pxscale[0] * y, tl[1] + pxscale[1] * x, 5 )
	return ll

# Limit gps values to 5 decimal places (1m precision) if needed
def clamp( fnum ):
	if fnum > 0:
		return math.floor( fnum * 100000 ) / 100000
	else:
		return math.ceil( fnum * 100000 ) / 100000
