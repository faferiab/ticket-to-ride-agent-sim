import unittest

from src.game import *
from src.model import *
from src.player import *

from .cards_routes import cards as ListCards, routes as ListRoutes

class TestingGame(unittest.TestCase):

  def test_score_path_single_route(self):
    routes = [Route('S1', 'E1', 2, Colour.ANY),
      Route('S2', 'E1', 2, Colour.ANY)]
    game = Game(Board([], []))
    match = Match(game, [])
    assert match.score_path(routes) == 4

  def test_score_path_multiple_route(self):
    routes = [Route('S1', 'E1', 2, Colour.ANY),
      Route('S2', 'E2', 2, Colour.ANY),
      Route('S3', 'E2', 2, Colour.ANY)]
    game = Game(Board([], []))
    match = Match(game, [])
    assert match.score_path(routes) == 4

  def test_score_route_simple(self):
    routes = [Route('S1', 'E1', 5, Colour.ANY)]
    game = Game(Board([], []))
    match = Match(game, [])
    assert match.score_routes(routes) == 15

  def test_score_route_simple(self):
    routes = [Route('S1', 'E1', 2, Colour.ANY), 
    Route('S2', 'E2', 2, Colour.ANY)]
    game = Game(Board([], []))
    match = Match(game, [])
    assert match.score_routes(routes) == 4

  def test_simple_match(self):
    routes = [Route('S1', 'S2', 2, Colour.ANY), Route('S2', 'S3', 2, Colour.ANY)
    ,Route('S3', 'S4', 2, Colour.ANY), Route('S4', 'S5', 2, Colour.ANY)
    ,Route('S5', 'S6', 2, Colour.ANY), Route('S6', 'S7', 2, Colour.ANY)
    ,Route('S7', 'S1', 2, Colour.ANY), Route('S2', 'S5', 2, Colour.ANY)]
    cards = []
    for colour, times in [(Colour.RED, 15), (Colour.BLACK, 19)]:
      for _ in range(times):
        cards.append(Card(colour))
    game = Game(Board(cards, routes))
    players = [EagerRoutePlayer('player1', 4, None), ExpensiveRoutePlayer('player2', 4, None),
    LongestRoutePlayer('player3', 4, None)]
    match = Match(game, players)
    #dict_player, count_rounds = match.run_game()
    #assert count_rounds
    #assert dict_player
    pass
  
  def test_full_match(self):
    routes = ListRoutes
    cards = ListCards
    game = Game(Board(cards, routes))
    players = [EagerRoutePlayer('player1', 45, None), ExpensiveRoutePlayer('player2', 45, None),
    LongestRoutePlayer('player3', 45, None)]
    match = Match(game, players)
    dict_player, count_rounds = match.run_game()
    print((dict_player, count_rounds))
    assert count_rounds
    assert dict_player

if __name__ == '__main__':
    unittest.main()
