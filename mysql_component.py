#!/usr/bin/python3
##### MySQL #####
import pymysql

#change the password to whichever password u have
sql_password = "password123"

##### MySQL Class #####
# This class handles mySQL data usage for the Inventory class in inv_main.py
class SQL_handler:

	def __init__(self):
		#setup db + cursor
		global sql_password
		self.db = pymysql.connect(host='localhost', user='root', password=sql_password, db='inventory')
		self.cursor = self.db.cursor()

	#checks if username & password are valid
	#returns data if login successful, false if unsuccessful
	def login_check(self, username, password):
		sql = "SELECT * FROM user_table WHERE username = '" + str(username) + "'"
		print(sql)

		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			
			if (len(results) == 1):
				print("found user -> " + str(username))
				found_user = results[0]
				found_password = found_user[2]
				if (password == found_password):
					print("correct password")
				else:
					print("incorrect Password")

				print(found_password)
				return found_user
			else:
				#display message
				#display_message("incorrect username")
				print("incorrect Username")
				return False
			
		except:
			print("ERR: couldn't access user table")
			return False

	def close_db(self):
		self.db.close()

