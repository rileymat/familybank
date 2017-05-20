import web_plugins.router as r
from web_plugins.response import HtmlTemplateResponse
from web_plugins.response import Redirect

import account
from money import Currency


def summary(request):
	response = HtmlTemplateResponse('home.mustache')
	accounts = request.session["accounts"]
	account_data = []
	for a in accounts:
		info = account.Account(a)
		account_data.append(info)
	response.arguments = {'accounts': account_data}
	return response

router = r.FirstMatchRouter()
router.routes.extend([r.ExactRoute('/', summary)])
