import web_plugins.router as r
from web_plugins.response import HtmlTemplateResponse
from web_plugins.response import Redirect
def summary(request):
	response = HtmlTemplateResponse('summary.mustache')
	response.arguments = {}
	return response

router = r.FirstMatchRouter()
router.routes.extend([r.ExactRoute('/summary', summary),r.ExactRoute('/', lambda request: Redirect('/summary'))])
