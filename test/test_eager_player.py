import unittest

from src.game import *
from src.model import *
from src.player import EagerRoutePlayer


class TestingEagerPlayer(unittest.TestCase):
  def test_buyable_routes_same_color(self):
    card_freq = {Colour.BLACK: 5, Colour.RED: 2}
    game = Game(Board([], [Route('S', 'E', 5, Colour.BLACK)]))
    player = EagerRoutePlayer('Player1', 5, None)
    assert len(player.get_buyable_routes(game, card_freq)) > 0

  def test_buyable_routes_any_color_in_hand(self):
    card_freq = {Colour.ANY: 5, Colour.RED: 2}
    game = Game(Board([], [Route('S', 'E', 5, Colour.BLACK)]))
    player = EagerRoutePlayer('Player1', 5, None)
    assert len(player.get_buyable_routes(game, card_freq)) > 0

  def test_buyable_routes_any_color_in_route(self):
    card_freq = {Colour.BLUE: 5, Colour.BLACK: 2}
    game = Game(Board([], [Route('S', 'E', 5, Colour.ANY)]))
    player = EagerRoutePlayer('Player1', 5, None)
    assert len(player.get_buyable_routes(game, card_freq)) > 0

  def test_buyable_routes_mixed_color_in_hand(self):
    card_freq = {Colour.ANY: 3, Colour.RED: 2}
    game = Game(Board([], [Route('S', 'E', 5, Colour.RED)]))
    player = EagerRoutePlayer('Player1', 5, None)
    assert len(player.get_buyable_routes(game, card_freq)) > 0

  def test_not_buyable_routes_mixed_color_in_hand(self):
    card_freq = {Colour.ANY: 1, Colour.RED: 2}
    game = Game(Board([], [Route('S', 'E', 5, Colour.RED)]))
    player = EagerRoutePlayer('Player1', None, None)
    assert len(player.get_buyable_routes(game, card_freq)) == 0

  def test_action_get_card(self):
    card_freq = {Colour.ANY: 1, Colour.RED: 2}
    game = Game(Board([Card(Colour.RED, Status.OPEN), 
                       Card(Colour.BLUE, Status.OPEN)], []))
    player = EagerRoutePlayer('Player1', None, None)
    assert player.action_get_card(game, card_freq).colour() == Colour.RED

  def test_action_get_most_common_card(self):
    card_freq = {Colour.BLACK: 1, Colour.RED: 2}
    game = Game(Board([Card(Colour.RED, Status.OPEN), 
                       Card(Colour.BLACK, Status.OPEN)], []))
    player = EagerRoutePlayer('Player1', None, None)
    assert player.action_get_card(game, card_freq).colour() == Colour.RED

  def test_action_get_not_found_card(self):
    card_freq = {Colour.BLACK: 1, Colour.RED: 2}
    game = Game(Board([Card(Colour.BLUE, Status.OPEN), 
                       Card(Colour.BLUE, Status.OPEN)], []))
    player = EagerRoutePlayer('Player1', None, None)
    assert player.action_get_card(game, card_freq) == None

  def test_result_get_card(self):
    game = Game(Board([Card(Colour.BLUE, Status.OPEN), 
                       Card(Colour.RED, Status.OPEN),
                       Card(Colour.BLACK, Status.CLOSE),
                       Card(Colour.BLACK, Status.CLOSE)], []))
    player = EagerRoutePlayer('Player1', None, 
    [Card(Colour.BLUE, Status.OPEN), Card(Colour.BLUE, Status.OPEN)])
    player.result(game, player.action(game))
    assert len(game.cards) == 2
    assert len(player.hand) == 4

  def test_result_get_route(self):
    game = Game(Board([], [Route('s', 'e', 2, Colour.BLUE)]))
    player = EagerRoutePlayer('Player1', 2, 
    [Card(Colour.BLUE, Status.OPEN), Card(Colour.BLUE, Status.OPEN)])
    player.result(game, player.action(game))
    assert not len(game.routes)
    assert len(game.cards)
    assert player.is_goal()

  def test_result_not_get_route_expensive(self):
    game = Game(Board([Card(Colour.BLUE, Status.CLOSE), 
                       Card(Colour.RED, Status.CLOSE)]
                       , [Route('s', 'e', 2, Colour.BLUE)]))
    player = EagerRoutePlayer('Player1', 1, 
    [Card(Colour.BLUE, Status.OPEN), Card(Colour.BLUE, Status.OPEN)])
    player.result(game, player.action(game))
    assert not player.is_goal()
  
if __name__ == '__main__':
    unittest.main()
