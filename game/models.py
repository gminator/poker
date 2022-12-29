from django.db import models
from game.exceptions import *
import re
from collections import Counter

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

	def low_card(self,):
		"""
		Low Card

		Get lowest card in hand 

		-- Return 
		tuple (int number, Card card)
		"""
		card = self.cards[0]

		for c in self.cards: 
			if c.number < card.number: 
				card = c

		return (card.number,card)

	def get_suits(self,):
		"""
		Get Suits 

		This function will group cards 
		into their suits for evaluation

		-- Return 
		dictionary {String suit : int count}
		"""
		suits = {}
		for c in self.cards:
			suits[c.symbol] = suits.get(c.symbol, 0)
			suits[c.symbol] += 1

		return suits 

	def get_kinds(self,):
		"""
		Get Suits 

		This function will group cards 
		into their numeric values for evaluation

		-- Return 
		dictionary {String kind : int count}
		"""
		suits = {}
		for c in self.cards:
			#print(c.letter)
			suits[c.letter] = suits.get(c.letter, 0)
			suits[c.letter] += 1

		return suits 

	def is_a_pair(self, search=2):
		"""
		Is A Pair 

		Determine if we have any 2 of the same 
		cards in this self.cards

		-- Return 
		Boolean True|False

		-- Depends 
		Classifier.get_kinds
		"""
		kinds = self.get_kinds().values()
		return search in kinds


	def is_two_pair(self,):
		"""
		Is A Pair 

		Determine if we have any 2 of the same 
		cards in this self.cards twice

		or that 2 occurs twice in get_kinds

		-- Return 
		Boolean True|False

		-- Depends 
		Classifier.get_kinds
		"""
		kinds = self.get_kinds().values() #Group in kinds 
		pairs = Counter(kinds).get(2, False) #group counts to find of there are
		return pairs == 2

	def is_full_house(self,):
		"""
		Is Full House 

		Determine if I have a 2 pair & a 3 pair 
		in the same hand or self.cards

		-- Return 
		Boolean True | False

		-- Depends 
		Classifier::is_a_pair
		"""	
		return self.is_a_pair(2) and self.is_a_pair(3)


	def is_flush(self,):
		"""
		Is Flush 

		Determine if all 5 cards are of the same suit

		-- Return 
		Boolean True | False

		-- Depends 
		Classifier::get_suits
		"""	
		kinds = self.get_suits().values() #Group in kinds 
		return 5 in kinds

	def is_straight(self,):
		"""
		Is Straight 

		Determine if all 5 cards are in sequence

		-- Return 
		Boolean True | False

		"""	
		cards = [c.number for c in  self.cards]
		cards.sort()

		#If this is a mathematical sequence 
		# Then (value @ n + 1) - i should always be 1

		for n,i in enumerate(cards):
			n += 1
			if n != len(cards) and (cards[n] - i) != 1:
				return False
		return True

	def is_straight_flush(self,):
		"""
		Is Straight Flush 

		Determine if this cards form a 
		straight & a flush

		-- Returns 
		Boolean True|False

		-- Depends
		Classifier.is_straight
		Classifier.is_flush
		"""
		return self.is_flush() and self.is_straight()



