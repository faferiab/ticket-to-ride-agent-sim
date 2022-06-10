import random
from typing import List, Tuple

from src.model import Board, Card, Colour, Route, Status


class Game():
  """Represent the game and its behaviour"""
  def __init__(self, board: Board):
    self.cards : List[Card] = board.cards()
    self.routes : List[Route] = board.routes()
    self.board = board
    if len(self.cards) > 5:
      for _ in range(5):
        random.choice(self.cards).set_status(Status.OPEN)


  def deal_open_card(self, card_selected: Card):
    """Return an open card located in the index position""" 
    if self.get_open_cards().count(card_selected):
      self.cards.remove(card_selected)
    if not self.get_close_cards():
      self.reshufle_discard_cards()
    random.choice(self.get_close_cards()).set_status(Status.OPEN)
    return card_selected

  def deal_close_card(self):
    """Return an close card"""
    if not self.get_close_cards():
      self.reshufle_discard_cards()
    return_card = random.choice(self.get_close_cards())
    self.cards.remove(return_card)
    return_card.set_status(Status.OPEN)
    return return_card

  def reshufle_discard_cards(self):
    for card in self.__cards_by_status__(Status.DISCARD):
        card.set_status(Status.CLOSE)
  
  def get_routes(self):
    """Return a new list of available train segments"""
    return [x for x in self.routes]
  
  def buy_route(self, cards: List[Card], route: Route):
    """Buy a train route using the cards"""
    cost, colour = route.cost(), route.colour()
    cost_match = len(cards) == cost
    colour_match = False
    if colour == Colour.ANY:
      colour_match = all(card.colour() == cards[0].colour() or card.colour() == Colour.ANY for card in cards)
    else :
      colour_match = all(card.colour() == colour or card.colour() == Colour.ANY for card in cards)
    route_match = self.routes.count(route)
    if(cost_match and colour_match and route_match):
      for card in cards:
        card.set_status(Status.DISCARD)
        self.cards.append(card)
      self.routes.remove(route)
      return route
    print(self.__class__, cost_match, colour_match, route_match, route, [(x.colour()) for x in cards])
    raise Exception("Invalid cards")

  def __cards_by_status__(self, Status):
    """Return a new list of cards filter by status"""
    return [x for x in self.cards if x.status() == Status]

  def get_open_cards(self):
    """Return a list of open cards"""
    return self.__cards_by_status__(Status.OPEN)

  def get_close_cards(self):
    """Return a list of close cards"""
    return self.__cards_by_status__(Status.CLOSE)

  def get_discard_cards(self):
    """Return a list of discard cards"""
    return self.__cards_by_status__(Status.DISCARD)

  def points(self, distance: int):
    """Return the score of a route"""
    x = [0, 1, 2, 4, 7, 10, 15]
    return x[distance]
