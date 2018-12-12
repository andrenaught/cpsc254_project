##### UI #####
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mysql_component import SQL_handler #SQL_handler class

import csv

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
		self.inv_manage_grid = None
		self.logged_in_user = {'username': None, 'password': None}

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

		#temp window (inventory manager)
		self.inv_manage_win = self.builder.get_object("inventory_manager_window")
		self.inv_manage_win.set_title("Inventory Manager")
		#self.inv_manage_win.connect("destroy", Gtk.main_quit) #close window button

		#temp window (inventory item editor)
		self.inv_item_edit_win = self.builder.get_object("inv_edit_window")
		self.inv_item_edit_win.set_title("Item Editor")

		#temp window (feedback notice window)
		self.add_new_item_win = self.builder.get_object("add_new_item_window")
		#self.add_new_item_win.connect("destroy", self.destroy_me) #close window button


		#temp window (feedback notice window)
		self.feedback_win = self.builder.get_object("feedback_window")

	### signal handlers ###
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

		if (result == "incorrect_username"):
			feedback_message = self.builder.get_object("feedback_message")
			feedback_message.set_text("Username not found.")
			feedback_button = self.builder.get_object("close_feedback_window")
			feedback_button.connect("clicked", self.close_feedback_message)

			self.feedback_win.show()
		elif (result == "incorrect_password"):
			feedback_message = self.builder.get_object("feedback_message")
			feedback_message.set_text("Incorrect Password.")
			feedback_button = self.builder.get_object("close_feedback_window")
			feedback_button.connect("clicked", self.close_feedback_message)

			self.feedback_win.show()
		else:
			print ("log em in!")
			self.logged_in_user['username'] = username
			self.logged_in_user['password'] = password
			self.open_user_window()

	#create dynamic UI for the inventory since its data is dynamic
	def on_manage_inventory_click(self, widget=None, action=None):
		print("welcome to the inventory manager")
		#self.inv_manage_win.show()

		if (action=="reset" or self.inv_manage_grid!=None):
			print('asd')
			the_grid = self.inv_manage_grid
			print(the_grid)
			self.inv_manage_grid.destroy()

		#get the data
		table_data = self.mysql.get_inv_table()

		#setup the core UI
		self.inv_manage_grid = Gtk.Grid()
		self.inv_manage_grid.set_name("inv_manager_grid")
		self.inv_manage_grid.set_css_name("inv_manager_grid")
		#self.builder.expose_object("inv_manager_grid", grid)
		self.inv_manage_grid.set_row_spacing(15)
		self.inv_manage_grid.set_column_spacing(15) #padding so it looks nice

		#first row
		name_label = Gtk.Label(label="Name")
		desc_label = Gtk.Label(label="Desc")
		price_label = Gtk.Label(label="Price")
		stock_label = Gtk.Label(label="Stock")
		public_label = Gtk.Label(label="Public")
		date_label = Gtk.Label(label="Date Added")

		self.inv_manage_grid.add(name_label)
		self.inv_manage_grid.add(desc_label)
		self.inv_manage_grid.add(price_label)
		self.inv_manage_grid.add(stock_label)
		self.inv_manage_grid.add(public_label)
		self.inv_manage_grid.add(date_label)

		#last row's initial item, we'll use this to align the rows properly
		last_rows_leftest = name_label

		#put data in a grid UI
		#print(table_data)
		count = 0
		#this array will be used to keep track of which items will be edited
		button_array = {}
		for row in table_data:
			ID = row[0]
			name = row[1]
			desc = row[2]
			price = row[3]
			stock = row[4]
			is_public = row[5]
			reg_date = row[6]

			name_label = Gtk.Label(label=row[1])
			desc_label = Gtk.Label(label=row[2])
			price_label = Gtk.Label(label=row[3])
			stock_label = Gtk.Label(label=row[4])
			public_label = Gtk.Label(label=row[5])
			date_label = Gtk.Label(label=row[6])

			edit_button = Gtk.Button(label="Edit")
			#button_array.update({str(ID):edit_button})

			#manage_inv = self.builder.get_object("manage_inventory_button")
			edit_button.connect("clicked", self.edit_inv_item, ID)


			#creates new row
			self.inv_manage_grid.attach_next_to(name_label, last_rows_leftest, Gtk.PositionType.BOTTOM, 1, 2)
			self.inv_manage_grid.attach_next_to(desc_label, name_label, Gtk.PositionType.RIGHT, 1, 1)
			self.inv_manage_grid.attach_next_to(price_label, desc_label, Gtk.PositionType.RIGHT, 1, 1)
			self.inv_manage_grid.attach_next_to(stock_label, price_label, Gtk.PositionType.RIGHT, 1, 1)
			self.inv_manage_grid.attach_next_to(public_label, stock_label, Gtk.PositionType.RIGHT, 1, 1)
			self.inv_manage_grid.attach_next_to(date_label, public_label, Gtk.PositionType.RIGHT, 1, 1)
			self.inv_manage_grid.attach_next_to(edit_button, date_label, Gtk.PositionType.RIGHT, 1, 1)


			#setup positioning for next row
			last_rows_leftest = name_label
			count+1



		table = self.builder.get_object("table1")
		self.inv_manage_win.add(self.inv_manage_grid)
		print("asd")
		print(self.inv_manage_win.find_child_property("inv_manager_grid"))

		#self.inv_manage_grid = grid
		#show it
		self.inv_manage_win.show_all()
		
	def on_add_new_item_click(self, widget=None):
		print("welcome to add new item window")
		print(self.builder.get_object("label8").get_text())

		name_input = self.builder.get_object("new_item_name_input")
		desc_input = self.builder.get_object("new_item_desc_input")
		price_input = self.builder.get_object("new_item_price_input")
		stock_input = self.builder.get_object("new_item_stock_input")
		is_public_input = self.builder.get_object("new_item_is_public_input")

		#set rules for numeric input
		stock_input.set_range(0, 1000)
		stock_input.set_increments(step=1.00, page=2.00)
		price_input.set_range(0, 1000)
		price_input.set_increments(step=0.50, page=1.00)

		#reset default input values
		name_input.set_text("")
		desc_input.set_text("")
		price_input.set_value(0.00)
		stock_input.set_value(0)
		is_public_input.set_active(False)

		#setup signal for submit button
		add_item_button = self.builder.get_object("confirm_new_item_button")
		#delete old signal, this caused bug where item was made multiple times if user pressed cancel
		try:
			add_item_button.disconnect_by_func(self.confirm_new_item)
			print("resetted signal")
		except:
			print("no need")
		add_item_button.connect("clicked", self.confirm_new_item, name_input, desc_input, price_input, stock_input, is_public_input)

		#setup signal for cancel button
		cancel_button = self.builder.get_object("new_item_cancel_button")
		cancel_button.connect("clicked", self.cancel_me, self.add_new_item_win)

		self.add_new_item_win.show_all()


	#closing out of the temp windows caused a bug where it would be blank next time we opened it, this way gives us more control
	def cancel_me(self, widget, window):
		window.hide()

	### action functions ###

	#after user logs in, this leads them to the user window		
	def open_user_window(self):
		print ("welcome to the user dashboard")	
		self.login_win.hide()
		self.user_dash_win.show()
		#self.login_win.unrealize()

		#show user info in dashboard
		dashboard_user_info = self.builder.get_object("dashboard_user_info")
		dashboard_user_info.set_text("Welcome " + str(self.logged_in_user['username']))

		#setup signals for logged in user
		log_out = self.builder.get_object("menu_logout")
		log_out.connect("button-press-event", self.log_me_out)

		#open manage inventory window
		manage_inv = self.builder.get_object("manage_inventory_button")
		manage_inv.connect("clicked", self.on_manage_inventory_click)

		#open add new item window
		add_new_item = self.builder.get_object("add_new_item_button")
		add_new_item.connect("clicked", self.on_add_new_item_click)

		#download csv
		order_sheet = self.builder.get_object("order_sheet_button")
		order_sheet.connect("clicked", self.download_orders)

		#add new order
		#add_new_order = self.builder.get_object("make_transaction_button")
		#add_new_order.connect("clicked", self.on_add_new_transaction)


	#download csv of orders table
	def download_orders(self, widget):
		data = self.mysql.get_orders_table()
		#print(data)
		data_arr = []
		for row in data:
			product_name = self.mysql.get_item(row[1])
			row = list(row)
			row[1] = product_name[0][1]
			temp = row

			data_arr.append(temp)


		#print(data_arr)
		with open('order_list.csv', 'w') as f:
			writer = csv.writer(f)
			#writer.writerow(['Column 1', 'Column 2'])
			#for h in data_arr:
			writer.writerows(data_arr)


	#log the current user out
	def log_me_out(self, widget, event):
		print("logging you out")
		self.login_win.show()
		self.user_dash_win.hide()

		#remove user info
		self.logged_in_user = {'username': None, 'password': None}

		#reset values
		username_obj = self.builder.get_object("username_input")
		password_obj = self.builder.get_object("password_input")

		username_obj.set_text("")
		password_obj.set_text("")

	#edit an inventory item
	#ID - the id of the item you wan't to edit
	def edit_inv_item(self, widget, ID):
		item_data = self.mysql.get_item(ID)
		first_found = item_data[0]

		ID = first_found[0]
		name = first_found[1]
		desc = first_found[2]
		price = first_found[3]
		stock = first_found[4]
		is_public = first_found[5]

		#open edit_window
		self.inv_item_edit_win.show()

		name_input = self.builder.get_object("inv_edit_name")
		desc_input = self.builder.get_object("inv_edit_desc")
		price_input = self.builder.get_object("inv_edit_price")
		stock_input = self.builder.get_object("inv_edit_stock")
		is_public_input = self.builder.get_object("inv_edit_is_public")

		#set rules for numeric input
		stock_input.set_range(0, 1000)
		stock_input.set_increments(step=1.00, page=2.00)
		price_input.set_range(0, 1000)
		price_input.set_increments(step=0.50, page=1.00)

		#set default input values
		name_input.set_text(name)
		desc_input.set_text(desc)
		price_input.set_value(price)
		stock_input.set_value(stock)
		is_public_input.set_active(bool(is_public))

		#setup signal for update button
		edit_item_button = self.builder.get_object("confirm_edit_item")
		#delete old signal, this caused bug where item was made multiple times if user pressed cancel
		try:
			edit_item_button.disconnect_by_func(self.confirm_edit_item)
			print("resetted signal")
		except:
			print("no need")
		edit_item_button.connect("clicked", self.confirm_edit_item, ID, name_input, desc_input, price_input, stock_input, is_public_input)

		#setup signal for delete button
		cancel_button = self.builder.get_object("confirm_delete_item")
		#delete old signal, this caused bug where item was made multiple times if user pressed cancel
		try:
			cancel_button.disconnect_by_func(self.delete_item)
			print("resetted signal")
		except:
			print("no need")
		cancel_button.connect("clicked", self.delete_item, ID)

		#setup signal for cancel button
		cancel_button = self.builder.get_object("inv_edit_cancel_button")
		cancel_button.connect("clicked", self.cancel_me, self.inv_item_edit_win)

		#result = self.mysql.edit_item(ID, password)
		print("editing item: " + str(ID))

	#delete item in mySQL inventory table
	def delete_item(self, widget, ID):
		result = self.mysql.delete_item(ID)

		self.inv_item_edit_win.hide()

		#reset inventory manager
		self.inv_manage_win.hide()
		self.on_manage_inventory_click(action='reset')

	#update item in mySQL inventory table
	def confirm_edit_item(self, widget, ID, name, desc, price, stock, is_public):
		name = name.get_text()
		desc = desc.get_text()
		price = price.get_value()
		stock = stock.get_value()
		is_public = is_public.get_active()
		update_list = {'name': name, 'desc': desc, 'price': float(price), 'stock': int(stock), 'is_public': int(is_public)}
		print(update_list)
		result = self.mysql.edit_item(ID, update_list)

		#close 'edit item' window
		self.inv_item_edit_win.hide()

		#reset inventory manager
		self.inv_manage_win.hide()
		self.on_manage_inventory_click(action='reset')


	#add new item to mySQL inventory table
	def confirm_new_item(self, widget, name, desc, price, stock, is_public):
		name = name.get_text()
		desc = desc.get_text()
		price = price.get_value()
		stock = stock.get_value()
		is_public = is_public.get_active()
		update_list = {'name': name, 'desc': desc, 'price': float(price), 'stock': int(stock), 'is_public': int(is_public)}
		print(update_list)
		result = self.mysql.add_item(update_list)

		#close 'new item' window
		self.add_new_item_win.hide()

		#open the inventory manager
		self.on_manage_inventory_click()


	#closes the feedback notice window
	def close_feedback_message(self, widget):
		self.feedback_win.hide()
