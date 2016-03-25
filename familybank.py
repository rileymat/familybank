from web_plugins.app import application
from web_plugins.response import HtmlTemplateResponse
import web_plugins.template as t

from web_plugins.session import InMemorySessionHandler

import routes

application.handler = routes.router
application.session_handler = InMemorySessionHandler()

HtmlTemplateResponse.default_template_handler = t.TemplateHandler(t.PystacheFileAdapter('./templates'))
