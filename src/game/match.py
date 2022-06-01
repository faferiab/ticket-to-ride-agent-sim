class Match():
  """Represent a match of a Game between Players"""
  def __init__(self, game, players=None, **kwds):
    self.game = game
    self.players = players
    self.end_game = False
    self.rounds = 0
  
  def run_game(self):
    idx = 0
    game = self.game
    while self.end_game:
      player = self.players[idx % len(self.players)]
      self.end_game = player.is_goal
      game = self.player_turn(player, game)
      idx += 1
    self.rounds = idx
    return self.score_game(self.game, self.players), self.rounds
  
  def score_game(self, game, players):
    """Return a dictionary with the score of the game"""
    score = {}
    for player in players:
      score[player.name] = game.score(player.segments)
    return score

  def player_turn(Player, game):
    """Execute every player action on game"""
    return Player.result(game, Player.action(game))
