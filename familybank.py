
import web_plugins.app
from web_plugins.app import application
from web_plugins.response import HtmlResponse
import web_plugins.router as r

from web_plugins.response import HtmlTemplateResponse
import web_plugins.htmlpage as wp
import web_plugins.template as t


def familybank(request):
	response = HtmlTemplateResponse('dashboard.mustache')
	response.arguments = {}
	return response
"""
	response = HtmlResponse()
	response.response_text = "familybank feels great."
	return response
"""

static_router = r.FileRoute('/','./static')
router = r.FirstMatchRouter()
router.routes.extend([static_router, r.Route(familybank)])
application.handler = router

HtmlTemplateResponse.default_template_handler = t.TemplateHandler(t.PystacheFileAdapter('./templates'))
