# -*- coding: utf-8 -*-
import logging
from random import randint

from .errors.noactivegameexception import NoActiveGameException


class GameStore(object):
    _instance = None
    _initialized = False

    def __new__(cls):
        if GameStore._instance is None:
            GameStore._instance = super(GameStore, cls).__new__(cls)
        return GameStore._instance

    def __init__(self):
        if not self._initialized:
            self._chat_dict = {}
            self._game_dict = {}
            self.logger = logging.getLogger(__name__)
            self._initialized = True

    @staticmethod
    def _generate_id():
        return randint(1000000, 9999999)

    def add_game(self, chat_id, game):
        if self.has_game(chat_id):
            raise Exception

        game.id = self._generate_id()
        while self._game_dict.get(game.id, None):
            game.id = self._generate_id()

        self.logger.info("Adding game with id {}".format(game.id))
        game.register_on_stop_handler(self._game_stopped_callback)
        self._chat_dict[chat_id] = game
        self._game_dict[game.id] = chat_id

    def get_game(self, chat_id):
        """

        :param chat_id:
        :return:
        """
        game = self._chat_dict.get(chat_id)
        if game is None:
            raise NoActiveGameException
        return game

    def has_game(self, chat_id):
        return chat_id in self._chat_dict

    def remove_game(self, chat_id):
        """
        Removes the game of a specific chat from the store
        :param chat_id:
        :return:
        """
        if chat_id == -1:
            return

        game = self._chat_dict.pop(chat_id)
        self._game_dict.pop(game.id)
        self.logger.debug("Removing game for {} ({})".format(chat_id, game.id))

    def _game_stopped_callback(self, game):
        """
        Callback to remove game from the GameStore
        :param game:
        :return:
        """
        # TODO Game statistics
        # for player in game.players:
        #     player set game won
        self.remove_game(self._game_dict[game.id])

        self.logger.debug("Current games: {}".format(len(self._chat_dict)))