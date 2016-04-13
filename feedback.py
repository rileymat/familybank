
def feedback_middleware(request, response):
	try:
		args = response.arguments
		if args is not None:
			feedback = request.session["feedback"]
			request.session["feedback"] = []
			args["feedback"] = feedback
			response.arguments = args
	except:
		pass
