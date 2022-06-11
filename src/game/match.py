from typing import List, Tuple
from src.game import Game
from src.model.enums import Action, Status
from src.model.route import Route
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
    return self.score_game(self.players), self.rounds
  
  def score_game(self, players: List[Player]):
    """Return a dictionary with the score of the game"""
    score = {}
    path_bonus = (None, 0)
    for player in players:
      score_path, score[player.name] = self.score(player.owned_routes)
      if path_bonus[1] < score_path:
        path_bonus = (player.name, score_path)
    score[path_bonus[0]] += 10
    return score

  def player_turn(self, player: Player, game: Game):
    """Execute every player action on game"""
    return player.result(game, player.action(game))

  def score(self, routes: List[Route]):
    """Return the score of a player"""
    return self.score_path(routes), self.score_routes(routes)
  
  def score_routes(self, routes: List[Route]):    
    """Return the score of a player by summing all the routes"""
    score = 0
    for route in routes:
      score += self.game.points(route.cost())
    return score

  def score_path(self, routes: List[Route]):
    """Return the score of a player's longest path"""
    max_number = 0
    for path in self.group_paths(routes):
      for station in self.get_origin_stations(path):
        max_number = max(self.search_longest_path(path, station), max_number)
    return max_number

  def group_paths(self, routes: List[Route]):
    """Return a list of lists each one with a connected routes"""
    result : List[List[Tuple]] = []
    station_stack = []
    links = routes.copy()
    group = []
    while len(links)>0:
      if len(station_stack) == 0:
        link = links.pop()
        station_stack.append(link.start())
        station_stack.append(link.end())
        result.append(group.copy())
        group = [(link.start(), link.end(), link.cost())]
      station = station_stack.pop(0)
      for link in list(filter(lambda x: [x.start(), x.end()].count(station) > 0, links)):
        links.remove(link)
        start, end = link.start(), link.end()
        group.append((start, end, link.cost()))
        station_stack.append(start if start != station else end)
    result.append(group)
    result.pop(0)
    return result

  def get_origin_stations(self, routes: List[Tuple]):
    """Return the origin stations for a routes list"""
    counter={}
    for segment in routes:
      start, end, *_ = segment
      value = counter.get(start)
      if value == None:
        value = 0
      counter[start] = value + 1
      value = counter.get(end)
      if value == None:
        value = 0
      counter[end] = value + 1
    origins : List[Tuple] = list(filter(lambda x: counter.get(x) == 1, counter.keys()))
    if not len(origins):
      min_size = (min(counter.values()))
      origins = list(filter(lambda x: counter.get(x) == min_size, counter.keys()))
      origins = [origins.pop()]
    return origins

  def search_longest_path(self, routes: List[Tuple], station: Tuple, count=0, max_number=0):
    """Return the longest path for a segment list"""
    match_routes = list(filter(lambda x: (x[0], x[1]).count(station), routes))
    if not len(match_routes):
      return max(max_number, count)
    for node in match_routes:
      new_routes = routes.copy()
      new_routes.remove(node)
      start, end, cost = node
      new_station = start if start != station else end
      max_number = self.search_longest_path(new_routes, new_station, count + cost, max_number)
    return max_number

