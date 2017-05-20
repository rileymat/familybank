import web_plugins.router as r
from web_plugins.response import HtmlTemplateResponse, HtmlResponse
from web_plugins.response import Redirect

from database import get_db_connection
import account
from money import Currency

def withdrawl(request):
	response = HtmlTemplateResponse('withdrawl.mustache')
	response.arguments = account.Account(request.params["account_id"])
	return response

def make_withdrawl(request):
   	amount = Currency(request.form_data["amount"])
	account_id = request.params["account_id"]
	user_id = request.session["user"]["user_id"]
	db = get_db_connection()
	c = db.cursor()
	c.execute("INSERT INTO account_transactions (account_id, amount, transaction_type_id, timestamp, source_id) VALUES(?,?,2,CURRENT_TIMESTAMP,2)",
			  (account_id, int(amount)))
	c.execute("INSERT INTO account_transaction_user (transaction_id, user_id) VALUES(?,?)", (c.lastrowid, user_id))
	db.commit()
	request.session["feedback"] = ["withdrawl amount" + str(amount) + " for account " + account_id]

	response = Redirect('/')
	return response


withdrawl_router = r.FirstMatchRouter()

def can_withdrawl(request):
	permissions = account.get_account_permissions(request.session["user"]["user_id"], request.params["account_id"])
	return 'withdrawl' in permissions

def unauthorized(request):
	response = HtmlResponse()
	response.response_text = "Unauthorized"
	return response

withdrawl_router.routes.extend([
	r.LambdaRoute(lambda request: not can_withdrawl(request), unauthorized),
	r.MethodRoute("post", make_withdrawl),
	r.MethodRoute("get", withdrawl)
])



router = r.FirstMatchRouter()
router.routes.extend([r.RegexRoute('/account/(?P<account_id>\w+)/withdrawl', withdrawl_router)])
