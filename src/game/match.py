from typing import List
from src.game import Game
from src.player.player import Player


class Match():
  """Represent a match of a Game between Players"""
  def __init__(self, game: Game, players: List[Player]):
    self.game = game
    self.players = players
    self.end_game = False
    self.rounds = 0
  
  def run_game(self):
    idx = 0
    game = self.game
    while not self.end_game:
      player = self.players[idx % len(self.players)]
      action = player.action(game)
      player.result(game, action)
      self.end_game = player.is_goal()
      idx += 1
    self.rounds = idx
    return self.score_game(self.game, self.players), self.rounds
  
  def score_game(self, game: Game, players: List[Player]):
    """Return a dictionary with the score of the game"""
    score = {}
    for player in players:
      score[player.name] = game.score(player.owned_routes)
    return score

  def player_turn(self, player: Player, game: Game):
    """Execute every player action on game"""
    return player.result(game, player.action(game))
