from django.test import TestCase
from game.models import *
from game.exceptions import * 
from unittest_data_provider import data_provider
from unittest.mock import patch

# Create your tests here.
class CardTest(TestCase):


	validate = lambda: (
		( 
			#Success Hearts
			(Card(None, suit="H", number=2), True, None ), 
			
			#Success Spades
			(Card(None, suit="S", number=9), True, None),
			
			#Success Diamonds
			(Card(None, suit="D", number=2), True, None), 

			#Success Club
			(Card(None, suit="C", number=2), True, None),
			
			#Failed Invalid Suit
			(Card(None, suit="B", number=2), False, InvalidSuitException),
			
			#Failed Number Too Low
			(Card(None, suit="H", number=1), False, InvalidCardNumberException),
			
			#Failed Number To High
			(Card(None, suit="H", number=15), False, InvalidCardNumberException)
		)

	)

	@data_provider(validate)
	def test_validate(self, card, expected, exception): 
		try: 
			result = card.validate()
			self.assertEquals(result, expected)
		except GameException as e:
			self.assertTrue(type(e) is exception) 

	
	parse = lambda: (
		( 
			#Success Parse 5 of Hearts
			("5H", Card(None, suit="H", number=5, letter="5", symbol="♥"), {"return_value" : True}, None),

			#Success Parse 2 of Diamonds
			("2D", Card(None, suit="D", number=2, letter="2", symbol="♦"), {"return_value" : True},None), 
			
			#Success Parse 7 of Spades
			("7S", Card(None, suit="S", number=7, letter="7", symbol="♠"), {"return_value" : True},None), 

			#Success Parse 7 of Clubs
			("7C", Card(None, suit="C", number=7, letter="7", symbol="♣"), {"return_value" : True},None), 
			
			#Success Parse J - Aof Spades
			("JS", Card(None, suit="S", number="J", letter="J", symbol="♠"), {"return_value" : True},None),
			("KS", Card(None, suit="S", number="K", letter="K", symbol="♠"), {"return_value" : True},None),
			("QS", Card(None, suit="S", number="Q", letter="Q", symbol="♠"), {"return_value" : True},None),
			("AS", Card(None, suit="S", number="A", letter="A", symbol="♠"), {"return_value" : True},None),
						
			#Negative Bad String
			("5X", Card(None, suit="H", number=5, letter="5", symbol="♥"), {"return_value" : True},InvalidCardStringException),
			
			#Negative Validation Failed
			("5H", Card(None, suit="H", number=5, letter="5", symbol="♥"), {"side_effect" : InvalidSuitException()}, InvalidSuitException), 
			("5H", Card(None, suit="H", number=5, letter="5", symbol="♥"), {"side_effect" : InvalidCardNumberException()}, InvalidCardNumberException),  
		)

	)


	@data_provider(parse)
	def test_parse(self, string, expected, validate, exception): 
		with patch.object(Card, 'validate', **validate) as mock:
			try:
				card = Card.parse(string)
				self.assertEquals(card.suit, expected.suit)
				self.assertEquals(card.number, expected.number)
				self.assertEquals(card.letter, expected.letter, "Expected %s but got %s" % (expected.letter, card.letter))
				self.assertEquals(card.symbol, expected.symbol)
			except GameException as e: 
				self.assertTrue(type(e) is exception)

	
class ClassifierTest(TestCase):

	parse = lambda: (
			( 
				#Invalid String
				("Invalid Hand String", {"return_value" : Card(None, suit="S", number="J", letter="J", symbol="♠")}, InvalidHandString, 5),
				
				#Card Validation Failed
				("AS,10C,10H,3D,3S", {"side_effect" : InvalidSuitException()}, InvalidSuitException, 0),
				("AS,10C,10H,3D,3S", {"side_effect" : InvalidCardNumberException()}, InvalidCardNumberException, 0),
				
				#Successfull Test
				("AS,10C,10H,3D,3S", {"return_value" : Card(None, suit="S", number="J", letter="J", symbol="♠")}, None, 5),
			)
		)


	@data_provider(parse)
	def test_parse(self, string, card_effect, exception, cards): 
		with patch.object(Card, 'parse', **card_effect) as mock:
			try:
				classifier = Classifier()
				classifier.parse(string)
				self.assertEquals(len(classifier.cards), cards) 
			except GameException as e:
				self.assertTrue(type(e) is exception)

	high_card = lambda: (
			( 
				
				#Successfull Test
				("AS,10C,10H,3D,3S", 14, Card(None, suit="S", number="A", letter="A", symbol="♠")),

				("2S,10H,10C,3D,3S", 10, Card(None, suit="H", number="10", letter="10", symbol="♥")),
			)
		)


	@data_provider(high_card)
	def test_high_card(self, string, value, expected):  
		classifier = Classifier()
		classifier.parse(string)
		val, card  = classifier.high_card()

		self.assertEquals(val, value)
		self.assertEquals(card.symbol, expected.symbol)
		self.assertEquals(card.suit, expected.suit)
		self.assertEquals(card.letter, expected.letter)
		self.assertEquals(card.number, expected.number)
