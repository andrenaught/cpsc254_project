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
	def __init__(self, title, glade):
		self.title = title

		#builder
		#self.builder = Gtk.Builder()
		self.builder.add_from_file(glade)

		#window
		self.login_win = self.builder.get_object("login_window")
		self.login_win.set_title("login window")
		self.login_win.connect("destroy", Gtk.main_quit) #close window button

		#window 2
		self.user_dash_win = self.builder.get_object("user_dashboard_window")
		self.user_dash_win.set_title("user dashboard")
		self.user_dash_win.connect("destroy", Gtk.main_quit) #close window button

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
		result = self.mysql.login_check(username, password)

		if (result != False):
			print ("log em in!")
			self.open_user_window()

	#after user logs in, this leads them to the user window		
	def open_user_window(self):
		print ("welcome to the user dashboard")	
		self.user_dash_win.show()
		self.login_win.unrealize()
		#self.window.hide()

		#setup signals
		log_out = self.builder.get_object("menu_logout")
		log_out.connect("button-press-event", self.log_me_out)
		#print(log_out.get_text())

	def log_me_out(self, widget, event):
		print("logging you out")



	