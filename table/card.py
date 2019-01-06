class Card:

    def __init__(self, string_value):
        self.value = string_value[0]
        self.suit = string_value[1]
        self.number = '23456789TJQKA'.find(self.value)
