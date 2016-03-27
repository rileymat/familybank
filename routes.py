import web_plugins.router as r

import login
import summary
import details
import deposit
import withdrawl

from web_plugins.response import HtmlResponse
static_router = r.FileRoute('/','./static')

def handle404(request):
	response = HtmlResponse()
	response.response_text = "Could not find page"
	return response

router = r.FirstMatchRouter()
router.routes.extend(
	[ static_router,
	  login.login_router,
	  summary.router,
	  deposit.router,
	  withdrawl.router,
	  details.router,
	  r.Route(handle404)
	]
)
