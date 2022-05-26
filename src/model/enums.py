from enum import Enum


class Colour(Enum):
  """Represent the status of a game card"""
  PINK = 'PINK'
  WHITE = 'WHITE'
  BLUE = 'BLUE'
  YELLOW = 'YELLOW'
  ORANGE = 'ORANGE'
  BLACK = 'BLACK'
  RED = 'RED'
  GREEN = 'GREEN'
  ANY = 'ANY'

class Status(Enum):
  """Represent a color of the game"""
  OPEN = 1
  CLOSE = 2
  DISCARD = 3

class Action(Enum):
  """Represent a color of the game"""
  TAKE = 'TAKE'
  BUY = 'BUY'
