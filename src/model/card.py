from .enums import Colour, Status


class Card():
  """Represent a game card"""
  def __init__(self, colour, status = Status.CLOSE):
    self.__colour__ : Colour = colour
    self.__status__ : Status = status

  def colour(self):
    """Card colour"""
    return self.__colour__

  def status(self):
    """Card status"""
    return self.__status__

  def set_status(self, value):
    """New card status"""
    self.__status__ = value

  def __str__(self) -> str:
      return "(" + str(self.__colour__) + ", " + str(self.__status__) + ")"

  def __eq__(self, __o: object) -> bool:
    if isinstance(__o, Card):
      return (self.colour() == __o.colour()
      and self.status() == __o.status())
    return False
