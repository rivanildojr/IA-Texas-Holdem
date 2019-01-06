from sys import stdin, stdout, stderr
import traceback
import time

from bot.player import Player
from table.card import Card
from table.table import Table


class Game:
    def __init__(self):
        self.time_per_move = -1
        self.timebank = -1
        self.initial_big_blind = -1
        self.initial_stack = -1
        self.hands_per_blind_level = -1

        self.last_update = 0

        self.round = 0
        self.bet_round = None
        self.player_names = []
        self.players = {}
        self.me = None
        self.opponent = None
        self.on_button_player = None
        self.table = Table()
        self.pot = -1
        self.amount_to_call = -1

    def update(self, data):
        # start timer
        self.last_update = time.time()
        for line in data.split('\n'):

            line = line.strip()
            if len(line) <= 0:
                continue

            tokens = line.split()
            if tokens[0] == "settings":
                self.parse_settings(tokens[1], tokens[2])
            elif tokens[0] == "update":
                if tokens[1] == "game":
                    self.parse_game_updates(tokens[2], tokens[3])
                else:
                    self.parse_player_updates(tokens[1], tokens[2], tokens[3])
            elif tokens[0] == "action":
                self.timebank = int(tokens[2])
                # Launching bot logic happens after setup finishes

    def parse_settings(self, key, value):
        if key == "timebank":
            self.timebank = int(value)
        elif key == "time_per_move":
            self.time_per_move = int(value)
        elif key == "player_names":
            self.player_names = value.split(',')
            self.players = {name: Player(name) for name in self.player_names}
        elif key == "your_bot":
            self.me = self.players[value]
            self.opponent = self.players[[name for name in self.player_names if name != value][0]]
        elif key == "initial_stack":
            self.initial_stack = int(value)
        elif key == "initial_big_blind":
            self.initial_big_blind = int(value)
        elif key == "hands_per_blind_level":
            self.hands_per_blind_level = int(value)

    def parse_game_updates(self, key, value):
        if key == "round":
            self.round = int(value)
            self.table.cards = []
        elif key == "bet_round":
            self.bet_round = value
        elif key == "small_blind":
            self.table.small_blind = int(value)
        elif key == "big_blind":
            self.table.big_blind = int(value)
        elif key == "on_button":
            self.on_button_player = self.players[value]
        elif key == "table":
            self.table.cards = self.parse_cards(value)

    def parse_player_updates(self, player_name, key, value):
        player = self.players[player_name]

        if key == "hand":
            player.hand = self.parse_cards(value)
        elif key == "bet":
            player.bet = int(value)
        elif key == "chips":
            player.chips = int(value)
        elif key == "pot":
            self.pot = int(value)
        elif key == "amount_to_call":
            self.amount_to_call = int(value)
        elif key == "move":
            player.move = value

    def time_remaining(self):
        return self.timebank - int(1000 * (time.clock() - self.last_update))

    @staticmethod
    def parse_cards(value):
        return [Card(string) for string in value.split(',')]

    @staticmethod
    def print_move(move):
        """issue an order, noting that (col, row) is the expected output
        however internally, (row, col) is used."""
        stdout.write('%s\n' % move)
        stdout.flush()

    def run(self, bot):
        """parse input, update game state and call the bot classes do_turn method"""
        not_finished = True
        data = ''

        while not stdin.closed and not_finished:
            try:
                current_line = stdin.readline().rstrip('\r\n')

                if len(current_line) <= 0:
                    time.sleep(1)
                    continue

                data += current_line + "\n"
                if current_line.lower().startswith("action"):
                    self.update(data)

                    move = bot.make_move(self)
                    self.print_move(move)

                    data = ''
                elif current_line.lower().startswith("quit"):
                    not_finished = False
            except EOFError:
                break
            except KeyboardInterrupt:
                raise
            except:
                # don't raise error or return so that bot attempts to stay alive
                traceback.print_exc(file=stderr)
                stderr.flush()
