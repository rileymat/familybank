

from database import get_db_connection

from money import Currency

def get_account_transactions(account_id):
	db = get_db_connection()
	c = db.cursor()
	c.execute("""SELECT ts.name as source, at.amount AS amount, tt.name AS type, at.timestamp AS timestamp, u.username AS transaction_user FROM account_transactions AS at
                 JOIN transaction_types AS tt ON tt.transaction_type_id = at.transaction_type_id
                 JOIN transaction_source as ts ON ts.source_id = at.source_id
	             LEFT JOIN account_transaction_user as atu ON at.transaction_id = atu.transaction_id
                 LEFT JOIN users as u ON u.user_id = atu.user_id
	             WHERE account_id = ? ORDER BY timestamp DESC""",(account_id, ))
	account_transactions = c.fetchall()
	for a in account_transactions:
		a["amount"] = Currency(a["amount"])
	return account_transactions

def get_account_permissions(user_id, account_id):
	db = get_db_connection()
	c = db.cursor()
	c.execute("""SELECT p.name from account_permissions AS ap
                 JOIN permissions as p ON p.permission_id = ap.permission_id
                 WHERE ap.account_id = ? AND ap.user_id = ?""",(account_id, user_id))
	permissions = c.fetchall()
	return [p["name"] for p in permissions]

def get_account_balance(account_id):
	db = get_db_connection()
	c = db.cursor()
	c.execute("""SELECT
                   SUM(CASE tt.positive WHEN 1 THEN at.amount ELSE 0 END) - SUM(CASE tt.positive WHEN 1 THEN 0 ELSE at.amount END) AS balance
                   FROM account_transactions AS at
                   JOIN transaction_types AS tt ON tt.transaction_type_id = at.transaction_type_id
                   WHERE at.account_id = ?
	          """, (account_id, ))
	return Currency(c.fetchall()[0]["balance"])
def get_account_name(account_id):
	db = get_db_connection()
	c = db.cursor()
	c.execute("""SELECT name FROM account_name WHERE account_id = ?""", (account_id, ))
	results = c.fetchall()
	print str(results[0]["name"])  + " " + str(len(results))
	result = results[0]["name"]
	print result
	return results[0]["name"] if len(results) == 1 else ""

def get_account_number(account_id):
	db = get_db_connection()
	c = db.cursor()
	c.execute("""SELECT account_number FROM accounts WHERE account_id = ?""", (account_id, ))
	return c.fetchall()[0]["account_number"]

def get_viewable_accounts(user_id):
	db = get_db_connection()
	c = db.cursor()
	c.execute("""SELECT a.account_id FROM accounts AS a JOIN account_permissions AS ap ON ap.account_id = a.account_id
                     JOIN permissions AS p ON p.permission_id = ap.permission_id WHERE ap.user_id = ? AND p.name = 'view'""",
				  (user_id, )
		);
	return [x["account_id"] for x in c.fetchall()]
