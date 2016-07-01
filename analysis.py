import pandas
import numpy
import MySQLdb
import datetime
from firebase import firebase
from pprint import pprint
import re
import traceback


def getCompanyName(website):
	dot1 = website.index('.') +1
	dot2 = website.index('.',dot1)
	return website[dot1:dot2]

def daysData(df, day):
	return df[df['PostingDate'] >= currDate - datetime.timedelta(days = day)]

def generalData(df):
	gen = {}
	gen['min'] = df.describe()['Price']['min']
	gen['max'] = df.describe()['Price']['max']
	gen['avg'] = df.describe()['Price']['mean']
	gen['count'] = df.describe()['Price']['count']
	# gen['std'] = df.describe()['Price']['std']
	gen['median'] = df.describe()['Price']['50%']
	gen['25%'] = df.describe()['Price']['25%']
	gen['75%'] = df.describe()['Price']['75%']
	return gen

def webLevelAnalysis(dataFrame):
	websites = list(set(dataFrame['Website']))
	webObject = {}
	for website in websites:
		websiteFrame = dataFrame[dataFrame['Website'] == website]
		webObject[getCompanyName(website)] = generalData(websiteFrame)

	return webObject

def areaLevelAnalysis(bhkFrame):
	areas = list(set(bhkFrame['SuperBuiltupArea']))
	sizeObject = {}
	for area in areas :
		sizeFrame = bhkFrame[bhkFrame['SuperBuiltupArea'] == area]
		
		obj = {'gen':generalData(sizeFrame)}
		
		obj['website'] = webLevelAnalysis(sizeFrame)
		sizeObject[str(int(area))] = obj

	return sizeObject

def BHKLevelAnalysis(dataFrame):
	bhk_list = list(set(dataFrame['Bedrooms']))
	bhkObject = {}
	SegmentObj = {}
	bhkDeepObject = {}
	for bhk in bhk_list:
		bhkFrame = dataFrame[dataFrame['Bedrooms'] == bhk]
		
		bhkDeepObject['gen'] = generalData(bhkFrame)
		bhkDeepObject['sizes'] = areaLevelAnalysis(bhkFrame)
		bhkDeepObject['website'] = webLevelAnalysis(bhkFrame)

		bhkObject[str(bhk)] = bhkDeepObject

	SegmentObj['gen'] = generalData(dataFrame)
	SegmentObj['bhk'] = bhkObject
	SegmentObj['website'] = webLevelAnalysis(dataFrame)
	return SegmentObj

def segmentLevelAnalysis(df, no_of_days):
	daysObj = {}
	SegmentObj = {}
	for days in no_of_days:
		dayDF = daysData(df,days)
		if not dayDF.empty:
			daysObj[str(days)] = BHKLevelAnalysis(dayDF)
	
	if daysObj:
		SegmentObj['days'] = daysObj
		SegmentObj['gen'] = generalData(df)
		SegmentObj['website'] = webLevelAnalysis(df)
	return SegmentObj

def projectLevelAnalysis(dataFrame, projects, days):
	projectObj = {}
	for project in projects:
		try :
			df = dataFrame[dataFrame['ProjectName'] == project]
			project = re.sub(r'[^\x00-\x7F]'," ",project) # replacing non non ascii with blank spaces
			segmentLevelData = segmentLevelAnalysis(df, days)
			if segmentLevelData:
				projectObj[project.replace('/','').replace('.','').replace('#','')] = segmentLevelData
		except:
			print traceback.print_exc()	
	return projectObj	


if __name__ == "__main__":
	# connection establishment
	cnx = MySQLdb.connect("localhost", "root", "123456", "99acres")
	cursor = cnx.cursor()

	dfTotal = pandas.read_sql('''SELECT * FROM total ''',cnx)
	dfProject = pandas.read_sql('''SELECT * FROM Project ''',cnx)

	# connection closing from MYSQL
	cnx.commit()
	cursor.close()
	cnx.close()

	# today's Date
	currDate = datetime.date.today()
	days = [7,15,30,60]

	# projects contain list of distinct project name
	projects = list(dfProject['projectName'])
	print "Analysis start..."
	# projectObj store object of all project
	analysis= projectLevelAnalysis(dfTotal, projects, days)
	print "Analysis end"
	pprint(analysis)
	print "Firebase start"
	firebase1 = firebase.FirebaseApplication('https://analysis-70c53.firebaseio.com/',None)
	print firebase1.put('/data/',currDate.isoformat(),analysis)
