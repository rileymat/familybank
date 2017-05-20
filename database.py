import sqlite3


def get_db_connection():
	db = sqlite3.connect('./bank.db')
	def dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d
	db.row_factory = dict_factory
	return db

def query_rows(query, params=None):
	db = get_db_connection()
	c = db.cursor()
	c.execute(query, params)
	return c.fetchall()

def query_row(query, params=None):
	rows = query_rows(query, params)
	number_of_rows = len(rows)
	if number_of_rows > 1:
		raise ValueError('More than one row returned')
	elif number_of_rows == 0:
		raise ValueError('No Rows');
	return rows[0]
