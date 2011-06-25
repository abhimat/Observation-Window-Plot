from pylab import *
from math import *
from datetime import *
from matplotlib.pyplot import *

#### The date2julian function
#### Converts date to Julian date
#### Abhimat K Gautam
def date2julian(month, date, year, hours, minutes, seconds):
	JDate = 2451544.0
	for i in range(2000, year):
		if i % 4 == 0 and (i % 100 != 0 or i % 400 == 0):
			JDate += 366
		else:
			JDate += 365
	monthList = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	for i in range(1, month):
		JDate += monthList[i-1]
		if i == 2 and (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
			date += 1
	JDate += date
	JDate += (hours-12)/24. + minutes/1440. + seconds/86400.
	
	return JDate


#### The obsWindowPlot function
#### Plots sunrise, sunset, object rise, and object set times at the observatory between the specified datetimes
#### Abhimat K Gautam
def obsWindowPlot(startDate, finDate):
	objRA = 17.0 + 45.0/60.0 + 40.04/3600.0		# Target object's right ascension (h, m, s)
	objRADeg = objRA * 15
	objDec = -29.0 + 0.0/60.0 + 28.1/3600.0		# Target object's declination (degrees)
	
	obsLong = 79.0 + 50.0/60.0 + 23.406/3600.0	# Observatory's longitude (degrees West)
	obsLat = 38.0 + 25.0/60.0 + 59.236/3600.0	# Observatory's latitude (degrees North)
	
	## Sun data
	
	sunriseTimesX = []
	sunriseTimesY = []
	sunsetTimesX = []
	sunsetTimesY = []
	
	## Object data
	
	objriseTimesX = []
	objriseTimesY = []
	objsetTimesX = []
	objsetTimesY = []
	
	fillX1 = []
	fillY1 = []
	fillY2 = []
	fillX2 = []
	fillY3 = []
	fillY4 = []
	
	## Angular Separation Data
	angSepX = []
	angSepY = []
	
	objH = degrees(acos(-tan(radians(objDec)) * tan(radians(obsLat))))
	objRise = objRADeg - objH
	objSet = objRADeg + objH
	
	# print objRise
	# print objSet
	
	startJulDate = date2julian(startDate.month, startDate.day, startDate.year, startDate.hour, startDate.minute, startDate.second)
	finJulDate = date2julian(finDate.month, finDate.day, finDate.year, finDate.hour, finDate.minute, finDate.second)
	curDate = date2num(startDate)
	
	for curJulDay in range(int(startJulDate), int(finJulDate)):
		## Calculating sunrise and sunset times
		
		julCycle = round(curJulDay - 2451545.0 - 0.0009 - (obsLong/360.0))
		# print julCycle
		
		julDateNoonApp = 2451545.0 + 0.0009 + (obsLong/360.0) + julCycle
		# print julDateNoonApp
		
		meanSolarAnomaly = (357.5291 + 0.98560028 * (julDateNoonApp - 2451545.0)) % 360
		# print meanSolarAnomaly
		
		eqCenter = ((1.9148 * sin(radians(meanSolarAnomaly))) + (0.0200 * sin(radians(2 * meanSolarAnomaly))) +
			(0.0003 * sin(radians(3 * meanSolarAnomaly))))
		# print eqCenter
		
		ecLongSun = (meanSolarAnomaly + 102.9372 + eqCenter + 180) % 360
		# print ecLongSun
		
		julDateNoonAcc = (julDateNoonApp + (0.0053 * sin(radians(meanSolarAnomaly))) - 
			(0.0069 * sin(radians(2 * ecLongSun))))
		# print julDateNoonAcc
		
		sunDec = degrees(asin(sin(radians(ecLongSun)) * sin(radians(23.45))))
		# print sunDec
		
		hourAngle = degrees(acos((sin(radians(-0.83)) - sin(radians(obsLat)) * sin(radians(sunDec)))/
			(cos(radians(obsLat)) * cos(radians(sunDec)))))
		# print hourAngle
		
		julDateSetApp = 2451545.0 + 0.0009 + ((hourAngle + obsLong)/360.0) + julCycle
		# print julDateSetApp
		
		julDateSet = julDateSetApp + (0.0053 * sin(radians(meanSolarAnomaly))) - (0.0069 * sin(radians(2 * ecLongSun)))
		# print julDateSet
		
		julDateRise = julDateNoonAcc - (julDateSet - julDateNoonAcc)
		# print julDateRise
		
		riseUTC = (0.5 - (curJulDay - julDateRise)) * 24
		# print riseUTC
		
		setUTC = (0.5 - (curJulDay - julDateSet)) * 24
		# print setUTC
		
		## Storing sunrise and sunset values
		if riseUTC / 24.0 >= 1.0:
			sunriseTimesX.append(num2date(curDate + 1))
			sunriseTimesY.append(riseUTC % 24)
		else:
			sunriseTimesX.append(num2date(curDate))
			sunriseTimesY.append(riseUTC)
		
		if setUTC / 24.0 >= 1.0:
			sunsetTimesX.append(num2date(curDate + 1))
			sunsetTimesY.append(setUTC % 24)
		else:
			sunsetTimesX.append(num2date(curDate))
			sunsetTimesY.append(setUTC)
		
		noonUTC = (riseUTC + setUTC)/2
		
		## Object rise and set times
		
		objRiseUTC = (objRise - ecLongSun)/15 + noonUTC
		objSetUTC = (objSet - ecLongSun)/15 + noonUTC
		
		if objRiseUTC / 24.0 >= 1.0:
			objriseTimesX.append(num2date(curDate + 1))
			objriseTimesY.append(objRiseUTC % 24)
		else:
			objriseTimesX.append(num2date(curDate))
			objriseTimesY.append(objRiseUTC)
		
		if objSetUTC / 24.0 >= 1.0:
			objsetTimesX.append(num2date(curDate + 1))
			objsetTimesY.append(objSetUTC % 24)
		else:
			objsetTimesX.append(num2date(curDate))
			objsetTimesY.append(objSetUTC)
		
		# Data for filling visibility
		if objRiseUTC % 24 <= objSetUTC % 24:
			fillX1.append(num2date(curDate))
			fillY1.append(objRiseUTC % 24)
			fillY2.append(objSetUTC % 24)
		else:
			fillX1.append(num2date(curDate))
			fillY1.append(objRiseUTC % 24)
			fillY2.append(24)
			fillX2.append(num2date(curDate))
			fillY3.append(0)
			fillY4.append(objSetUTC % 24)
		
		## Angular Separation
		sunRA = (ecLongSun + (-2.468 * sin(radians(2 * ecLongSun))) + (0.053 * sin(radians(4 * ecLongSun))) +
			(-0.0014 * sin(radians(6 * ecLongSun))))
		# print sunRA
		
		angSep = degrees(acos(sin(radians(sunDec)) * sin(radians(objDec)) + cos(radians(sunDec)) * cos(radians(objDec)) *
			cos(radians(sunRA - objRADeg))))
		# print angSep
					
		angSepX.append(num2date(curDate))
		angSepY.append(angSep)
		
		curDate += 1
	
	### Plotting
	## The figure
	fig = figure()
	
	## The rise and set plot
	ax1 = fig.add_subplot(121)
	ax1.plot_date(sunriseTimesX, sunriseTimesY, xdate = True, ydate = False, fmt = 'o', color = '#eda802', label = 'Sunrise')
	ax1.plot_date(sunsetTimesX, sunsetTimesY, xdate = True, ydate = False, fmt = 'o', color = '#5995fa', label = 'Sunset')
	ax1.plot_date(objriseTimesX, objriseTimesY, xdate = True, ydate = False, fmt = '.', color = '#eda802', label = 'Object Rise')
	ax1.plot_date(objsetTimesX, objsetTimesY, xdate = True, ydate = False, fmt = '.', color = '#5995fa', label = 'Object Set')
	
	# Filling
	ax1.fill_between(fillX1, fillY1, fillY2, facecolor = '#b8b8b8')
	ax1.fill_between(fillX2, fillY3, fillY4, facecolor = '#b8b8b8')
	
	ax1.set_xlabel('Date')
	ax1.set_ylabel('Time (UTC)')
	ax1.set_ylim(ymax=24)
	ax1.set_title('Galactic Center Visibility and Sun Rise/Set')
	
	legend()
	yticks(arange(0, 28, 4))
	
	## The angular separation plot
	ax2 = fig.add_subplot(122)
	ax2.plot_date(angSepX, angSepY, xdate = True, ydate = False, fmt = 'o', color = 'gray')
	ax2.set_xlabel('Date')
	ax2.set_ylabel('Angular Separation (Degrees)')
	ax2.set_title('Galactic Center and Sun Angular Separation')
	
	show()
	
	return 1
	
#### Testing the obsWindowPlot function
print obsWindowPlot(datetime(2011, 9, 1), datetime(2012, 5, 31))