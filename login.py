import bcrypt

import web_plugins.router as r

from web_plugins.response import HtmlTemplateResponse
from web_plugins.response import HtmlResponse
from web_plugins.response import Redirect
from web_plugins.response import OriginRedirect

import account
from database import get_db_connection

is_logged_in = lambda request: "user" in request.session
is_logged_out = lambda request: not is_logged_in(request)




def logged_out_post(request):
	username = request.form_data["username"]
	password = request.form_data["password"]
	db = get_db_connection()
	c = db.cursor()
	c.execute("SELECT user_id, username, email, password  FROM users where username = ?", (username,))
	result = c.fetchall()

	if len(result) > 0:
		hashed_password_bytes = result[0]["password"].encode('utf-8')
		password_bytes = password.encode('utf-8')
		if bcrypt.hashpw(password_bytes, hashed_password_bytes) == hashed_password_bytes:
			response = OriginRedirect(request, "/")
			request.session["user"] = result[0]
			request.session["accounts"] = account.get_viewable_accounts(result[0]["user_id"])
		else:
			response = Redirect('/login');
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
	del request.session["accounts"]
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
