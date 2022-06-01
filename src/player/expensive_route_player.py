from enum import Enum
from typing import Dict, List

from src.game import Game
from src.model import Action, Card, Colour, Route

from .player import Player


class ExpensiveRoutePlayer(Player):

    def get_buyable_route(self, game: Game, cards_freq: Dict):
        """Return best buyable route based on players hand cards and route reward"""
        ROUTE = 0
        AVAILABLE = 2
        route_list = self.get_reward_route_list(
            self.get_longest_available_routes(game, 3), cards_freq, game)
        result = route_list.pop(0) if len(route_list) > 0 else (None, 0, False)
        route: Route = result[ROUTE]
        available: bool = result[AVAILABLE]
        if available and route and route.cost() <= self.__train_counter__:
            return route
        return None

    def get_longest_available_routes(self, game: Game, top: int):
        """Return top available longest routes"""
        routes = game.get_routes()
        top = top if len(routes) > top else len(routes)
        routes.sort(key=lambda route: route.cost(), reverse=True)
        return [routes[x] for x in range(top)]

    def get_reward_route_list(self, routes: List[Route], cards_freq: Dict, game: Game):
        """Return metric reward for a given route list and hand card"""
        REWARD_PROP = 1
        AVAILABLE = 2
        result = []
        count_wildcard = (0 if cards_freq.get(Colour.ANY) == None
                          else cards_freq.get(Colour.ANY))
        temp_cards_freq = cards_freq.copy()
        temp_cards_freq.update({Colour.ANY: -1})
        for route in routes:
            cost, colour_route = route.cost(), route.colour()
            available = 0
            if colour_route == Colour.ANY:
                available = max(temp_cards_freq.values())
            else:
                available = (0 if temp_cards_freq.get(colour_route) == None
                             else temp_cards_freq.get(colour_route))
            percentage_route = (available + count_wildcard) / cost
            result.append((route, percentage_route * game.points(cost),
                           percentage_route >= 1))
        result.sort(key=lambda route: (
            route[REWARD_PROP], route[AVAILABLE]), reverse=True)
        return result

    def action_get_card(self, game: Game, cards_freq: Dict):
        """Return a pickable card based on metrics in cards players hand else return None"""
        ROUTE = 0
        AVAILABLE = 2
        reward_list = self.get_reward_route_list(
            self.get_longest_available_routes(game, 5), cards_freq, game)
        cards_list = [card.colour() for card in game.get_open_cards()]
        route: Route
        for route in [x[ROUTE] for x in reward_list if not x[AVAILABLE]]:
            if cards_list.count(route.colour()):
                return [card for card in game.get_open_cards()].pop()
        return None

    def action(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError
