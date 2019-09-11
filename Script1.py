import arcpy,os,math

inputFC = arcpy.GetParameter(0)
inputCenter = arcpy.GetParameter(1)
outputFC = arcpy.GetParameterAsText(2)
path=os.path.dirname(outputFC)
outputFC=os.path.basename(outputFC)

#path=r"D:\Benutzer\issh1011\Documents\ArcGIS\Default.gdb"
#arcpy.env.workspace = path


with arcpy.da.SearchCursor(inputCenter,"SHAPE@") as centercursor:
    for row in centercursor:
        xc = row[0][0].X
        yc = row[0][0].Y

arcpy.env.overwriteOutput = True
sr = arcpy.Describe(inputFC).spatialReference
arcpy.CreateFeatureclass_management(path,outputFC,'POINT',template=inputFC,spatial_reference=sr)
arcpy.AddField_management(outputFC, "Distance",field_type="DOUBLE")
arcpy.AddField_management(outputFC, "Angle",field_type="DOUBLE")





def quarter(dx,dy):

    if dx>0 and dy>0:
        return 1
    elif dx<0 and dy>0:
        return 2
    elif dx<0 and dy<0:
        return 3
    else:
        return 4

def calculate(x,y):
    dx=x-xc
    dy=y-yc
    distance=math.sqrt(dx**2+dy**2)
    angle=math.atan(dy/dx)
    r=quarter(dx,dy)
    
    if r==2 or r==3:
        angle+=math.pi
    elif r==4:
        angle+=math.pi*2

    angle=angle/math.pi*180
    #print r, angle
    return angle,distance


outputcursor=arcpy.da.InsertCursor(outputFC,["SHAPE@","Angle","Distance"])

with arcpy.da.SearchCursor(inputFC,"SHAPE@") as cursor:
    for row in cursor:
        x=row[0][0].X
        y=row[0][0].Y
        a,d=calculate(x,y)
        print a,d
        p=arcpy.Point(x,y)
        list=[p,a,d]
        outputcursor.insertRow((p,a,d))
        #outputcursor.insertRow()
        #outputcursor.insertRow()


        
        


print "Successfully completed"
