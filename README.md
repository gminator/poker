# Table of Contents  
1. [Summary](#summary)  
2. [Customer Brief](#customer-brief)  
3. [Solution](#solution)  
3.1 [Design Principles](#design-principles)  
3.2 [Framework Choice](#framework-choice)  
3.3 [Business Rules](#business-rules)  
3.4 [Poker Hands](#poker-hands)  
4. [Design](#design)  
4.1 [Card()](#card)  
4.1 [Classifier()](#classifire)  
5. [User Stories()](#user-stories)  
5.1. [Card Acceptance Criteria](#card-acceptance-criteria)
5.1. [Classifier Acceptance Criteria](#classifier-acceptance-criteria)

# Summary
The purpose of this Project is to demostrate my compencies in Python, OOP, SOLID and TDD.

It show how I go about planning, building and testing my work. 

# Customer Brief 

For this program, you will be taking a text input of playing cards and evaluating what the best poker
hand could be constructed with the cards.
For example, given a string input of:
'AS, 10C, 10H, 3D, 3S'

(the cards above are ace of spades, 10 of clubs, 10 of hearts, 3 of diamonds and 3 of spades)
Output would be: 'Two Pair'

# Solution 

This solution provides a simple that will accept 5 card and output a classification or name for Poker Combinations in that set of cards. 

It is written using Python3 with Django4,this only to show a working understanding of Django and will expose the functionanilty  Django Management cammands and a REST API built from Django Rest Framework. 

The application can be deployed using docker-compose (instructions to follow)

### Design Principles

The code will be written inline with the **SOLID principle** honoring single respobsibiliy, open close principle and interface segregation and effort to write DRY scalable code. 

**Single responsiblity** in important because it faciliates good TDD or Unit test, having fat or ambigious functions  makes testing difficult. 


The acceptance criteria is written in Gherkin, I've found that this is easier for stakeholder to validate assumptions against and for developers to write unit tests.


### Framework Choice 

Its not entirely neccasry to use a Framework like Django. I chose this to show that I have a grounded understanding of the elements of frameowrks (Routing, ORM, MVC, Serializers, etc) these exist in almost all frameworks irrespecitve of lanuage. 

### Business Rules 

There a rules that I will negate for the purpose of the excercise. 

#### The Joker 
The Joker is typically used as a wild card, players can use this stand in for cards of their choice. I will not be using this card in my evaluations as it will require additional user input, and is not critical for demostrating a working understanding of the principles I wish to demonstrate

#### The Ace 
The ace card can represent boht 1 & 14, aslo depending on the players choice. For purpose of the test it will always represent the highest available card. 

### Poker Hands

The supported poker hands are outlined below. 

![Poker Hands](https://github.com/gminator/poker/raw/main/docs/img/pocker-hands.jpg "Poker Hands")


# Design 
The solution consists of 2 basic models one for Storing Cards and the Other for the business logic of classification and comparison of Hands. 

## Card


Cards are complex in that they can be represented by letters (K,Q,J,A) that have a numeric value. The class will store these properties that can later be used for classification, validation and evaluation. 

|Cards| | |
|-------|-| -|
| **type** | **Name** | **Description** |
| **enum** | suit| Unicode Symbol For Cards|
| **int** | number | Numeric Number Of Card |
| **char** | letter |Alphabetical designation of card |
| **Card** | __init__(string card) | Initiate a new card|
| **boolean** | validate() | Check That card meets required criteria |

## Classifier

This class will house all the bussiness logic for the variuos poker hands 

|Classifire| | |
|-------|-| -|
| **type** | **Name** | **Description** |
| **array** |cards| An array of 5 Card() |
| **Classifier** | __init__(string cards) | Initiate a new card|
| **int** | high_card() | Get the highest card in hand |
| **int** | low_card() | Get the highest card in hand |
| **dictionary** | get_suits() | Get group of suits |
| **dictionary** | get_kinds() | Get group of kinds |
| **boolean** | is_a_pair(int pair) | Determine if all 5 cards are of the same suit |
| **boolean** | is_full_house() | Determine if there is full hand of sets |
| **boolean** | is_flush() | Determine if all 5 cards are of the same suit |
| **boolean** | is_streight() | Determine if we have a sequence of 5 numbers |
| **boolean** | is_streight_flush() | Determine if we have a sequence of 5 numbers of the same suits |
| **boolean** | is_royal_flush() | Determine if we have a sequence of 5 numbers of the same suits & with highest card being A |

# User Stories 
Below are the user stories written in a Gherkin styles. I prefer this method for writting out test cases, it makes it easy for both Stakeholders and developers to understand and critique the proposed flow.

## Card Acceptance Criteria 
These are the user stories for the card Model, validate will throw any exception if any of the attributes are outside of the specified range. 

It is implement by the parse, so that the error can buble up to the hgih levels of the code (API or Management Cammands) 


### Card::validate()
```
Feature: Card::validate
Validate the user inputs

Scenario: Failed Invalid Suit
Given I have Card(suit="B",...)
And I call the validate method 
Then I should recieve InvalidSuitException


Scenario: Failed Number Too Low
Given I have Card(number=0,...)
And I call the validate method 
Then I should recieve InvalidNumberException

Scenario: Failed Number Too High 
Given I have Card(number=20,...)
And I call the validate method 
Then I should recieve InvalidNumberException
```
### Card::parse(string card)

```
Feature: Card::parse
Conver text input to Card

Scenario: Ace oh Hearts
Given Card.validate() returns True 
And I call Card.parse("AH")
Then I should recieve Card(suit="♥", number=14, letter="A")

Scenario: King Of Spades
Given Card.validate() returns True 
And I call Card.parse("KS")
Then I should recieve Card(suit="♠", number=13, letter="K")


Scenario: Queen Of Clubs
Given Card.validate() returns True 
And I call Card.parse("QC")
Then I should recieve Card(suit="♣", number=12, letter="Q")


Scenario: Jack Of Diamonds
Given Card.validate() returns True 
And I call Card.parse("JD")
Then I should recieve Card(suit="♦", number=11, letter="J")


Scenario: 9 Of Diamonds
Given Card.validate() returns True 
And I call Card.parse("JD")
Then I should recieve Card(suit="♦", number=9, letter="9")


Scenario: 3 Of Hearts
Given Card.validate() returns True 
And I call Card.parse("3H")
Then I should recieve Card(suit="♥", number=3, letter="3")


Scenario: Validation Failed
Given Card.validate() throw InvalidSuitException 
And I call Card.parse("3H")
Then I should recieve an InvalidSuitException
```

## Classifier Acceptance Criteria 
This is the acceptance criteria for the Clasiffier, its written in a DRY format so that the individual test are re-usable. 

i.e Streight Flush is a combination of is_streight and is_flush, this makes the most effecient use of the code. 

### Classifire::parse 
```
Feature: Classifire::parse()
Conver text input to a list of cards


Scenario: Failed Invalid String
Given I Card.parse(...) returns Card()
And I have Classifier() as hand
And I call hand.parse("Invalid Hand String")
Then I should recieve and InvalidHandString 

Scenario: Failed Invalid Suit Given
Given I Card.parse(...) throws InvlidSuitException
And I have Classifier() as hand
And I call hand.parse("AS,...")
Then I should recieve and InvalidSuitException


Scenario: Failed Invalid Number
Given I Card.parse(...) throws InvlidNumberException
And I have Classifier() as hand
And I call hand.parse("AS,...")
Then I should recieve and InvlidNumberException


Scenario: Success
Given I Card.parse(...) returns Card()
And I have Classifier() as hand
And I call hand.parse("AH,KS,QC,JD,9D")
Then hand.cards should contain 5 Cards:
	| Card(suit="♥", number=14, letter="A") |
	| Card(suit="♠", number=13, letter="K") | 
	| Card(suit="♣", number=12, letter="Q") |
	| Card(suit="♦", number=11, letter="J") | 
	| Card(suit="♦", number=9, letter="9")  |
```
