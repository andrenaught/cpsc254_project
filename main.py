##### IMPORTS #####
#gtk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#sql
import pymysql
#custom classes
from inv_main import Inventory #Inventory class, the main class
from mysql_component import SQL_handler #SQL_handler class

############### START ###############
inv_main = Inventory("Inventory Manager", "inv_GUI.glade", "window1")

#login UI
#signal handling
button = inv_main.builder.get_object("submit_input")
button.connect("clicked", inv_main.on_login_submit)

#start GUI
inv_main.window.show_all()
Gtk.main()

#close the db connection
inv_main.mysql.close_db()