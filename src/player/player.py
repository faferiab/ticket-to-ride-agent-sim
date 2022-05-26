
from typing import List

from src.model.card import Card


class Player():
  """Represent a game player"""
  def __init__(self, name: str, train_counter: int, initial: List[Card]):
    self.name = name
    self.train_counter = train_counter
    self.hand = initial

  def action(self, state):
    """Return one possible action for player"""
    raise NotImplementedError

  def result(self, state, action):
    """Return one possible action for player"""
    raise NotImplementedError

  def is_goal(self):
    return self.train_counter == 0
