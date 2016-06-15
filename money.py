import six
import decimal

class Currency(object):
	def __init__(self, amount):
		if isinstance(amount, six.string_types):
			x = decimal.Decimal(amount)
			x = x * 100
			self.amount = int(x)
		else:
			self.amount = amount
	def __str__(self):
		return str(self.amount/100) + "." + "%02d"%(self.amount%100)
	def __int__(self):
		return self.amount
