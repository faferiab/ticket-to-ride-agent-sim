
from enum import Enum
from typing import List

from src.model import Card, Colour, Route
from src.game import Game


class Upgrade(Enum):
    ADD = 'ADD',
    REMOVE = 'REMOVE'

class Player():
  """Represent a game player"""

  def __init__(self, name: str, train_counter: int, initial: List[Card]):
    self.name = name
    self.__train_counter__ = 0 if not train_counter else train_counter
    self.hand = initial
    # V,K = Colour: Qty
    self.cards_freq = {}
    self.owned_routes = []
    if initial:
      for card in initial:
        self.add_card(card.colour())

  def action(self, state):
    """Return one possible action for player"""
    raise NotImplementedError

  def result(self, state, action):
    """Return one possible action for player"""
    raise NotImplementedError

  def is_goal(self):
    return self.__train_counter__ == 0

  def add_card(self, colour: Colour):
    self.__card_freq_update__(colour, Upgrade.ADD)

  def remove_card(self, colour: Colour):
    self.__card_freq_update__(colour, Upgrade.REMOVE)

  def __card_freq_update__(self, colour: Colour, upgrade: Upgrade):
    """Update de frequency card dict"""
    if upgrade == Upgrade.ADD:
      if not self.cards_freq.get(colour):
        self.cards_freq[colour] = 0
      self.cards_freq[colour] += 1
    if upgrade == Upgrade.REMOVE:
      self.cards_freq[colour] -= 1
      if self.cards_freq[colour] == 0:
        self.cards_freq.pop(colour)



  def action_buy_route(self, game: Game, route: Route):
    """Buy a train route returning the matching cards in hand"""
    cost, colour = route.cost(), route.colour()
    cards: List[Card] = list(
        filter(lambda card: card.colour() == colour, self.hand))
    cards.extend(
        list(filter(lambda card: card.colour() == Colour.ANY, self.hand)))
    game.buy_route(cards[0:cost], route)
    for delete_card in cards[0:cost]:
        self.hand.remove(delete_card)
        self.remove_card(delete_card.colour())
    self.__train_counter__ -= cost
    self.owned_routes.append(route)
