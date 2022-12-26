# Table of Contents  
[Headers](#headers)  
[Emphasis](#emphasis)  

# The Poker Test
The purpose of this Project is to demostrate my compencies in Python, OOP, SOLID.

It show how I go about planning, building and testing my work. 

# Brief 

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

### Considerations and Assumptions

### Framework Choice 

Its not entirely neccasry to use a Framework like Django. I chose this to show that I have a grounded understanding of the elements of frameowrks (Routing, ORM, MVC, Serializers, etc) these exist in almost all frameworks irrespecitve of lanuage. 

### Business Rules 

There a rules that I will negate for the purpose of the excercise. 

#### The Joker 
The Joker is typically used as a wild card, players can use this stand in for cards of their choice. I will not be using this card in my evaluations as it will require additional user input, and is not critical for demostrating a working understanding of the principles I wish to demonstrate

#### The Ace 
The ace card can represent boht 1 & 14, aslo depending on the players choice. For purpose of the test it will always represent the highest available card. 

### Overview 
The solution consists of 2 basic classess. 

#### Card

Cards are complex in that they can be represented by letters (K,Q,J,A) that have a numeric value. The class will store these properties that can later be used for classification, validation and evaluation. 

|Cards| | |
|-------|-| -|
| **type** | **Name** | **Description** |
| **enum** | suit| Unicode Symbol For Cards|
| **int** | number | Numeric Number Of Card |
| **int** | letter |Alphabetical designation of card |
| **boolean** | validate() | Check That card meets required criteria |
