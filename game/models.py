from django.db import models
from game.exceptions import *
import re


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

	LETTERS = (
		("J", 11),
		("Q", 12),
		("K", 13),
		("A", 14),
	)

	def __init__(self, card: str, **kwargs):

		#For overiding in unit tests
		[setattr(self,k,v) for k,v in kwargs.items()]

		self.card = card
		self.letter = str(self.number)
		self.number = int(dict(Card.LETTERS).get(self.number, self.number))
		self.symbol = dict(Card.SUITS).get(self.suit, "")

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


	@staticmethod
	def parse(card: str):
		"""
		Parse 

		This will take the card string and convert its attributes

		-- Returns 
		Card()

		-- Throws 
		InvalidCardStringException 
		InvalidSuitException
		InvalidCardNumberException
		"""
		card = card.upper()
		match = re.search("([0-9AJKQ]{,2})([HDSC])", card, re.IGNORECASE)
		
		if not match:
			raise InvalidCardStringException("%s is not a valid card string" % card)
		
		card = Card(card, number=match.group(1), suit=match.group(2))
		card.validate()
		return card



class Classifier(object): 

	def __init__(self,):
		self.cards = []
		

	def parse(self, hand: str): 
		"""
		Parse hand into individuals cards

		-- Return
		void 

		-- Throws 
		InvalidHandString
		InvalidCardStringException 
		InvalidSuitException
		InvalidCardNumberException

		"""
		match = re.search("([0-9AJKQ]{,2}[HDSC],?){5}", hand, re.IGNORECASE)

		if not match:
			raise InvalidHandString("%s does not match format AS,10C,10H,3D,3S" % hand)

		self.cards = [ Card.parse(i) for i in hand.split(",")]

	def high_card(self,):
		"""
		High Card

		Get highest card in hand 

		-- Return 
		tuple (int number, Card card)
		"""
		card = self.cards[0]

		for c in self.cards: 
			if c.number > card.number: 
				card = c

		return (card.number,card)