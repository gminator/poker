from django.db import models
from game.exceptions import *


class Card(object):
	"""
	Card 

	Store and validate card attributes 
	For late evaluation 
	"""
	SUITS = (
		("H","♥"),
		("S","♠"),
		("D","♦"),
		("C","♣"),
	)

	def __init__(self, card: str, **kwargs):

		#For overiding in unit tests
		[setattr(self,k,v) for k,v in kwargs.items()]

	def validate(self,): 
		"""
		Validate

		Ensure that use are only allowed to assign 
		Valid Suit and Number designations

		-- Returns 
		boolean True|False

		-- Throws
		InvalidSuitException When suit is not valid 
		InvalidCardNumberException When card number is not valid

		"""
		if self.suit not in dict(Card.SUITS):
			raise InvalidSuitException("%s is not a valid suit designation" % self.suit) 

		if not 2 <= self.number <= 14: 
			raise InvalidCardNumberException("%s is not a valid number between 2 - 14" % self.number) 

		return True