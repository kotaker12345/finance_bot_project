import sqlite3
import time

from pprint import pprint


class WorkDB():
	def __init__(self, db_path="finaces.db"):
		self.database = db_path
		self.conn = sqlite3.connect(db_path)
		self.data_creation() 
		

	def data_creation(self):	
		with self.conn as con:
			con.execute("""
				CREATE TABLE IF NOT EXISTS expenses( 
					id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					type VARCHAR(30),
					amount DECIMAL(30,2) NOT NULL,
					timestamp FLOAT NOT NULL
				)
			""")
			
			con.execute("""
				CREATE TABLE IF NOT EXISTS goals( 
					id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					name VARCHAR(30),
					balance DECIMAL(30,2) NOT NULL,
					amount DECIMAL(30,2) NOT NULL,
					timestamp FLOAT NOT NULL
				)
			""")

	def add_expenses(self, expenses_type, amount, timestamp):
		
		with self.conn as con:
			sql = 'INSERT INTO expenses (`type`, `amount`, `timestamp`) VALUES (?,?,?)'
			sql_data = [expenses_type, float(amount), timestamp]
			con.execute(sql, sql_data)
			con.commit()
			
	def get_expenses(self, amount, offset=0):

		with self.conn as con:
			sql = 'SELECT * FROM expenses LIMIT ?, ?';
			sql_data = [offset, amount]
			t = con.execute(sql, sql_data)
			TABLE = []
			for x in t:
				TABLE.append(dict(id=x[0], type=x[1], amount=x[2], timestamp=x[3]))
		return TABLE
		
		
	def get_current_month_expenses(self, current_month):
		with self.conn as con:
			sql = 'SELECT * FROM expenses WHERE (timestamp >= ?)'
			sql_data = [current_month]
			t = con.execute(sql, sql_data)
			
			TABLE = []
			for x in t:
				TABLE.append(dict(id=x[0], type=x[1], amount=x[2], timestamp=x[3]))
		return TABLE
	
	
	

def main():
	dataBase = WorkDB()
	
	
if __name__ == "__main__":
	main()