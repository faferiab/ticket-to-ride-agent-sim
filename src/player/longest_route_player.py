from typing import Dict, List, Set

from src.game import Game
from src.model import Action, Card, Colour, Route

from .player import Player
import random

class LongestRoutePlayer(Player):

    def get_nearest_routes(self, game: Game):
        """Return a list of the routes that connect with the start or end in the 
        actual player route, if there are not available connected routes use the n-1 
        deep to look for routes"""
        result : Set[Route] = set()
        actual_routes = self.owned_routes if len(self.owned_routes) else [random.choice(game.routes)]
        for idx in range(min(len(actual_routes), 2)):
            start, end = actual_routes[idx], actual_routes[len(actual_routes)-1-idx]
            looking_route = [start.start(), start.end(), end.start(), end.end()]
            for route in game.get_routes():
                if(looking_route.count(route.start()) or looking_route.count(route.end())):
                    result.add(route)
            if len(result):
                return result
        return result

    def get_reward_route_list(self, routes: List[Route], cards_freq: Dict):
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
            result.append((route, percentage_route / (abs(cost-3.5)),
                           percentage_route >= 1))
        result.sort(key=lambda route: (
            route[REWARD_PROP], route[AVAILABLE]), reverse=True)
        return result

    def get_buyable_route(self, game: Game, cards_freq: Dict):
        """Return best buyable route based on players hand cards and route reward"""
        ROUTE = 0
        AVAILABLE = 2
        route_list = self.get_reward_route_list(
            self.get_nearest_routes(game), cards_freq)
        result = [x[ROUTE] for x in route_list if x[AVAILABLE]]
        route: Route = result.pop(0) if len(result) else None
        if route and route.cost() <= self.__train_counter__:
            return route
        return None

    def action_get_card(self, game: Game, cards_freq: Dict):
        """Return a pickable card based on metrics in cards players hand else return None"""
        ROUTE = 0
        AVAILABLE = 2
        reward_list = self.get_reward_route_list(
            self.get_nearest_routes(game), cards_freq, game)
        cards_list = [card.colour() for card in game.get_open_cards()]
        route: Route
        for route in [x[ROUTE] for x in reward_list if not x[AVAILABLE]]:
            if cards_list.count(route.colour()):
                return [card for card in game.get_open_cards() 
                if card.colour() == route.colour()].pop()
        return None

    def action_take_card(self, game: Game, cards_freq: Dict, hand: List[Card]):
        card = self.action_get_card(game, cards_freq)
        card = game.deal_close_card() if not card else game.deal_open_card(card)
        hand.append(card)
        super().add_card(card.colour())

    def action(self, game):
        """If the player can buy a route return BUY else the player take a card 
        and return TAKE"""
        route = self.get_buyable_route(game, self.cards_freq)
        if route:
            return (Action.BUY, route)
        return (Action.TAKE, None)

    def result(self, game: Game, action):
        action_type, action_data = action
        if action_type == Action.BUY:
            super().action_buy_route(game, action_data)
        elif action_type == Action.TAKE:
            for _ in range(2):
                self.action_take_card(game, self.cards_freq, self.hand)
