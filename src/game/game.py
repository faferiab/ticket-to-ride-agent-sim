import random
from typing import List, Tuple

from src.model import Board, Card, Colour, Route, Status


class Game():
  """Represent the game and its behaviour"""
  def __init__(self, board: Board):
    self.cards : List[Card] = board.cards()
    self.routes : List[Route] = board.routes()
    self.board = board
    if len(self.cards) > 5:
      for _ in range(5):
        random.choice(self.cards).set_status(Status.OPEN)


  def deal_open_card(self, card_selected: Card):
    """Return an open card located in the index position""" 
    if self.get_open_cards().count(card_selected):
      self.cards.remove(card_selected)
    if not self.get_close_cards():
      self.reshufle_discard_cards()
    random.choice(self.get_close_cards()).set_status(Status.OPEN)
    return card_selected

  def deal_close_card(self):
    """Return an close card"""
    if not self.get_close_cards():
      self.reshufle_discard_cards()
    return_card = random.choice(self.get_close_cards())
    self.cards.remove(return_card)
    return_card.set_status(Status.OPEN)
    return return_card

  def reshufle_discard_cards(self):
    for card in self.__cards_by_status__(Status.DISCARD):
        card.set_status(Status.CLOSE)
  
  def get_routes(self):
    """Return a new list of available train segments"""
    return [x for x in self.routes]
  
  def buy_route(self, cards: List[Card], route: Route):
    """Buy a train route using the cards"""
    cost, colour = route.cost(), route.colour()
    cost_match = len(cards) == cost
    colour_match = False
    if colour == Colour.ANY:
      colour_match = all(card.colour() == cards[0].colour() for card in cards)
    else :
      colour_match = all(card.colour() == colour or card.colour() == Colour.ANY 
                         for card in cards)
    route_match = self.routes.count(route)
    if(cost_match and colour_match and route_match):
      for card in cards:
        card.set_status(Status.DISCARD)
        self.cards.append(card)
      self.routes.remove(route)
      return route
    raise Exception("Invalid cards")

  def __cards_by_status__(self, Status):
    """Return a new list of cards filter by status"""
    return [x for x in self.cards if x.status() == Status]

  def get_open_cards(self):
    """Return a list of open cards"""
    return self.__cards_by_status__(Status.OPEN)

  def get_close_cards(self):
    """Return a list of close cards"""
    return self.__cards_by_status__(Status.CLOSE)

  def get_discard_cards(self):
    """Return a list of discard cards"""
    return self.__cards_by_status__(Status.DISCARD)

  def score(self, routes: List[Route]):
    """Return the score of a player"""
    return self.score_path(routes), self.score_routes(routes)

  def score_routes(self, routes: List[Route]):    
    """Return the score of a player by summing all the routes"""
    score = 0
    for route in routes:
      score += self.points(route.cost())
    return score

  def points(self, distance: int):
    """Return the score of a route"""
    x = [0, 1, 2, 4, 7, 10, 15]
    return x[distance]

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
