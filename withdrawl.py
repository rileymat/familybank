import web_plugins.router as r
from web_plugins.response import HtmlTemplateResponse
from web_plugins.response import Redirect

from account import get_account_balance
from money import Currency


def withdrawl(request):
	response = HtmlTemplateResponse('summary.mustache')
	response.arguments = {'account_balance': get_account_balance(request.session["accounts"][0])}
	return response

router = r.FirstMatchRouter()
router.routes.extend([r.ExactRoute('/withdrawl', withdrawl)])
