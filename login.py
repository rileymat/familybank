import web_plugins.router as r

from web_plugins.response import HtmlTemplateResponse
from web_plugins.response import HtmlResponse
from web_plugins.response import Redirect
from web_plugins.response import OriginRedirect

is_logged_in = lambda request: "user" in request.session
is_logged_out = lambda request: not is_logged_in(request)


import sqlite3

def logged_out_post(request):
	username = request.form_data["username"]
	password = request.form_data["password"]
	db = sqlite3.connect('./bank.db')
	c = db.cursor()
	c.execute("SELECT * FROM users where username = ? AND password = ?", (username, password))
	result = c.fetchall()

	if len(result) > 0:
		response = OriginRedirect(request, "/")
		request.session["user"] = result[0]
	else:
		response = Redirect("/login")

	response.arguments = {}
	return response

def logged_out_get(request):
	response = HtmlTemplateResponse('login.mustache')
	response.arguments = {}
	return response

def logout(request):
	del request.session["user"]
	return Redirect("/login")

login_page_router = r.FirstMatchRouter()
login_page_router.routes.extend(
	[r.MethodRoute("post", logged_out_post),
	 r.MethodRoute("get", logged_out_get)])

logged_out_router = r.FirstMatchRouter()
logged_out_router.routes.extend([r.ExactRoute('/login', login_page_router),
								 r.Route(lambda request: Redirect('/login', request.path))])

login_router = r.FirstMatchRouter()
login_router.routes.extend(
[r.ExactRoute('/logout', logout),
 r.LambdaRoute(is_logged_out, logged_out_router)])
