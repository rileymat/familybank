import web_plugins.router as r
import login as l
import summary as s

from web_plugins.response import HtmlResponse
static_router = r.FileRoute('/','./static')
#router = r.FirstMatchRouter()
#router.routes.extend([static_router, r.Route(familybank)])

def handle404(request):
	response = HtmlResponse()
	response.response_text = "Could not find page"
	return response

router = r.FirstMatchRouter()
router.routes.extend(
	[ static_router,
	  l.login_router,
	  s.router,
	  r.Route(handle404)
	]
)
