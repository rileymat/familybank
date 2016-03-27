

class Currency(object):
	def __init__(self, amount):
		self.amount = amount
	def __str__(self):
		return str(self.amount/100) + "." + "%02d"%(self.amount%100)
