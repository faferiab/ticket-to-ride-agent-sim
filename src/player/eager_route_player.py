import operator
from enum import Enum
from typing import Dict, List, Tuple

from src.game import Game
from src.model import Action, Card, Colour, Route

from .player import Player


class Upgrade(Enum):
  ADD = 'ADD',
  REMOVE = 'REMOVE'

class EagerRoutePlayer(Player):
  #V,K = Colour: Qty
  cards_freq = {}
  def __init__(self, name: str, train_counter: int, initial: List[Card]):
    super().__init__(name, train_counter, initial)
    if initial:
      for card in initial:
        self.card_freq_update(self.cards_freq, card.colour(), Upgrade.ADD)

  def get_buyable_routes(self, game: Game, cards_freq: Dict):
    """Return all buyable routes based on the cards in players hand"""
    result : List[Route] = []
    count_wildcard = (0 if cards_freq.get(Colour.ANY) == None 
                      else cards_freq.get(Colour.ANY))
    for route in game.get_routes():
      cost, colour_route = route.cost(), route.colour()
      if any((colour_route == colour_card or colour_route == Colour.ANY 
              or colour_card == Colour.ANY) 
      and ((colour_card == Colour.ANY and cards_freq[colour_card] >= (cost))
      or (colour_card != Colour.ANY and cards_freq[colour_card] >= (cost-count_wildcard)))
      for colour_card in cards_freq.keys()):
        result.append(route)
        continue
    return result

  def action_get_card(self, game: Game, cards_freq: Dict):
    """Return a pickable card based on cards players hand else return None"""
    for card_colour, _ in sorted(cards_freq.items(), key=operator.itemgetter(1), 
                            reverse=True):
      available_cards : List[Card] = list(
          filter(lambda card: card.colour() == card_colour or 
                 card.colour() == Colour.ANY, game.get_open_cards()))
      if len(available_cards):
        return available_cards.pop(0)
    return None

  def action_buy_route(self, game: Game, action_data: Tuple):
    """Buy a train route returning the matching cards in hand"""
    *_, cost, colour = action_data
    cards : List[Card] = list(filter(lambda card: card.colour() == colour, self.hand))
    cards.extend(list(filter(lambda card: card.colour() == Colour.ANY, self.hand)))
    game.buy_route(cards[0:cost], action_data)
    for delete_card in cards[0:cost]:
      self.hand.remove(delete_card)
      self.card_freq_update(self.cards_freq, delete_card.colour(), Upgrade.REMOVE)

  def card_freq_update(self, cards_freq: Dict, colour: Colour, upgrade: Upgrade):
    """Update de frequency card dict"""
    if upgrade == Upgrade.ADD:
      if not cards_freq.get(colour):
        cards_freq[colour] = 0
      cards_freq[colour] += 1
    if upgrade == Upgrade.REMOVE:
      cards_freq[colour] -= 1
      if cards_freq[colour] == 0:
        cards_freq.pop(colour)

  def action(self, game):
    """If the player can buy a route return BUY else the player take a card 
    and return TAKE"""
    available_routes = self.get_buyable_routes(game, self.cards_freq)
    if len(available_routes) > 0:
      return (Action.BUY, available_routes.pop())
    return (Action.TAKE, None)

  def result(self, game: Game, action: Tuple):
    action_type, action_data = action
    if action_type == Action.BUY:
      self.action_buy_route(game, action_data)
    elif action_type == Action.TAKE:
      for _ in range(2):
        card = self.action_get_card(game, self.cards_freq)
        card = game.deal_close_card() if not card else game.deal_open_card(card)
        self.hand.append(card)
        self.card_freq_update(self.cards_freq, card.colour(), Upgrade.ADD)
