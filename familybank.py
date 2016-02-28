
import web_plugins.app
from web_plugins.app import application
from web_plugins.response import HtmlResponse
import web_plugins.router as r

def familybank(request):
	response = HtmlResponse()
	response.response_text = "familybank feels great."
	return response

static_router = r.FileRoute('/','./static')
router = r.FirstMatchRouter()
router.routes.extend([static_router, r.Route(familybank)])
application.handler = router

