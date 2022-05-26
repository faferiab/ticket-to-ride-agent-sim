from .enums import Colour


class Route():
  """Represent a game route"""
  def __init__(self, start, end, cost, colour):
    self.__colour__ : Colour = colour
    self.__start__ = start
    self.__end__ = end
    self.__cost__ : int = cost

  def start(self):
    '''Route start'''
    return self.__start__

  def end(self):
    '''Route end'''
    return self.__end__

  def cost(self):
    '''Route cost'''
    return self.__cost__

  def colour(self):
    '''Route colour'''
    return self.__colour__

  def __str__(self) -> str:
      return ("(" + self.__start__ + ", " + self.__end__ + ", " 
              + str(self.__cost__) + ", " + str(self.__colour__) + ")")

  def __eq__(self, __o: object) -> bool:
    if isinstance(__o, Route):
      return (self.start() == __o.start() 
      and self.end() == __o.end()
      and self.colour() == __o.colour()
      and self.cost() == __o.cost())
    return False
