#_*_coding:utf-8_*_
import arcpy
import os
import math
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

arcpy.env.workspace = "D:\\code\\czx"
outPath = "D:\\code\\czx"
file = "cz36.shp"

desc = arcpy.Describe(file)
shapename = desc.ShapeFieldName
srs = desc.spatialReference

#获取xy坐标
def getXYcoord(file):
	arcpy.AddField_management("D:\\code\\czx\\cz36.shp","XZB","DOUBLE",12,4)
	arcpy.AddField_management("D:\\code\\czx\\cz36.shp","YZB","DOUBLE",12,4)

	rows = arcpy.da.UpdateCursor(file, ["SHAPE@XY","XZB","YZB"])
	for row in rows:
		print row[0]
		row[1] = row[0][0]
		row[2] = row[0][1]
		rows.updateRow(row)
	del row, rows

#度转弧度 等同于math.radians()
def duTohd(values):

	hd = values * (2 * math.pi / 360)

	return hd

def getValues(file):
	itemlist = []
	valuesList = []
	rows = arcpy.SearchCursor(file)
	for row in rows:
		idvalue = row.getValue("ID")
		tybhvalue = row.getValue("TYBH")
		dcfh = row.getValue("DCFH")
		dcqx = row.getValue("DCQX")
		dcqj = row.getValue("DCQJ")
		pntx = row.getValue("XZB")
		pnty = row.getValue("YZB")

		zx = dcqx + 90

		spx = pntx + (2.5 * math.sin(math.radians(zx)))
		spy = pnty + (2.5 * math.cos(math.radians(zx)))

		epx = pntx + (2.5 * math.sin(math.radians(zx + 180)))
		epy = pnty + (2.5 * math.cos(math.radians(zx + 180)))


		qxxsx = pntx #倾向线起始位置X
		qxxsy = pnty #倾向线起始位置y
		qxxex = pntx + (1.5 * math.sin(math.radians(dcqx))) #倾向线终点位置X
		qxxey = pnty + (1.5 * math.cos(math.radians(dcqx)))	#倾向线终点位置Y

		zxxValue = "[" + str(spx) + "," + str(spy) + "]" + "," + "["  + str(epx) + "," + str(epy) + "]"
		zxxWkt = "LINESTRING" + "(" + str(spx) + " " + str(spy) + "," + str(epx) + " " + str(epy) + ")"
		qxxWKT = "LINESTRING" + "(" + str(qxxsx) + " " + str(qxxsy) + "," + str(qxxex) + " " + str(qxxey) + ")"

		itemlist.append(idvalue)
		itemlist.append(tybhvalue)
		itemlist.append(dcfh)
		itemlist.append(dcqx)
		itemlist.append(dcqj)
		itemlist.append(zxxWkt)
		itemlist.append(qxxWKT)
		# itemlist.append(spx)
		# itemlist.append(spy)
		# itemlist.append(epx)
		# itemlist.append(epy)

        


		valuesList.append(itemlist)
		itemlist = []#每组循环之后一定要记得清零

	del row,rows

	return valuesList
# getXYcoord(file)
def creatZxshp(outfile,values,spat_ref):
	# try:
	outshp = arcpy.CreateFeatureclass_management(outPath,outfile, "POLYLINE", "", "", "",spat_ref)
	arcpy.AddField_management(outshp,"XH","TEXT")
	arcpy.AddField_management(outshp,"TYBH","TEXT")
	arcpy.AddField_management(outshp,"DCFH","TEXT")
	arcpy.AddField_management(outshp,"DCQX","TEXT")
	arcpy.AddField_management(outshp,"DCQJ","TEXT")
	# except:
	# 	outshp = outPath+"/"+outName+".shp"
	cur = arcpy.InsertCursor(outshp)
	for value in values:
		row = cur.newRow()
		xhz = value[0]
		tybhz = value[1]
		dcfhz = value[2]
		dcqxz = str(value[3])
		dcqjz = str(value[4])
		wktStings = value[5]
		# stx = value[5]
		# sty = value[6]
		# endx = value[7]
		# endy = value[8]

		plGeometry = arcpy.FromWKT(wktStings)
		row.shape = plGeometry
		row.XH = xhz
		row.TYBH = tybhz
		row.DCFH = dcfhz
		row.DCQX = dcqxz
		# row.DCQJ = dcqjz

		cur.insertRow(row)

def creatQxshp(outfile,values,spat_ref):
	# try:
	outshp = arcpy.CreateFeatureclass_management(outPath,outfile, "POLYLINE", "", "", "",spat_ref)
	arcpy.AddField_management(outshp,"XH","TEXT")
	arcpy.AddField_management(outshp,"TYBH","TEXT")
	arcpy.AddField_management(outshp,"DCFH","TEXT")
	arcpy.AddField_management(outshp,"DCQX","TEXT")
	arcpy.AddField_management(outshp,"DCQJ","TEXT")
	# except:
	# 	outshp = outPath+"/"+outName+".shp"
	cur = arcpy.InsertCursor(outshp)
	for value in values:
		row = cur.newRow()
		xhz = value[0]
		tybhz = value[1]
		dcfhz = value[2]
		dcqxz = str(value[3])
		dcqjz = str(value[4])
		wktStings = value[6]
		# stx = value[5]
		# sty = value[6]
		# endx = value[7]
		# endy = value[8]

		plGeometry = arcpy.FromWKT(wktStings)
		row.shape = plGeometry
		row.XH = xhz
		row.TYBH = tybhz
		row.DCFH = dcfhz
		# row.DCQX = dcqxz
		row.DCQJ = dcqjz

		cur.insertRow(row)

vls = getValues(file)
creatZxshp("zxx",vls,srs)
creatQxshp("qxx",vls,srs)
print "ok"