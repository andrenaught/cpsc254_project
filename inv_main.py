##### UI #####
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mysql_component import SQL_handler #SQL_handler class

##### Inventory Class #####
# This handles the logic between the GUI and the data from mySQL
class Inventory:
	### setup variables ###

	#UI
	builder = Gtk.Builder()

	#mySQL
	#db = pymysql.connect(host='localhost', user='root', password='password123', db='inventory')
	mysql = SQL_handler()

	#init
	def __init__(self, title, glade, window):
		self.title = title

		#builder
		#self.builder = Gtk.Builder()
		self.builder.add_from_file(glade)

		#window
		self.window = self.builder.get_object(window)
		self.window.set_title(title)
		self.window.connect("destroy", Gtk.main_quit) #close window button

	#signal handlers
	def on_login_submit(self, widget):
		#print(username)
		#print(password)
		username_obj = self.builder.get_object("username_input")
		password_obj = self.builder.get_object("password_input")
		username = username_obj.get_text()
		password = password_obj.get_text()
		print ("logging in with credentials: ")
		print ("USERNAME: " + str(username))
		print ("PASSWORD: " + str(password))
		self.mysql.login_check(username, password)
	