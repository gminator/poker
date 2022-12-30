from django.test import TestCase
from game.models import *
from game.exceptions import * 
from unittest_data_provider import data_provider
from unittest.mock import patch
from game.views import ClassifierView
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


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



	is_a_pair = lambda: (
			( 
				
				#Successfull Test
				(True, {"return_value" : {"2" : 2, "3" : 3}}),
				(False, {"return_value" : {"1" : 2, "1" : 4, "3" : 3}}),
			)
		)


	@data_provider(is_a_pair)
	def test_is_a_pair(self, expected_output, get_kind_reponse):  
		with patch.object(Classifier, 'get_kinds', **get_kind_reponse) as mock:
			classifier = Classifier()
			self.assertEquals(expected_output, classifier.is_a_pair())




	is_two_pair = lambda: (
			( 
				
				#Successfull Test
				(True, {"return_value" : {"3" : 2, "2" : 2, "K" : 1}}),
				(False, {"return_value" : {"2" : 2, "3" : 3}}),
				(False, {"return_value" : {"K" : 1,"5" : 1, "3" : 3}}),
			)
		)


	@data_provider(is_two_pair)
	def test_is_two_pair(self, expected_output, get_kind_reponse):  
		with patch.object(Classifier, 'get_kinds', **get_kind_reponse) as mock:
			classifier = Classifier()
			self.assertEquals(expected_output, classifier.is_two_pair())



	is_full_house = lambda: (
			( 
				
				#Successfull Test
				(True, {"return_value" : {"3" : 2, "2" : 3}}),
				(False, {"return_value" : {"2" : 1, "3" : 3, "K" : 1}}),
				(False, {"return_value" : {"K" : 1,"5" : 1, "A" : 2, "Q" : 1}}),
			)
		)


	@data_provider(is_full_house)
	def test_is_full_house(self, expected_output, get_kind_reponse):  
		with patch.object(Classifier, 'get_kinds', **get_kind_reponse) as mock:
			classifier = Classifier()
			self.assertEquals(expected_output, classifier.is_full_house())


	is_flush = lambda: (
			( 
				
				#Successfull Test
				(False, {"return_value" : {"♥" : 2, "♣" : 3}}),
				(False, {"return_value" : {"♥" : 4, "♣" : 1}}),
				(True, {"return_value" : {"♥" : 5}}),
			)
		)


	@data_provider(is_flush)
	def test_is_flush(self, expected_output, get_kind_reponse):  
		with patch.object(Classifier, 'get_suits', **get_kind_reponse) as mock:
			classifier = Classifier()
			self.assertEquals(expected_output, classifier.is_flush())



	is_straight = lambda: (
			( 
				("AS,10C,JH,QD,KS",True),
				("5S,7C,6H,8D,9S",True),
				("5S,7C,6H,8D,JS",False),
			)
		)


	@data_provider(is_straight)
	def test_is_straight(self, card_string, expected_output):  
		classifier = Classifier()
		classifier.parse(card_string)
		self.assertEquals(expected_output, classifier.is_straight())




	is_straight_flush = lambda: (
			( 
				
				#Successfull Test
				(True, {"return_value" : True}, {"return_value" : True}),
				#Not Streight 
				(False, {"return_value" : False}, {"return_value" : True}),
				#Is a streight but not flush
				(False, {"return_value" : True}, {"return_value" : False}),
			)
		)


	@data_provider(is_straight_flush)
	def test_is_straight_flush(self, expected_output, is_straight_output, is_flush_output):  
		with patch.object(Classifier, 'is_straight', **is_straight_output) as mock:
			with patch.object(Classifier, 'is_flush', **is_flush_output) as mock:
				classifier = Classifier()
				self.assertEquals(expected_output, classifier.is_straight_flush())


	is_royal_flush = lambda: (
			( 
				
				#Successfull Test
				(True, {"return_value" : True}, {"return_value" : (14, None)}),
				#Not Streight + Flush but no high card
				(False, {"return_value" : True}, {"return_value" : (10, None)}),
				#High Card with no streight + flush
				(False, {"return_value" : False}, {"return_value" : (14, None)}),
			)
		)


	@data_provider(is_royal_flush)
	def test_is_royal_flush(self, expected_output, is_straight_flush_output, high_card_output):  
		with patch.object(Classifier, 'is_straight_flush', **is_straight_flush_output) as mock:
			with patch.object(Classifier, 'high_card', **high_card_output) as mock:
				classifier = Classifier()
				self.assertEquals(expected_output, classifier.is_royal_flush())




	evaluate = lambda: (
			( 
				
				#Successfull Test
				("Royal Flush", 
						{"return_value" : True}, #ROYAL_FLUSH = "Royal Flush" 
						{"return_value" : True}, #STRAIGHT_FLUSH = "Straight Flush"
						{"return_value" : True}, #FOUR_KIND = "Four of a kind"
						{"return_value" : True}, #FULL_HOUSE = "Full House"
						{"return_value" : True}, #FLUSH = "Flush"
						{"return_value" : True}, #STRAIGHT = "Straight"
						{"return_value" : True}, #THREE_KIND = "Three of a kind"
						{"return_value" : True}, #TOW_PAIR = "Tow Pair"
						{"return_value" : True}, #PAIR = "Pair"
						{"return_value" : True}, #HIGH_CARD = "High Card"

				),
				
				("Straight Flush", 
						{"return_value" : False}, #ROYAL_FLUSH = "Royal Flush" 
						{"return_value" : True}, #STRAIGHT_FLUSH = "Straight Flush"
						{"return_value" : True}, #FOUR_KIND = "Four of a kind"
						{"return_value" : True}, #FULL_HOUSE = "Full House"
						{"return_value" : True}, #FLUSH = "Flush"
						{"return_value" : True}, #STRAIGHT = "Straight"
						{"return_value" : True}, #THREE_KIND = "Three of a kind"
						{"return_value" : True}, #TOW_PAIR = "Tow Pair"
						{"return_value" : True}, #PAIR = "Pair"
						{"return_value" : True}, #HIGH_CARD = "High Card"

				),

				("Four of a kind", 
						{"return_value" : False}, #ROYAL_FLUSH = "Royal Flush" 
						{"return_value" : False}, #STRAIGHT_FLUSH = "Straight Flush"
						{"return_value" : True}, #FOUR_KIND = "Four of a kind"
						{"return_value" : True}, #FULL_HOUSE = "Full House"
						{"return_value" : True}, #FLUSH = "Flush"
						{"return_value" : True}, #STRAIGHT = "Straight"
						{"return_value" : True}, #THREE_KIND = "Three of a kind"
						{"return_value" : True}, #TOW_PAIR = "Tow Pair"
						{"return_value" : True}, #PAIR = "Pair"
						{"return_value" : True}, #HIGH_CARD = "High Card"

				),

				("Full House", 
						{"return_value" : False}, #ROYAL_FLUSH = "Royal Flush" 
						{"return_value" : False}, #STRAIGHT_FLUSH = "Straight Flush"
						{"return_value" : False}, #FOUR_KIND = "Four of a kind"
						{"return_value" : True}, #FULL_HOUSE = "Full House"
						{"return_value" : True}, #FLUSH = "Flush"
						{"return_value" : True}, #STRAIGHT = "Straight"
						{"return_value" : True}, #THREE_KIND = "Three of a kind"
						{"return_value" : True}, #TOW_PAIR = "Tow Pair"
						{"return_value" : True}, #PAIR = "Pair"
						{"return_value" : True}, #HIGH_CARD = "High Card"

				),

				("Flush", 
						{"return_value" : False}, #ROYAL_FLUSH = "Royal Flush" 
						{"return_value" : False}, #STRAIGHT_FLUSH = "Straight Flush"
						{"return_value" : False}, #FOUR_KIND = "Four of a kind"
						{"return_value" : False}, #FULL_HOUSE = "Full House"
						{"return_value" : True}, #FLUSH = "Flush"
						{"return_value" : True}, #STRAIGHT = "Straight"
						{"return_value" : True}, #THREE_KIND = "Three of a kind"
						{"return_value" : True}, #TOW_PAIR = "Tow Pair"
						{"return_value" : True}, #PAIR = "Pair"
						{"return_value" : True}, #HIGH_CARD = "High Card"

				),

				("Straight", 
						{"return_value" : False}, #ROYAL_FLUSH = "Royal Flush" 
						{"return_value" : False}, #STRAIGHT_FLUSH = "Straight Flush"
						{"return_value" : False}, #FOUR_KIND = "Four of a kind"
						{"return_value" : False}, #FULL_HOUSE = "Full House"
						{"return_value" : False}, #FLUSH = "Flush"
						{"return_value" : True}, #STRAIGHT = "Straight"
						{"return_value" : True}, #THREE_KIND = "Three of a kind"
						{"return_value" : True}, #TOW_PAIR = "Tow Pair"
						{"return_value" : True}, #PAIR = "Pair"
						{"return_value" : True}, #HIGH_CARD = "High Card"

				),

				("Three of a kind", 
						{"return_value" : False}, #ROYAL_FLUSH = "Royal Flush" 
						{"return_value" : False}, #STRAIGHT_FLUSH = "Straight Flush"
						{"return_value" : False}, #FOUR_KIND = "Four of a kind"
						{"return_value" : False}, #FULL_HOUSE = "Full House"
						{"return_value" : False}, #FLUSH = "Flush"
						{"return_value" : False}, #STRAIGHT = "Straight"
						{"return_value" : True}, #THREE_KIND = "Three of a kind"
						{"return_value" : True}, #TOW_PAIR = "Tow Pair"
						{"return_value" : True}, #PAIR = "Pair"
						{"return_value" : True}, #HIGH_CARD = "High Card"

				),

				("Two Pair", 
						{"return_value" : False}, #ROYAL_FLUSH = "Royal Flush" 
						{"return_value" : False}, #STRAIGHT_FLUSH = "Straight Flush"
						{"return_value" : False}, #FOUR_KIND = "Four of a kind"
						{"return_value" : False}, #FULL_HOUSE = "Full House"
						{"return_value" : False}, #FLUSH = "Flush"
						{"return_value" : False}, #STRAIGHT = "Straight"
						{"return_value" : False}, #THREE_KIND = "Three of a kind"
						{"return_value" : True}, #TOW_PAIR = "Tow Pair"
						{"return_value" : True}, #PAIR = "Pair"
						{"return_value" : 10}, #HIGH_CARD = "High Card"

				),

				("Pair", 
						{"return_value" : False}, #ROYAL_FLUSH = "Royal Flush" 
						{"return_value" : False}, #STRAIGHT_FLUSH = "Straight Flush"
						{"return_value" : False}, #FOUR_KIND = "Four of a kind"
						{"return_value" : False}, #FULL_HOUSE = "Full House"
						{"return_value" : False}, #FLUSH = "Flush"
						{"return_value" : False}, #STRAIGHT = "Straight"
						{"return_value" : False}, #THREE_KIND = "Three of a kind"
						{"return_value" : False}, #TOW_PAIR = "Tow Pair"
						{"return_value" : True}, #PAIR = "Pair"
						{"return_value" : 10}, #HIGH_CARD = "High Card"

				),


				("High Card", 
						{"return_value" : False}, #ROYAL_FLUSH = "Royal Flush" 
						{"return_value" : False}, #STRAIGHT_FLUSH = "Straight Flush"
						{"return_value" : False}, #FOUR_KIND = "Four of a kind"
						{"return_value" : False}, #FULL_HOUSE = "Full House"
						{"return_value" : False}, #FLUSH = "Flush"
						{"return_value" : False}, #STRAIGHT = "Straight"
						{"return_value" : False}, #THREE_KIND = "Three of a kind"
						{"return_value" : False}, #TOW_PAIR = "Tow Pair"
						{"return_value" : False}, #PAIR = "Pair"
						{"return_value" : 10}, #HIGH_CARD = "High Card"

				),
			)
		)


	@data_provider(evaluate)
	def test_evaluate(self, expected_output, 
			royal_flush,
			streight_flush,
			four_kind,
			full_house,
			flush,
			straight,
			three_kinds,
			two_pair,
			pair,
			high_card):

		#print(royal_flush)  
		with patch.object(Classifier, 'is_royal_flush', **royal_flush) as mock:
			with patch.object(Classifier, 'is_straight_flush', **streight_flush) as mock:
				with patch.object(Classifier, 'is_4_of_a_kind', **four_kind) as mock:
					with patch.object(Classifier, 'is_full_house', **full_house) as mock:
						with patch.object(Classifier, 'is_flush', **flush) as mock:
							with patch.object(Classifier, 'is_straight', **straight) as mock:
								with patch.object(Classifier, 'is_3_of_a_kind', **three_kinds) as mock:
									with patch.object(Classifier, 'is_two_pair', **two_pair) as mock:
										with patch.object(Classifier, 'is_a_pair', **pair) as mock:
											with patch.object(Classifier, 'high_card', **high_card) as mock:
												classifier = Classifier()
												self.assertEquals(expected_output, classifier.evaluate())




	api = lambda: (
			( 
				
				#Royal Flush
				( {'cards': '10H,JH,QH,KH,AH'},
				200, {
				"hand" : "Royal Flush",
				"cards" : ["10♥","J♥","Q♥","K♥","A♥",]
				}),


				#Straight Flush
				( {'cards': '9H,10H,JH,QH,KH'},
				200, {
				"hand" : "Straight Flush",
				"cards" : ["9♥","10♥","J♥","Q♥","K♥"]
				}),


				#Straight
				( {'cards': '9H,10H,JH,QC,KH'},
				200, {
				"hand" : "Straight",
				"cards" : ["9♥","10♥","J♥","Q♣","K♥"]
				}),


				#Flush
				( {'cards': '9H,10H,JH,5H,KH'},
				200, {
				"hand" : "Flush",
				"cards" : ["5♥","9♥","10♥","J♥","K♥"]
				}),


				#Pair
				( {'cards': '5C,10H,JH,5H,KH'},
				200, {
				"hand" : "Pair",
				"cards" : ["5♣","5♥","10♥","J♥","K♥"]
				}),

				#2 Pair
				( {'cards': '5C,10H,JH,5H,10C'},
				200, {
				"hand" : "Two Pair",
				"cards" : ["5♣","5♥","10♥","10♣","J♥"]
				}),

				#4 Of Kind
				( {'cards': '5C,5D,5S,5H,10C'},
				200, {
				"hand" : "Four of a kind",
				"cards" : ["5♣","5♦","5♠","5♥","10♣"]
				}),


				#3 Of Kind
				( {'cards': '5C,5D,5S,6H,10C'},
				200, {
				"hand" : "Three of a kind",
				"cards" : ["5♣","5♦","5♠","6♥","10♣"]
				}),


				#Full House
				( {'cards': '5C,5D,5S,10H,10C'},
				200, {
				"hand" : "Full House",
				"cards" : ["5♣","5♦","5♠","10♥","10♣"]
				}),

				#Invalid Card String
				( {'cards': '10H*&S,JH,QH,KH,AH'},
				400, {"error" : "10H*&S,JH,QH,KH,AH does not match format AS,10C,10H,3D,3S"}),

				#B is not a suit
				( {'cards': '10B,JH,QH,KH,AH'},
				400, {"error" : "10B,JH,QH,KH,AH does not match format AS,10C,10H,3D,3S"}),

				#Card To Low
				( {'cards': '1H,JH,QH,KH,AH'},
				400, {"error" : "1 is not a valid number between 2 - 14"}),


				#Card To Low
				( {'cards': 'KH,JH,QH,KH,15H'},
				400, {"error" : "15 is not a valid number between 2 - 14"}),
			)
		)


	@data_provider(api)
	def test_api(self, body, status, json):  
		#raise Exception([hasattr(self, "client"), getattr(self, "token")])
		if not hasattr(self, "token"):
			self.client = APIClient()
			self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
			self.token = Token.objects.create(user=self.user)
			#raise Exception(1)

		request  = APIRequestFactory().post('/classify/', body, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))
		view = ClassifierView.as_view({"post" : "create"})
		response = view(request)

		#self.assertEquals(status, response.status_code)
		self.assertEquals(json, response.data)
