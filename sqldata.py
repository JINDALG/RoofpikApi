import MySQLdb
from pprint import pprint
def get_data(city):
	city = city.capitalize()
	city  = "%" + city + "%"
	cnx = MySQLdb.connect("localhost", "root", "123456", "99acres")
	cursor = cnx.cursor()
	# cursor.execute("SELECT * FROM Project Where city like %s" %(repr(city)))
	cursor.execute('''SELECT * FROM Project Where city like "''' + city +'''"''')
	columns = [desc[0] for desc in cursor.description]
	rows = cursor.fetchall()

	results = []
	for row in rows:
		row = dict(zip(columns, row))
		results.append(row)
	cnx.commit()
	cursor.close()
	cnx.close()

	# pprint(results)
	return results

def set_data(name,roofpikId):
	name  = name + "%"
	cnx = MySQLdb.connect("localhost", "root", "123456", "99acres")
	cursor = cnx.cursor()
	# cursor.execute("SELECT * FROM Project Where city like %s" %(repr(city)))
	result = {}
	try :
		cursor.execute('''UPDATE Project SET roofpikID = "''' + roofpikId + '''"''' + ''', flag = 1 Where projectName like "''' + name +'''"''')
		result['status'] = "Success"
	except :
		print "error"
		result['status'] = "fail"

	finally :
		cnx.commit()

		cursor.close()
		cnx.close()
	return result
# if __name__ == "__main__":
# 	get_data('gurgaon')