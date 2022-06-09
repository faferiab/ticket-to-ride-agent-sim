import unittest

from src.game import *
from src.model import *
from src.player import *


class TestingGame(unittest.TestCase):
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
    dict_player, count_rounds = match.run_game()
    assert count_rounds
    assert dict_player

if __name__ == '__main__':
    unittest.main()
