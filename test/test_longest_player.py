import unittest

from src.game import *
from src.model import *
from src.player import LongestRoutePlayer


class TestingExpensivePlayer(unittest.TestCase):

  def test_nearest_routes_first_level(self):
    game = Game(Board([], [Route('S1', 'E1', 5, Colour.BLACK), 
      Route('S2', 'E2', 2, Colour.ANY)]))
    player = LongestRoutePlayer('Player1', 5, None)
    player.owned_routes = [Route('S1', 'EX', 5, Colour.BLACK)]
    assert len(player.get_nearest_routes(game)) == 1

  def test_nearest_routes_second_level(self):
    game = Game(Board([], [Route('SX', 'EX', 5, Colour.BLACK), 
      Route('S2', 'E2', 2, Colour.ANY)]))
    player = LongestRoutePlayer('Player1', 5, None)
    player.owned_routes = [Route('S1', 'E1', 5, Colour.BLACK),
    Route('S2', 'E2', 5, Colour.BLACK), Route('S3', 'E3', 5, Colour.BLACK)]
    assert len(player.get_nearest_routes(game)) == 1

  def test_nearest_routes_none(self):
    game = Game(Board([], [Route('SX', 'EX', 5, Colour.BLACK)]))
    player = LongestRoutePlayer('Player1', 5, None)
    player.owned_routes = [Route('S1', 'E1', 5, Colour.BLACK),
    Route('S2', 'E2', 5, Colour.BLACK)]
    assert len(player.get_nearest_routes(game)) == 0

  def test_get_reward_route_list(self):
    card_freq = {Colour.BLACK: 3, Colour.RED: 2}
    player = LongestRoutePlayer('Player1', 5, None)
    reward = player.get_reward_route_list([Route('S', 'E', 3, Colour.BLACK),
      Route('S', 'E', 2, Colour.BLACK)], card_freq)
    route: Route
    route, metric, available = reward[0]
    assert len(reward)
    assert metric == 2
    assert available == True
    assert route.colour() == Colour.BLACK

  def test_get_buyable_route(self):
    card_freq = {Colour.BLACK: 4, Colour.RED: 2}
    game = Game(Board([], [Route('S', 'E', 5, Colour.BLACK), 
      Route('S', 'E', 2, Colour.RED)]))
    player = LongestRoutePlayer('Player1', 5, None)
    player.owned_routes = [Route('S', 'E2', 5, Colour.RED)]
    assert player.get_buyable_route(game, card_freq)

  def test_get_buyable_route_none_cards(self):
    card_freq = {Colour.BLACK: 4, Colour.RED: 2}
    game = Game(Board([], [Route('S', 'E', 5, Colour.BLACK), 
      Route('S', 'E', 3, Colour.RED)]))
    player = LongestRoutePlayer('Player1', 5, None)
    player.owned_routes = [Route('S', 'E2', 5, Colour.RED)]
    assert not player.get_buyable_route(game, card_freq)

  def test_get_buyable_route_none_routes(self):
    card_freq = {Colour.BLACK: 4, Colour.RED: 2}
    game = Game(Board([], [Route('SX', 'E', 5, Colour.BLACK), 
      Route('SY', 'E', 3, Colour.RED)]))
    player = LongestRoutePlayer('Player1', 5, None)
    player.owned_routes = [Route('S', 'E2', 5, Colour.RED)]
    assert not player.get_buyable_route(game, card_freq)

  def test_get_buyable_route_initial(self):
    card_freq = {Colour.RED: 3}
    game = Game(Board([], [Route('SY', 'E', 3, Colour.RED)]))
    player = LongestRoutePlayer('Player1', 5, None)
    assert player.get_buyable_route(game, card_freq)

  def test_get_buyable_route_over_none(self):
    card_freq = {Colour.RED: 3}
    game = Game(Board([], [Route('SY', 'E', 3, Colour.RED)]))
    player = LongestRoutePlayer('Player1', 2, None)
    assert not player.get_buyable_route(game, card_freq)

if __name__ == '__main__':
    unittest.main()
