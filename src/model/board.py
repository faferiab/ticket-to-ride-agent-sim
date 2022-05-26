from typing import List

from .card import Card
from .route import Route


class Board():
  def __init__(self, cards: List[Card], routes: List[Route]):
    self.__cards__= cards
    self.__routes__= routes

  def cards(self):
    return self.__cards__

  def routes(self):
    return self.__routes__
