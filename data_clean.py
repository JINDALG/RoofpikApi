import MySQLdb
import datetime
from pprint import pprint

if __name__ == "__main__":
	# connection establishment
	cnx = MySQLdb.connect("localhost", "root", "123456", "99acres")
	cursor = cnx.cursor()

	# Triming of spaces from left and right
	cursor.execute('''UPDATE Data set ProjectName= LTRIM(RTRIM(ProjectName))''')
	cursor.execute('''UPDATE MagicData set ProjectName= LTRIM(RTRIM(ProjectName))''')
	cursor.execute('''UPDATE Data set City= LTRIM(RTRIM(City))''')
	cursor.execute('''UPDATE MagicData set City= LTRIM(RTRIM(City))''')

	# convert projectName to lowerCase
	cursor.execute('''UPDATE Data SET ProjectName = LOWER(ProjectName)''')
	cursor.execute('''UPDATE MagicData SET ProjectName = LOWER(ProjectName)''')
	cursor.execute('''UPDATE Data SET City = LOWER(City)''')
	cursor.execute('''UPDATE MagicData SET City = LOWER(City)''')

	# Fill superBuiltArea with carpetArea where superBuiltArea not given
	cursor.execute('''UPDATE MagicData SET SuperBuiltupArea = CarpetArea WHERE SuperBuiltupArea = -1''')
	cursor.execute('''UPDATE Data SET SuperBuiltupArea = CarpetArea WHERE SuperBuiltupArea = -1''')

	# remove data where size is not given
	cursor.execute('''DELETE FROM MagicData WHERE SuperBuiltupArea = -1 and CarpetArea=-1''')
	cursor.execute('''DELETE FROM Data WHERE SuperBuiltupArea = -1 and CarpetArea=-1''')

	# push distinct project details in project table
	cursor.execute('''INSERT IGNORE INTO Project (projectName,source,city) SELECT ProjectName, Website, City FROM `MagicData` GROUP BY ProjectName, Website, City''')
	cursor.execute('''INSERT IGNORE INTO Project (projectName,source,city) SELECT ProjectName, Website, City FROM `Data` GROUP BY ProjectName, Website, City''')

	# push all data in total table
	cursor.execute(''' INSERT INTO total SELECT * FROM Data ''')
	cursor.execute(''' INSERT INTO total SELECT * FROM MagicData ''')


	cnx.commit()
	cursor.close()
	cnx.close()