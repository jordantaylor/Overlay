import os

#by calling build entry you add a file to the folder saves

def buildEntry(name, pointArray):

    #windows
    savepath = ("..\\..\\saves")
    
    #unix
    #savepath = ("../../saves")



    #strip name out of filepath
    while "\\" in name:
        index = name.find("\\") 
        name = name[index:]
    name = name[:-4]
    print("Saving waypoints to %s_waypoints.txt" % name)


    entry = ""
    newFile = os.path.join(savepath, name + "_waypoints.txt")

    f = open(newFile, "w+")

        #loop to insert entries
    for point in pointArray:

        #x data
        xdata = str(point.x)
        #y data
        ydata = str(point.y)
        
        newEntry = xdata + "," + ydata
        

        #test function 
        #newEntry = point

        f.write("%s\n" % newEntry)
    f.close()



#test function
"""
testName = input("filename: ")

testArray = input("array: ")

buildEntry(testName, testArray)
"""


