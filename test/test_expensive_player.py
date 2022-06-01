import unittest

from src.game import *
from src.model import *
from src.player import ExpensiveRoutePlayer


class TestingExpensivePlayer(unittest.TestCase):

  def test_longest_available_routes(self):
    game = Game(Board([], [Route('S', 'E', 5, Colour.BLACK), 
      Route('S', 'E', 2, Colour.ANY)]))
    player = ExpensiveRoutePlayer('Player1', 5, None)
    assert 0 < len(player.get_longest_available_routes(game, 1)) < 2

  def test_get_reward_route_list(self):
    card_freq = {Colour.BLACK: 2, Colour.RED: 2}
    game = Game(Board([], []))
    player = ExpensiveRoutePlayer('Player1', 5, None)
    reward = player.get_reward_route_list([Route('S', 'E', 2, Colour.BLACK)], card_freq, game)
    *_, metric, available = reward[0]
    assert len(reward)
    assert metric == 2
    assert available == True

  def test_get_reward_route_list_multiple(self):
    card_freq = {Colour.BLACK: 2, Colour.RED: 3}
    game = Game(Board([], []))
    player = ExpensiveRoutePlayer('Player1', 5, None)
    reward = player.get_reward_route_list([Route('S', 'E', 5, Colour.BLACK), 
      Route('S1', 'E1', 3, Colour.RED)], card_freq, game)
    *_, metric, available = reward[0]
    assert len(reward)
    assert metric == 4
    assert available == True

  def test_get_reward_route_list_wcolour_any(self):
    card_freq = {Colour.BLACK: 1, Colour.RED: 2, Colour.ANY: 1}
    game = Game(Board([], []))
    player = ExpensiveRoutePlayer('Player1', 5, None)
    reward = player.get_reward_route_list([Route('S', 'E', 5, Colour.BLACK), 
      Route('S1', 'E1', 3, Colour.RED)], card_freq, game)
    *_, metric, available = reward[0]
    assert len(reward)
    assert metric == 4
    assert available == True

  def test_buyable_route(self):
    card_freq = {Colour.BLACK: 4, Colour.RED: 2}
    game = Game(Board([], [Route('S', 'E', 5, Colour.BLACK), 
      Route('S', 'E', 2, Colour.RED)]))
    player = ExpensiveRoutePlayer('Player1', 5, None)
    assert not player.get_buyable_route(game, card_freq)

  def test_get_card(self):
    card_freq = {Colour.BLACK: 4}
    game = Game(Board([Card(Colour.BLACK, Status.OPEN)], 
      [Route('S', 'E', 5, Colour.BLACK)]))
    player = ExpensiveRoutePlayer('Player1', 5, None)
    card : Card = player.action_get_card(game, card_freq)
    assert card.colour() == Colour.BLACK

if __name__ == '__main__':
    unittest.main()
