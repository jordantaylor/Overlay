import os

#by calling build entry you add a file to 

def buildEntry(name, pointArray):
	#entry = str(index) + "," + str(x) + ","+ str(y)
	curpath = os.path.dirname(__file__)

        #strip name out of filepath
        while "\\" in name:
            index = name.find("\\") 
            name = name[index:]
        name = name[:-4]
        print("Saving waypoints to %s" % name)


        entry = ""

        path = '\\waypoints' + name
        newpath = os.path.relpath(name + "_waypoints.txt")

	#createfile(entry, name)
        #put into way points folder
	filename = name + "_waypoints.txt"
	f = open(filename, "w+")

        #loop to insert entries
        for point in pointArray:
            #x data
            xdata = str(point.x)
            #y data
            ydata = str(point.y)

            newEntry = xdata + "," + ydata
            
            f.write("%s\n" % newEntry)
        f.close()


	#f.write("%s\n" % entry)
	#f.close()

#def removeEntry(name, index):
 #   filename = name + "_waypoints.txt"
	
	
#buildEntry("test2", "b", 10, 33)
