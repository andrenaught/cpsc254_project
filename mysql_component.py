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

	#close the connection
	def close_db(self):
		self.db.close()

	#checks if username & password are valid
	#returns data if login successful, false if unsuccessful
	def login_check(self, username, password):
		sql = "SELECT * FROM user_table WHERE BINARY username = '" + str(username) + "'"
		print(sql)

		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			
			if (len(results) == 1):
				found_user = results[0]
				found_username = found_user[1]
				found_password = found_user[2]
				print("found user -> " + str(found_username))

				if (password == found_password):
					print("correct password")
					return found_user
				else:
					print("incorrect Password")
					return "incorrect_password"				
			else:
				#display message
				#display_message("incorrect username")
				print("incorrect Username")
				return "incorrect_username"
			
		except:
			print("ERR: couldn't access user table")
			return "SQL Error"

	#return an array of all the items from the inventory table
	def get_inv_table(self):
		sql = "SELECT * FROM inv_table"
		print(sql)

		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			return results							
		except:
			print("ERR: couldn't access user table")
			return False

	#get item data based on ID given
	def get_item(self, ID):
		sql = "SELECT * FROM inv_table WHERE id = " + str(ID)
		print(sql)

		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			return results							
		except:
			print("ERR: couldn't access user table")
			return False

	#edit item data based on ID given
	def edit_item(self, ID, data):
		name = data['name']
		desc = data['desc']
		price = data['price']
		stock = data['stock']
		public = data['is_public']

		sql = "UPDATE inv_table SET name = '"+str(name)+"', description='"+str(desc)+"', price="+str(price)+", stock="+str(stock)+", is_public="+str(public)+" WHERE id = " + str(ID)
		print(sql)

		try:
			self.cursor.execute(sql)
			self.db.commit()
			results = self.cursor.rowcount
			print(str(results) + "rows updated")
			return results							
		except:
			print("ERR: couldn't access inventory table")
			return False

	#add new item to database
	def add_item(self, data):
		name = data['name']
		desc = data['desc']
		price = data['price']
		stock = data['stock']
		public = data['is_public']


		sql = "INSERT INTO inv_table (name, description, price, stock, is_public) VALUES (%s,%s,%s,%s,%s)"
		val = (str(name), str(desc), str(price), str(stock), str(public))
		print(sql)
		print(val)

		try:
			self.cursor.execute(sql, val)
			self.db.commit()
			results = self.cursor.rowcount
			print(str(results) + "rows inserted")
			return results							
		except:
			print("ERR: couldn't access inventory table")
			return False

	#delete item from database
	def delete_item(self, ID):
		sql = "DELETE FROM inv_table WHERE id = " + str(ID)
		print(sql)

		try:
			self.cursor.execute(sql)
			self.db.commit()
			print(self.cursor.rowcount, "items deleted")
		except:
			print("ERR: couldn't access inventory table")
			return False
