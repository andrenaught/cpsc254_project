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
inv_main = Inventory("Inventory Manager", "inv_GUI.glade")

### login System ###
#signal handling
button = inv_main.builder.get_object("submit_input")
button.connect("clicked", inv_main.on_login_submit)

### User Dashboard ###
#log_out = inv_main.builder.get_object("log_out")

### start GUI ###
#start at log in window
inv_main.login_win.show_all()


# TESTING
inv_main.open_user_window()
Gtk.main()

#close the db connection
inv_main.mysql.close_db()