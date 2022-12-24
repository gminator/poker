# Porker Test
The purpose of this Project is to demostrate my compencies in Python, OOP, SOLID.

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

The code will be written inline with the *SOLID principle* honoring single respobsibiliy, open close principle and interface segregation and effort to write DRY scalable code. 

Other principle being applied also include Domain Driven Design even at this level of code. This important to faciliate good TDD or Unit test, having fat or ambigious functions  makes testing difficult. 


The acceptance criteria is written in Gherkin, I've found that this is easier for stakeholder to validate assumptions against and for developers to write unit tests.

### Overview 
The solution consists of 2 basic classess. 

| Type | Name | Description |
|-------|-| -|
| [string] suit| Symbol For Suit |
| [int] number |Numeric value of this card |
