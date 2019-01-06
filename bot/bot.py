from ranker import ranker


class Bot:

    def make_move(self, game):
        """
        Implement this method to make the bot smarter.
        Currently will check the strength of the hand and will Check, Call, or Raise.

        Not every move will be perfectly legal in all cases, but the engine will
        transform the move to the logical alternative and output a warning if illegal.
        """
        hand = game.me.hand
        table = game.table.cards

        strength = self.get_hand_strength(hand, table)

        # Check if we're on the river with only a high card
        if strength[0] < ranker.PAIR and game.bet_round == 'river':
            return 'check'

        # Call if we have a hand weaker than straight
        if strength[0] < ranker.STRAIGHT:
            return 'call'

        # Raise by minimum amount if straight or higher
        return 'raise_' + str(game.table.big_blind * 2)

    @staticmethod
    def get_hand_strength(hand, table):
        if len(table) == 0:
            return ranker.rank_two_cards(hand)

        if len(table) == 3:
            return ranker.rank_five_cards(hand + table)

        return ranker.rank_more_than_five_cards(hand + table)