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

	
	low_card = lambda: (
			( 
				
				#Successfull Test
				("AS,10C,10H,8D,3S", 3, Card(None, suit="S", number="3", letter="3", symbol="♠")),

				("9S,10H,10C,7D,4H", 4, Card(None, suit="H", number="4", letter="4", symbol="♥")),
			)
		)


	@data_provider(low_card)
	def test_low_card(self, string, value, expected):  
		classifier = Classifier()
		classifier.parse(string)
		val, card  = classifier.low_card()

		self.assertEquals(val, value)
		self.assertEquals(card.symbol, expected.symbol)
		self.assertEquals(card.suit, expected.suit)
		self.assertEquals(card.letter, expected.letter)
		self.assertEquals(card.number, expected.number)


	get_suits = lambda: (
			( 
				
				#Successfull Test
				("7H,6H,6C,5C,2C", {"♥" : 2, "♣" : 3}),

				("3H,6H,6C,5C,2D", {"♥" : 2, "♣" : 2, "♦" : 1}),
			)
		)


	@data_provider(get_suits)
	def test_get_suits(self, card_string, expected_output):  
		classifier = Classifier()
		classifier.parse(card_string)
		suits  = classifier.get_suits()
		self.assertEquals(suits, expected_output)



	get_kinds = lambda: (
			( 
				
				#Successfull Test
				("2H,2S,AH,AD,AS", {"2" : 2, "A" : 3}),

				("2H,2S,AH,AD,3S", {"2" : 2, "A" : 2, "3" : 1}),
			)
		)


	@data_provider(get_kinds)
	def test_get_kinds(self, card_string, expected_output):  
		classifier = Classifier()
		classifier.parse(card_string)
		suits  = classifier.get_kinds()
		self.assertEquals(suits, expected_output)
