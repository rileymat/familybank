import web_plugins.router as r
from web_plugins.response import HtmlTemplateResponse, HtmlResponse
from web_plugins.response import Redirect

from database import get_db_connection
import account
from money import Currency


def deposit(request):
	response = HtmlTemplateResponse('deposit.mustache')
	response.arguments = account.Account(request.params["account_id"])
	return response

def make_deposit(request):
	amount = Currency(request.form_data["amount"])
	account_id = request.params["account_id"]
	user_id = request.session["user"]["user_id"]
	db = get_db_connection()
	c = db.cursor()
	c.execute("INSERT INTO account_transactions (account_id, amount, transaction_type_id, timestamp, source_id) VALUES(?,?,1,CURRENT_TIMESTAMP,2)",
			  (account_id, int(amount)))
	c.execute("INSERT INTO account_transaction_user (transaction_id, user_id) VALUES(?,?)", (c.lastrowid, user_id))
	db.commit()
	request.session["feedback"] = ["deposit amount" + str(amount) + " for account " + account_id]

	response = Redirect('/')
	return response

deposit_router = r.FirstMatchRouter()

def can_deposit(request):
	permissions = account.get_account_permissions(request.session["user"]["user_id"], request.params["account_id"])
	return 'deposit' in permissions

def unauthorized(request):
	response = HtmlResponse()
	response.response_text = "Unauthorized"
	return response

deposit_router.routes.extend([
	r.LambdaRoute(lambda request: not can_deposit(request), unauthorized),
	r.MethodRoute("post", make_deposit),
	r.MethodRoute("get", deposit)
])


router = r.FirstMatchRouter()
router.routes.extend([r.RegexRoute('/account/(?P<account_id>\w+)/deposit', deposit_router)])
