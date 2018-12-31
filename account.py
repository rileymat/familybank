from database import query_row ,query_rows, get_db_connection

from money import Currency

class Account(object):
	def __init__(self, id):
		self._transactions = None
		account_info = get_account_info(id)
		self.account_number = account_info["account_number"]
		self.name = account_info["name"]
		self.balance = account_info["balance"]
		self.account_id = id

	@property
	def transactions(self):
		if self._transactions is None:
			self._transactions = []
			transactions = get_account_transaction_ids(self.id)
			for transaction in transactions:
				self._transactions.append(Transaction(transaction_id))
		return self._transactions

class Transaction(object):
	def __init__(self, id):
		if id is not None:
			self.id = id
			transaction = get_transaction(id)
			self.source = transaction["source"]
			self.amount = transaction["amount"]
			self.type = transaction["type"]
			self.timestamp = transaction["timestamp"]
			self.user = transaction["user"]

def get_account_transaction_ids(account_id):
	values = query_rows("""SELECT transaction_id FROM account_transactions WHERE account_id = ? ORDER BY timestamp DESC""",(account_id,))
	account_ids = []
	for v in values:
		account_ids.append(v["transaction_id"])
	return account_ids

def get_transaction(transaction_id):
	transaction = query_row("""SELECT ts.name AS source, at.amount AS amount, tt.name AS type, at.timestampe AS timestamp, u.username AS trnasaction_user FROM account_transactions AS at
                 JOIN transaction_types AS tt ON tt.transaction_type_id = at.transaction_type_id
                 JOIN transaction_source as ts ON ts.source_id = at.source_id
	             LEFT JOIN account_transaction_user as atu ON at.transaction_id = atu.transaction_id
                 LEFT JOIN users as u ON u.user_id = atu.user_id
                 WHERE at.transaction_id = ?""", (transaction_id, ))
	return transaction


def get_account_transactions(account_id):
	account_transactions = query_rows("""SELECT ts.name as source, at.amount AS amount, tt.name AS type, at.timestamp AS timestamp, u.username AS transaction_user FROM account_transactions AS at
                 JOIN transaction_types AS tt ON tt.transaction_type_id = at.transaction_type_id
                 JOIN transaction_source as ts ON ts.source_id = at.source_id
	             LEFT JOIN account_transaction_user as atu ON at.transaction_id = atu.transaction_id
                 LEFT JOIN users as u ON u.user_id = atu.user_id
	             WHERE account_id = ? ORDER BY timestamp DESC""",(account_id, ))
	for a in account_transactions:
		a["amount"] = Currency(a["amount"])
	return account_transactions

def get_account_permissions(user_id, account_id):
	permissions = query_rows("""SELECT p.name from account_permissions AS ap
                 JOIN permissions as p ON p.permission_id = ap.permission_id
                 WHERE ap.account_id = ? AND ap.user_id = ?""",(account_id, user_id))
	return [p["name"] for p in permissions]

def get_account_info(account_id):
	account_info = query_row("""SELECT a.account_number AS account_number, an.name AS name,
                   SUM(CASE tt.positive WHEN 1 THEN at.amount ELSE 0 END) - SUM(CASE tt.positive WHEN 1 THEN 0 ELSE at.amount END) AS balance
                   FROM accounts AS a
                   LEFT JOIN account_name AS an ON an.account_id = a.account_id
                   LEFT JOIN account_transactions AS at ON at.account_id = a.account_id
                   JOIN transaction_types AS tt ON tt.transaction_type_id = at.transaction_type_id
                   WHERE a.account_id = ?
	          """, (account_id, ))
	return account_info

def get_viewable_accounts(user_id):
	db = get_db_connection()
	c = db.cursor()
	c.execute("""SELECT a.account_id FROM accounts AS a JOIN account_permissions AS ap ON ap.account_id = a.account_id
                     JOIN permissions AS p ON p.permission_id = ap.permission_id WHERE ap.user_id = ? AND p.name = 'view'""",
				  (user_id, )
		);
	return [x["account_id"] for x in c.fetchall()]
