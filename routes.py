import web_plugins.router as r

import login
import home
import details
import deposit
import withdrawl
from feedback import feedback_middleware
from web_plugins.response import HtmlResponse
static_router = r.FileRoute('/','./static')

def handle404(request):
	response = HtmlResponse()
	response.response_text = "Could not find page"
	return response

router = r.FirstMatchRouter()


dynamic_router = r.FirstMatchRouter()

dynamic_router.pre_route.extend([])
dynamic_router.post_route.extend([feedback_middleware])
dynamic_router.routes.extend(
	[ login.login_router,
	  home.router,
	  deposit.router,
	  withdrawl.router,
	  details.router
	]
)

router.routes.extend(
	[ static_router,
	  dynamic_router,
	  r.Route(handle404)
	]
)
