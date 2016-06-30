import pandas
import numpy
import MySQLdb
import datetime
from firebase import firebase
from pprint import pprint


def daysData(df, day):
	
	return df[df['PostingDate'] >= currDate - datetime.timedelta(days = day)]

def generalData(df):
	gen = {}
	gen['min'] = df.describe()['Price']['min']
	gen['max'] = df.describe()['Price']['max']
	gen['avg'] = df.describe()['Price']['mean']
	gen['count'] = df.describe()['Price']['count']
	gen['std'] = df.describe()['Price']['std']
	gen['median'] = df.describe()['Price']['50%']
	gen['25%'] = df.describe()['Price']['25%']
	gen['75%'] = df.describe()['Price']['75%']
	return gen

def areaLevelAnalysis(bhkFrame):
	areas = list(set(bhkFrame['SuperBuiltupArea']))
	sizeObject = {}
	for area in areas :
		sizeFrame = bhkFrame[bhkFrame['SuperBuiltupArea'] == area]
		websites = list(set(sizeFrame['Website']))
		obj = {'gen':generalData(sizeFrame)}
		webObject = {}
		for website in websites:
			websiteFrame = sizeFrame[sizeFrame['Website'] == website]
			webObject[website] = generalData(websiteFrame)
		obj['website'] = webObject
		sizeObject[str(area)] = obj

	return sizeObject

def BHKLevelAnalysis(segmentDF, bhk_list):
	SegmentObj = {'gen':generalData(segmentDF)}
	for bhk in bhk_list:
		bhkFrame = segmentDF[segmentDF['Bedrooms'] == bhk]
		
		sizeObject = areaLevelAnalysis(bhkFrame)

		bhkObject = {'gen':generalData(bhkFrame)}
		bhkObject['sizes'] = sizeObject

		SegmentObj[str(bhk)+"bhk"] = bhkObject

	return SegmentObj

def segmentLevelAnalysis(df, no_of_days):
	segmentDF = daysData(df,no_of_days)

	# bhk contains set of bedrooms
	bhk_list = list(set(segmentDF['Bedrooms']))
	
	return { str(no_of_days)+'days' : BHKLevelAnalysis(segmentDF, bhk_list)}

def projectLevelAnalysis(dataFrame, projects, days):
	projectObj = {}
	for project in projects[:50]:
		try :
			df = dataFrame[dataFrame['ProjectName'] == project]
			projectObj[project] = segmentLevelAnalysis(df, days)
		except:
			pass	
	return projectObj	


if __name__ == "__main__":
	# connection establishment
	cnx = MySQLdb.connect("localhost", "root", "123456", "99acres")
	cursor = cnx.cursor()

	dfTotal = pandas.read_sql('''SELECT * FROM total ''',cnx)
	dfProject = pandas.read_sql('''SELECT * FROM Project ''',cnx)

	# today's Date
	currDate = datetime.date.today()
	days = 120

	# projects contain list of distinct project name
	projects = list(dfProject['projectName'])
	analysis = {}

	# projectObj store object of all project
	analysis[currDate.isoformat()] = projectLevelAnalysis(dfTotal, projects, days)
	
	pprint(analysis)
	
	cnx.commit()
	cursor.close()
	cnx.close()



# if __name__ == "__main__":
# 	# connection establishment
# 	cnx = MySQLdb.connect("localhost", "root", "123456", "99acres")
# 	cursor = cnx.cursor()

# 	# current data
# 	currDate = datetime.date.today()

# 	dfTotal = pandas.read_sql('''SELECT * FROM total ''',cnx)
# 	dfProject = pandas.read_sql('''SELECT * FROM Project ''',cnx)

# 	# projects contain list of distinct project name
# 	projects = list(dfProject['projectName'])
# 	analysis = {currDate.isoformat() : {}}

# 	# projectObj store object of all project
# 	projectObj = analysis[currDate.isoformat()]
# 	for project in projects[:50]:
# 		try :
# 			df = dfTotal[dfTotal['ProjectName'] == project]
# 			# segment dataFrame
# 			segmentDF = daysData(df,120)
# 			# object of general details
# 			gen = generalData(segmentDF)
# 			SegmentObj = {'gen':gen}
# 			bhk = list(set(segmentDF['Bedrooms']))
# 			for each in bhk:
# 				bhkFrame = segmentDF[segmentDF['Bedrooms'] == each]
				
# 				sizes = list(set(bhkFrame['SuperBuiltupArea']))
# 				sizeObject = {}

# 				for size in sizes :
# 					sizeFrame = bhkFrame[bhkFrame['SuperBuiltupArea'] == size]
# 					websites = list(set(sizeFrame['Website']))
# 					obj = {'gen':generalData(sizeFrame)}
# 					webObject = {}
# 					for website in websites:
# 						websiteFrame = sizeFrame[sizeFrame['Website'] == website]
# 						webObject[website] = generalData(websiteFrame)
# 					obj['website'] = webObject
# 					sizeObject[str(size)] = obj
# 				bhkObject = {'gen':generalData(bhkFrame)}
# 				bhkObject['sizes'] = sizeObject
# 				SegmentObj[str(each)+"bhk"] = bhkObject

# 			sectionObj = {'7days' : SegmentObj}
# 			projectObj[project] = sectionObj
# 		except:
# 			pass		
# 	pprint(analysis)
	
# 	cnx.commit()
# 	cursor.close()
# 	cnx.close()
