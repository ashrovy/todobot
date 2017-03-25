import sqlite3

class DBHelper:
	# __init__() takes a database name (by default store our data in a file called todo.sqlite) and creates a database connection.
	def __init__(self, dbname="lala.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)
	# setup() creates a new table called items in our database. This table has one column (called description)
	def setup(self):
		tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
		itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)" 
		ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
		self.conn.execute(tblstmt)
		self.conn.execute(itemidx)
		self.conn.execute(ownidx)
		# print("creating table")
		# stmt = "CREATE TABLE IF NOT EXISTS items(description text, owner text)"
		# self.conn.execute(stmt)
		self.conn.commit()
	# add_item() takes the text for the item and inserts it into our database table.
	def add_item(self, item_text, owner):
		stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
		args = (item_text, owner)
		self.conn.execute(stmt, args)
		self.conn.commit()
	# delete_item() takes the text for an item and removes it from the database
	def delete_item(self, item_text, owner):
		stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
		args = (item_text, owner )
		self.conn.execute(stmt, args)
		self.conn.commit()
	# get_items() returns a list of all the items in our database.
	def get_items(self, owner):
		stmt = "SELECT description FROM items WHERE owner = (?)"
		args = (owner, )
		return [x[0] for x in self.conn.execute(stmt, args)]
