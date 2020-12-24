import math
from datetime import date
from fractions import Fraction

# this class represents shares

class Share:

	# class variables for cut off dates and prices before various cutoff points
	
	# PRICE1 is the price before CUTOFF1
	# PRICE2 is the price before CUTOFF2 and after CUTOFF1
	# PRICE3 is the price after CUTOFF2

	# all prices in whole dollars (AUD)


	CUTOFF1 = date(2021, 1, 14)
	CUTOFF2 = date(2021, 6, 10)

	PRICE1 = 5000
	PRICE2 = 5500
	PRICE3 = 6000

	def initialize(self, *args):
		''' create a share, either from a number of shares, or a dollar and a price '''
		
		# internally we store shares as a rational number

		if len(args) == 1: # one value provided, an amount of shares
			shares = args[0]
			self._rational = Fraction(shares)
		elif len(args) == 2: # two values provided, dollars and price
			dollars = args[0]
			price   = args[1]
			self._rational = Fraction(dollars, price)
		else:
			raise TypeError("wrong number of arguments ({}), expecting an amount or a dollar value and price".format(len(args)))

	def one(self):
		pass

	def as_rational(self):
		''' return shares as rational number '''
		return self.__rational


	def __add__(self, other):
		''' can add two shares together '''
		if not isinstance(other, Share):
			raise TypeError("expecting to add to another Share, got object of class '{}' instead".format(other.__class__.__name__))
		return Share(self.as_rational() + other.as_rational())


	def __float__(self):
		''' return the number of shares owned in floating point '''
		return float(self.as_rational())


	def __str__(self):
		''' return shares as string, a float truncated to a maximum of 2 decimal places'''
		
		as_float      = float(self)

		# calculate number of digits to left of decimal point
		
		# log10(x) gives (number of digits - 1) i.e. log10(10) is 1, log10(100) is 2, while log10(x<1.0) gives a negative number
		
		# add 1.0 to log10(x) to get total number of digits right of decimal, then int(value) will round down to 
		# the nearest whole integer i.e. int(1.1) is 1, int(0.9) is 0
		
		whole_digits  = int(1.0 + math.log10(as_float)) 
		
		# if whole digits is less than zero thanks to log10(...), set to 0
		whole_digits  = 0 if whole_digits < 0 else whole_digits 
		
		# maximum precision is number of whole digits + 2
		precision     = whole_digits + 2 

		 # construct format string with correct precision               
		format_string = "{{:.{}g}}".format(precision)  
		return format_string.format(as_float)



	@staticmethod
	def price_at(day):
		''' returns the price in AUD at a particular date '''

		if day < Share.CUTOFF1:
			return Share.PRICE1
		elif day < Share.CUTOFF2:
			return Share.PRICE2
		else:
			return Share.PRICE3


	@staticmethod
	def shares_purchased(dollars, day):
		''' return the number of shares that will be purchased if spending AUD 'dollars' at date 'day' '''
		price = Share.price_at(day)
		return Share(dollars, price)

