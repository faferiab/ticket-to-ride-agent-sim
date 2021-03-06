import unittest

from src.game import *
from src.model import *


class TestingGame(unittest.TestCase):
  def test_deal_open_card(self):
    card_open = Card(Colour.ANY, Status.OPEN)
    card_close = Card(Colour.ANY, Status.CLOSE)
    game = Game(Board([card_open, card_close], []))
    card = game.deal_open_card(card_open)
    assert card == card_open
    assert len(game.cards) == 1
    assert all([x.status() == Status.OPEN for x in game.cards])

  def test_deal_open_card_wdiscard(self):
    card_open = Card(Colour.ANY, Status.OPEN)
    card_discard = Card(Colour.ANY, Status.DISCARD)
    game = Game(Board([card_open, card_discard], []))
    game.deal_open_card(card_open)
    assert len(game.cards) == 1
    assert all([x.status() == Status.OPEN for x in game.cards])

  def test_deal_close_card(self):
    card_close = Card(Colour.ANY, Status.CLOSE)
    game = Game(Board([card_close], []))
    card = game.deal_close_card()
    assert card.status() == Status.OPEN
    assert not game.cards

  def test_deal_close_card_wdiscard(self):
    card_discard = Card(Colour.ANY, Status.DISCARD)
    game = Game(Board([card_discard], []))
    card = game.deal_close_card()
    assert card.status() == Status.OPEN
    assert not game.cards
  
  def test_buy_route_wcolour(self):
    route = Route('start', 'end', 2, Colour.BLACK)
    route_buy = Route('start', 'end', 2, Colour.BLACK)
    card_open1 = Card(Colour.BLACK, Status.OPEN)
    card_open2 = Card(Colour.BLACK, Status.OPEN)
    game = Game(Board([], [route]))
    game.buy_route([card_open1, card_open2], route_buy)
    assert len(game.cards) == 2
    assert not game.routes

  def test_buy_route_colour_any(self):
    route = Route('start', 'end', 2, Colour.ANY)
    route_buy = Route('start', 'end', 2, Colour.ANY)
    card_open1 = Card(Colour.BLACK, Status.OPEN)
    card_open2 = Card(Colour.BLACK, Status.OPEN)
    game = Game(Board([], [route]))
    game.buy_route([card_open1, card_open2], route_buy)
    assert len(game.cards) == 2
    assert not game.routes

if __name__ == '__main__':
    unittest.main()
