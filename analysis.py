import pandas
import numpy
import MySQLdb
import datetime
from firebase import firebase
from pprint import pprint


def daysData(df, day):
	return df[df['PostingDate'] >= currDate-datetime.timedelta(days = day)]

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

if __name__ == "__main__":
	# connection establishment
	cnx = MySQLdb.connect("localhost", "root", "123456", "99acres")
	cursor = cnx.cursor()

	# current data
	currDate = datetime.date.today()

	dfTotal = pandas.read_sql('''SELECT * FROM total ''',cnx)
	dfProject = pandas.read_sql('''SELECT * FROM Project ''',cnx)

	# projects contain list of distinct project name
	projects = list(dfProject['projectName'])
	analysis = {currDate.isoformat() : {}}

	# projectObj store object of all project
	projectObj = analysis[currDate.isoformat()]
	for project in projects[:50]:
		try :
			df = dfTotal[dfTotal['ProjectName'] == project]
			# segment dataFrame
			sevenDayData = daysData(df,120)
			# object of general details
			gen = generalData(sevenDayData)
			SegmentObj = {'gen':gen}
			bhk = list(set(sevenDayData['Bedrooms']))
			for each in bhk:
				bhkFrame = sevenDayData[sevenDayData['Bedrooms'] == each]
				
				sizes = list(set(bhkFrame['SuperBuiltupArea']))
				sizeObject = {}

				for size in sizes :
					sizeFrame = bhkFrame[bhkFrame['SuperBuiltupArea'] == size]
					websites = list(set(sizeFrame['Website']))
					obj = {'gen':generalData(sizeFrame)}
					webObject = {}
					for website in websites:
						websiteFrame = sizeFrame[sizeFrame['Website'] == website]
						webObject[website] = generalData(websiteFrame)
					obj['website'] = webObject
					sizeObject[str(size)] = obj
				bhkObject = {'gen':generalData(bhkFrame)}
				bhkObject['sizes'] = sizeObject
				SegmentObj[str(each)+"bhk"] = bhkObject

			sectionObj = {'7days' : SegmentObj}
			projectObj[project] = sectionObj
		except:
			pass		
	pprint(analysis)
	
	cnx.commit()
	cursor.close()
	cnx.close()

