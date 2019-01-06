from itertools import combinations

ROYAL_FLUSH = '9'
STRAIGHT_FLUSH = '8'
FOUR_OF_A_KIND = '7'
FULL_HOUSE = '6'
FLUSH = '5'
STRAIGHT = '4'
THREE_OF_A_KIND = '3'
TWO_PAIR = '2'
PAIR = '1'
HIGH_CARD = '0'


def rank_two_cards(cards):
    # Pair in hand
    if cards[0].value == cards[1].value:
        return ['1', str(cards[0].number)]
    # No pair
    values = sorted([card.number for card in cards], reverse=True)
    return ['0', [str(value) for value in values]]


def rank_five_cards(cards):
    """Returns an (array) value that represents a strength for a hand.
       These can easily be compared against each other."""

    # List of all card values
    values = sorted([card.number for card in cards])

    # Checks if hand is a straight
    is_straight = all([values[i] == values[0] + i for i in range(5)])

    # Additional straight check
    if not is_straight:

        # Weakest straight
        is_straight = all(values[i] == values[0] + i for i in range(4)) and values[4] == 12

        # Rotate values as the ace is weakest in this case
        values = values[1:] + values[:1]

    # Checks if hand is a flush
    is_flush = all([card.suit == cards[0].suit for card in cards])

    # Get card value counts
    value_count = {value: values.count(value) for value in values}

    # Sort value counts by most occuring
    sorted_value_count = sorted([(count, value) for value, count in value_count.items()],
                                reverse=True)

    # Get all kinds (e.g. four of a kind, three of a kind, pair)
    kinds = [value_count[0] for value_count in sorted_value_count]

    # Get values for kinds
    kind_values = [value_count[1] for value_count in sorted_value_count]

    # Royal flush
    if is_straight and is_flush and values[0] == 8:
        return [ROYAL_FLUSH] + [str(value) for value in values]
    # Straight flush
    if is_straight and is_flush:
        return [STRAIGHT_FLUSH] + kind_values
    # Four of a kind
    if kinds[0] == 4:
        return [FOUR_OF_A_KIND] + kind_values
    # Full house
    if kinds[0] == 3 and kinds[1] == 2:
        return [FULL_HOUSE] + kind_values
    # Flush
    if is_flush:
        return [FLUSH] + kind_values
    # Straight
    if is_straight:
        return [STRAIGHT] + kind_values
    # Three of a kind
    if kinds[0] == 3:
        return [THREE_OF_A_KIND] + kind_values
    # Two pair
    if kinds[0] == 2 and kinds[1] == 2:
        return [TWO_PAIR] + kind_values
    # Pair
    if kinds[0] == 2:
        return [PAIR] + kind_values
    # No pair
    return [HIGH_CARD] + kind_values


def rank_more_than_five_cards(cards):
    """(Not the most efficient way to do this)"""
    combinations_of_five = list(combinations(cards, 5))
    return max([rank_five_cards(cards) for cards in combinations_of_five])
