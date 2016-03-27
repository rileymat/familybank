

from database import get_db_connection

from money import Currency

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

def get_viewable_accounts(user_id):
	db = get_db_connection()
	c = db.cursor()
	c.execute("""SELECT a.account_id FROM accounts AS a JOIN account_permissions AS ap ON ap.account_id = a.account_id
                     JOIN permissions AS p ON p.permission_id = ap.permission_id WHERE ap.user_id = ? AND p.name = 'view'""",
				  (user_id, )
		);
	return [x["account_id"] for x in c.fetchall()]
