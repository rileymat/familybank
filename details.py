import web_plugins.router as r
from web_plugins.response import HtmlTemplateResponse, HtmlResponse
from web_plugins.response import Redirect

import account

from money import Currency
from datetime import datetime


def generate_descriptions(transactions):
	for transaction in transactions:
		if transaction["source"] == "Automatic Deposit":
			transaction["description"] = "Automatic Deposit"
		elif transaction["source"] == "user" and transaction["transaction_user"] is not None:
			transaction["description"] = transaction["type"].capitalize() + " By " + transaction["transaction_user"].capitalize()
		else:
			transaction["description"] = "unknown"
		transaction_timestamp = transaction["timestamp"]
		transaction_datetime = datetime.strptime(transaction_timestamp, '%Y-%m-%d %H:%M:%S')
		transaction["date"] = transaction_datetime.strftime("%-m-%-d-%y")
		transaction["time"] = transaction_datetime.strftime("%-I:%M %p")
	return transactions

def details(request):
	response = HtmlTemplateResponse('details.mustache')
	transactions = account.Transactions(request.params["account_id"])
	response.arguments = {'transactions': transactions}
	return response

details_router = r.FirstMatchRouter()

def can_view(request):
	permissions = account.get_account_permissions(request.session["user"]["user_id"], request.params["account_id"])
	return 'view' in permissions

def unauthorized(request):
	response = HtmlResponse()
	response.response_text = "Unauthorized"
	return response

details_router.routes.extend([
	r.LambdaRoute(lambda request: not can_view(request), unauthorized),
	r.Route(details)
])

router = r.FirstMatchRouter()
router.routes.extend([r.RegexRoute('/account/(?P<account_id>\w+)/details', details_router)])
