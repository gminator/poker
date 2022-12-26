

class GameException(Exception):pass

class InvalidSuitException(GameException):
	"""
	Thrown if a card is given 
	and invalid suit designation
	"""


class InvalidCardNumberException(GameException):
	"""
	Thrown if a card designation
	is too low or to high
	"""


class InvalidCardStringException(GameException):
	"""
	Thrown if when card string is not valud
	"""


class InvalidHandString(GameException):
	"""
	Thrown if when card string is not valud
	"""