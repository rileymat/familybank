import web_plugins.router as r
from web_plugins.response import HtmlTemplateResponse, HtmlResponse
from web_plugins.response import Redirect

import account
from money import Currency


def withdrawl(request):
	response = HtmlTemplateResponse('withdrawl.mustache')
	response.arguments = {'account_balance': account.get_account_balance(request.session["accounts"][0])}
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
	r.Route(withdrawl)
])



router = r.FirstMatchRouter()
router.routes.extend([r.RegexRoute('/account/(?P<account_id>\w+)/withdrawl', withdrawl_router)])
