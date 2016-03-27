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
