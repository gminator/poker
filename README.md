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
4.1 [Classifier()](#classifier)  
5. [User Stories()](#user-stories)  
5.1. [Card Acceptance Criteria](#card-acceptance-criteria)  
5.1. [Classifier Acceptance Criteria](#classifier-acceptance-criteria)
6. [Installation](#installation)  


# Summary

The purpose of this Project is to demonstrate my competencies  in Python, OOP, SOLID and TDD/BDD.

It shows how I go about planning, building and testing  work. All my projects are accompanied with document similar to this as part of my planning approach. 

Documents such as these can be used for both Stakeholders and developers, and should help reduce ambiguity in the delivery scope by clearly outlining expectations and ensuring that the solution satisfies all critical requirements. 

# Customer Brief 

For this program, you will be taking a text input of playing cards and evaluating what the best poker
hand could be constructed with the cards.
For example, given a string input of:
'AS, 10C, 10H, 3D, 3S'

(the cards above are ace of spades, 10 of clubs, 10 of hearts, 3 of diamonds and 3 of spades)
Output would be: 'Two Pair'

# Solution 

This solution provides a simple program that will accept 5 cards and output a classification or name of the Poker Combinations in that set of cards. 

It is written using Python3 with Django3, the classifier will be exposed via a REST API built from Django Rest Framework. 

The application is deployed using Docker Compose. 

### Design Principles

The code will be written in line with the **SOLID principle** honouring single responsibility, open close principle and interface segregation in an effort to write DRY scalable code. 

**Separation of concerns** is important because it facilitates good TDD or Unit tests, having fat or ambiguous functions  makes testing difficult. 

The requirements are written in a Gherkin style, I've found that this is easier for stakeholders to validate assumptions against while still being clear enough to qualify for acceptance criteria when writing code.


### Framework Choice 

It’s not entirely necessary to use a Framework like Django for something so simple. I chose this to demonstrate an understanding of the elements of frameworks (Routing, ORM, MVC, Serializers, etc) these exist in almost all frameworks irrespective of language. 

### Business Rules 

There a rules that I will negate for the purpose of the exercise. 

#### The Joker 
The Joker is typically used as a wild card, players can use this stand in for cards of their choice. I will not be using this card in my evaluations as it will require additional user input, and is not critical for demonstrating a working understanding of the principles I wish to convey.

#### The Ace 
The ace card can represent both 1 & 14, also depending on the players choice. For the purpose of the test it will always represent the highest available card. 

### Poker Hands

The supported poker hands are outlined below. 

![Poker Hands](https://github.com/gminator/poker/raw/main/docs/img/pocker-hands.jpg "Poker Hands")


# Design 
The solution consists of 2 basic models one for Storing Cards and the Other for the business logic of classification and comparison of Hands. 

## Card

Cards are complex in that they can be represented by letters (K,Q,J,A) that have a numeric value with an accompanying suit or symbol. The class will store these properties that can later be used for classification, validation and evaluation.

|Cards| | |
|-------|-| -|
| **type** | **Name** | **Description** |
| **enum** | suit| Unicode Symbol For Cards|
| **int** | number | Numeric Number Of Card |
| **char** | letter |Alphabetical designation of card |
| **Card** | __init__(string card) | Initiate a new card|
| **boolean** | validate() | Check That card meets required criteria |

## Classifier

This class will house all the business logic for the various poker hands 

|Classifier| | |
|-------|-| -|
| **type** | **Name** | **Description** |
| **array** |cards| An array of 5 Card() |
| **Classifier** | __init__(string cards) | Initiate a new card|
| **void** | [parse(string cards)](#classifierparse) | Initiate a new card|
| **int** | [high_card()](#classifierhigh_card) | Get the highest card in hand |
| **int** | [low_card()](#classifierlow_card) | Get the highest card in hand |
| **dictionary** | [get_suits()](#classifierget_suits) | Get group of suits |
| **dictionary** | [get_kinds()](#classifierget_kinds) | Get group of kinds |
| **boolean** | [is_a_pair(int pair)](#classifieris_pair) | Determine if all 5 cards are of the same suit |
| **boolean** | [is_full_house()](#classifieris_full_house) | Determine if there is full hand of sets |
| **boolean** | [is_flush()](#classifieris_flush) | Determine if all 5 cards are of the same suit |
| **boolean** | [is_straight()](#classifieris_strieght) | Determine if we have a sequence of 5 numbers |
| **boolean** | [is_straight_flush()](#classifieris_flush) | Determine if we have a sequence of 5 numbers of the same suits |
| **boolean** | [is_royal_flush()](#classifieris_royal_flush) | Determine if we have a sequence of 5 numbers of the same suits & with highest card being A |

# User Stories 
Below are the user stories written in a Gherkin styles. I prefer this method for writing out test cases, it makes it easy for both Stakeholders and developers to understand and critique the proposed flow.

## Card Acceptance Criteria 
These are the user stories for the card Model, validate will throw any exception if any of the attributes are outside of the specified range. 

It is implement by the parse, so that the error can bubble up to the high levels of the code (API) 


### Card::validate()
```
Feature: Card::validate
Validate the user inputs

Scenario: Failed Invalid Suit
Given I have Card(suit="B",...)
And I call the validate method 
Then I should receive InvalidSuitException


Scenario: Failed Number Too Low
Given I have Card(number=0,...)
And I call the validate method 
Then I should receive InvalidNumberException

Scenario: Failed Number Too High 
Given I have Card(number=20,...)
And I call the validate method 
Then I should receive InvalidNumberException
```
### Card::parse(string card)

```
Feature: Card::parse
Conver text input to Card

Scenario: Ace oh Hearts
Given Card.validate() returns True 
And I call Card.parse("AH")
Then I should receive Card(suit="♥", number=14, letter="A")

Scenario: King Of Spades
Given Card.validate() returns True 
And I call Card.parse("KS")
Then I should receive Card(suit="♠", number=13, letter="K")


Scenario: Queen Of Clubs
Given Card.validate() returns True 
And I call Card.parse("QC")
Then I should receive Card(suit="♣", number=12, letter="Q")


Scenario: Jack Of Diamonds
Given Card.validate() returns True 
And I call Card.parse("JD")
Then I should receive Card(suit="♦", number=11, letter="J")


Scenario: 9 Of Diamonds
Given Card.validate() returns True 
And I call Card.parse("JD")
Then I should receive Card(suit="♦", number=9, letter="9")


Scenario: 3 Of Hearts
Given Card.validate() returns True 
And I call Card.parse("3H")
Then I should receive Card(suit="♥", number=3, letter="3")


Scenario: Validation Failed
Given Card.validate() throw InvalidSuitException 
And I call Card.parse("3H")
Then I should receive an InvalidSuitException
```

## Classifier Acceptance Criteria 
This is the acceptance criteria for the Classifier, its written in a DRY format so that the individual test are re-usable. 

i.e Straight Flush is a combination of is_straight and is_flush, this makes the most efficient use of the code. 

### Classifier::parse 
```
Feature: Classifier::parse()
Convert text input to a list of cards


Scenario: Failed Invalid String
Given I Card.parse(...) returns Card()
And I have Classifier() as hand
And I call hand.parse("Invalid Hand String")
Then I should receive and InvalidHandString 

Scenario: Failed Invalid Suit Given
Given I Card.parse(...) throws InvlidSuitException
And I have Classifier() as hand
And I call hand.parse("AS,...")
Then I should receive and InvalidSuitException


Scenario: Failed Invalid Number
Given I Card.parse(...) throws InvlidNumberException
And I have Classifier() as hand
And I call hand.parse("AS,...")
Then I should receive and InvlidNumberException


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
### Classifier::high_card 
```

Feature: Classifier::high_card()
Retrieve highest card in deck 


Scenario: Regular cards 
Given have the following cards: 
	|1H,6S,6C,5D,2D|
And I call get Classifier::high_card()
Then I should reciece 6


Scenario: Complex Cards 
Given have the following cards: 
	|AH,6S,KC,5D,JD|
And I call get Classifier::high_card()
Then I should reciece 14
```

### Classifier::low_card 
```

Feature: Classifier::low_card()
Retrieve lowest card in deck 


Scenario: Regular cards 
Given have the following cards: 
	|1H,6S,6C,5D,2D|
And I call get Classifier::low_card()
Then I should reciece 1


Scenario: Complex Cards 
Given have the following cards: 
	|AH,6S,KC,5D,JD|
And I call get Classifier::low_card()
Then I should reciece 5
```



### Classifier::get_suits 

```
Feature: Classifier::get_suits()
I should be able to group and count suits 


Scenario: 2 Hearts 3 Spades
Given have the following cards: 
	|1H,6H,6S,5S,2S|
And I call get Classifier::get_suits()
Then I should reciece a dictionary 
	|♥|2|
	|♣|3|


Scenario: 2 Hearts, 3 Spades and 1 Diamond
Given have the following cards: 
	|1H,6H,6S,5S,2S|
And I call get Classifier::get_suits()
Then I should reciece a dictionary 
	|♥|2|
	|♣|2|
	|♦|1|
```


### Classifier::get_kinds 

```
Feature: Classifier::get_kinds()
I should be able to group and count kinds/numbers 


Scenario: 2x 4s, 3x As  
Given have the following cards: 
	|2H,2S,AH,AD,AS|
And I call get Classifier::get_suits()
Then I should reciece a dictionary 
	|2|2|
	|4|3|


Scenario: 2x 4s, 2x As and 1 3  
Given have the following cards: 
	|2H,2S,AH,AD,3S|
And I call get Classifier::get_suits()
Then I should reciece a dictionary 
	|2|2|
	|14|2|
	|3|1|
```


### Classifier::is_a_pair 

```
Feature: Classifier::get_kinds()
Determin combination of kinds


Scenario: Success 1 Pair 
Given I have a Classifier Object
And get_kinds returns a dictionary:
	|2|2|
	|3|3|
And I call get Classifier::is_a_pair(2)
Then I should receive True


Scenario: Failed 1 Pair 
Given I have a Classifier Object
And get_kinds returns a dictionary:
	|1|2|
	|1|4|
	|3|3|
And I call get Classifier::is_a_pair(2)
Then I should receive False


Scenario: Success 3 Of A Kind
Given I have a Classifier Object
And get_kinds returns a dictionary:
	|2|2|
	|3|3|
And I call get Classifier::is_a_pair(3)
Then I should receive True


Scenario: Failed 3 Of A Kind
Given I have a Classifier Object
And get_kinds returns a dictionary:
	|2|2|
	|2|3|
	|1|14|
And I call get Classifier::is_a_pair(3)
Then I should receive False 


Scenario: Success 4 Of A Kind
Given I have a Classifier Object
And get_kinds returns a dictionary:
	|2|2|
	|3|4|
And I call get Classifier::is_a_pair(4)
Then I should receive True


Scenario: Failed 4 Of A Kind
Given I have a Classifier Object
And get_kinds returns a dictionary:
	|2|2|
	|2|3|
	|1|14|
And I call get Classifier::is_a_pair(4)
Then I should receive False 

```


### Classifier::is_two_pair 

```
Feature: Classifier::is_two_pair()
Check for 2 sets of pairs 


Scenario: Success 2 Pair 
Given I have a Classifier Object
And get_kinds returns a dictionary:
	|2|2|
	|3|2|
And I call get Classifier::is_two_pair()
Then I should receive True

Scenario: Failed 2 Pair 
Given I have a Classifier Object
And get_kinds returns a dictionary:
	|2|2|
	|3|3|
And I call get Classifier::is_two_pair()
Then I should receive False

```

### Classifier::is_full_house

```
Feature: Classifier::is_full_house()
A hand that contains three cards of one rank and two cards of another rank

Scenario: Success Is Full House
Given I have a Classifier Object
And get_kinds returns a dictionary:
	|2|2|
	|3|3|
And I call get Classifier::is_full_house()
Then I should receive True


Scenario: Success Is Full House
Given I have a Classifier Object
And get_kinds returns a dictionary:
	|2|2|
	|3|2|
	|K|1|
And I call get Classifier::is_full_house()
Then I should receive False

```

### Classifier::is_flush

```
Feature: Classifier::is_flush()
Any five cards of the same suit which are not consecutive

Scenario: Success Is FLush
Given I have a Classifier Object
And get_suits returns a dictionary:
	|♥|5|
And I call get Classifier::is_flush()
Then I should receive True


Scenario: Success Is FLush
Given I have a Classifier Object
And get_suits returns a dictionary:
	|♥|4|
	|♠|1|
And I call get Classifier::is_flush()
Then I should receive False
```


### Classifier::is_straight

```
Feature: Classifier::is_straight()
Any five consecutive cards of different suits

Scenario: Success Is Straight
Given I have a Classifier Object with:
	|AS, 10C, JH, QD, KS|
And I call get Classifier::is_straight()
Then I should receive True


Scenario: Failed Is Straight
Given I have a Classifier Object with:
	|AS, 9C, JH, QD, KS|
And I call get Classifier::is_straight()
Then I should receive False

```


### Classifier::is_straight_flush

```
Feature: Classifier::is_straight_flush()
Any straight with all five cards of the same suit.

Scenario: Success Is Straight
Given I have a Classifier Object 
And Classifier.is_flush return True
And Classifier.is_straight return True
And I call get Classifier::is_straight_flush()
Then I should receive True


Scenario: FAiled Not A Flush
Given I have a Classifier Object 
And Classifier.is_flush return False
And Classifier.is_straight return True
And I call get Classifier::is_straight_flush()
Then I should receive False


Scenario: FAiled Not A Straight
Given I have a Classifier Object 
And Classifier.is_flush return True
And Classifier.is_straight return False
And I call get Classifier::is_straight_flush()
Then I should receive False


Scenario: Neither Strait nor Flush
Given I have a Classifier Object 
And Classifier.is_flush return False
And Classifier.is_straight return False
And I call get Classifier::is_straight_flush()
Then I should receive False

```


### Classifier::is_royal_flush

```
Feature: Classifier::is_royal_flush()
Any straight with all five cards of the same suit.

Scenario: Success Is Straight
Given I have a Classifier Object 
And Classifier.is_straight_flush return True
And Classifier.get_high return 14
And I call get Classifier::is_royal_flush()
Then I should receive True


Scenario: Faild Is Not Straight Flush
Given I have a Classifier Object 
And Classifier.is_straight_flush return False
And Classifier.get_high return 14
And I call get Classifier::is_royal_flush()
Then I should receive False


Scenario: Faild Is High Enough
Given I have a Classifier Object 
And Classifier.is_straight_flush return True
And Classifier.get_high return 10
And I call get Classifier::is_royal_flush()
Then I should receive False
```

# Installation 

The app is easily install & configured using Docker, all packages and configurations will automatically be deployed. 

It will configure the following: 
1. Django3 + Django Rest Framework + Python3
2. Postgress Service 

Follow the instructions below to run the service.

### Step 1: Intall Docker Desktop 

Follow the instructions for your Operating System, if you don't already have Docker Desktop

[Docker Desktop - Mac](https://docs.docker.com/desktop/install/mac-install/)

[Docker Desktop - Windows](https://docs.docker.com/desktop/install/windows/)

[Docker Desktop - Ubuntu](https://docs.docker.com/desktop/install/ubuntu/)


### Step 2: Clone & Configure Container 

Once docker is installed you may clone and configure the container.

```sh=
#Clone & Start Docker Container
git clone git@github.com:gminator/poker.git
cd poker
docker-compose up -d
docker exec -it django python manage.py migrate
```

### Step 3: Run Unit Tests
```sh=
docker exec -it django python manage.py test
```


### Step 4: Authentication & Quey API 
```sh
docker exec -it django python manage.py createsuperuser --noinput --username admin --email giovann.adonis@gmail.com
docker exec -it django python manage.py drf_create_token admin

```


#### Full House
```sh
curl --location --request POST 'http://0.0.0.0:8000/classify/' \
--header 'Authorization: Token <Copy-Token-Id-Here>' \
--header 'Content-Type: application/json' \
--data-raw '{"cards" : "5C,5D,5S,10H,10C"}' | python -m json.tool
```


#### Royal Flush 
```sh
curl --location --request POST 'http://0.0.0.0:8000/classify/' \
--header 'Authorization: Token <Copy-Token-Id-Here>' \
--header 'Content-Type: application/json' \
--data-raw '{"cards" : "10S,QS,KS,AS,JS"}' | python -m json.tool
```


#### 4 Of A Kind  
```sh
curl --location --request POST 'http://0.0.0.0:8000/classify/' \
--header 'Authorization: Token <Copy-Token-Id-Here>' \
--header 'Content-Type: application/json' \
--data-raw '{"cards" : "10S,10D,5S,10H,10C"}' | python -m json.tool
```

