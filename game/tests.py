from django.test import TestCase
from game.models import Card 
from game.exceptions import * 
from unittest_data_provider import data_provider

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
    	except Exception as e:
    		self.assertTrue(type(e) is exception)

    	

    