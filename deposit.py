import web_plugins.router as r
from web_plugins.response import HtmlTemplateResponse, HtmlResponse
from web_plugins.response import Redirect

import account
from money import Currency


def deposit(request):
	response = HtmlTemplateResponse('deposit.mustache')
	response.arguments = {'account_name': account.get_account_name(request.params["account_id"])}
	return response

def make_deposit(request):
	request.session["feedback"] = ["Sucessful deposit"]
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
