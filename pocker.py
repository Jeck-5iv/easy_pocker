import abc
import copy
import random
from typing import final


@final
class Card(object):
    """Represents a standard playing card."""

    def __init__(self, suit, suit_index, rank, rank_index):
        self.suit = suit
        self.suit_index = suit_index
        self.rank = rank
        self.rank_index = rank_index

    def __repr__(self):
        return '{0} of {1}'.format(self.rank, self.suit)

    def __gt__(self, other):
        if self.rank_index > other.rank_index:
            return True
        return False

    def __lt__(self, other):
        if self.rank_index < other.rank_index:
            return True
        return False

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def is_suit_equal(self, other):
        return self.suit == other.suit

    def is_rank_equal(self, other):
        return self.rank_index == other.rank_index

    def is_next_in_rank(self, other):
        if self.rank is None or other.rank is None:
            return False
        if self.rank_index == other.rank_index + 1:
            return True
        if self.rank == 'Ace' and other.rank == '5':
            return True
        return False

    def __hash__(self):
        return hash(str(self))


@final
class Deck(object):
    """Represents a deck of cards."""

    SUIT_NAMES = ("Clubs", "Diamonds", "Hearts", "Spades")
    RANK_NAMES = (
        "No_rank", "No_rank", "2", "3", "4", "5", "6", "7", "8", "9", "10",
        "Jack", "Queen", "King", "Ace"
    )

    def __init__(self):
        self._cards = []
        for suit_index, suit in enumerate(self.SUIT_NAMES):
            for rand_index, rank in enumerate(self.RANK_NAMES[2:], start=2):
                card = Card(
                    suit=suit,
                    suit_index=suit_index,
                    rank=rank,
                    rank_index=rand_index,
                )
                self._cards.append(card)

    def __str__(self):
        res = []
        for card in self._cards:
            res.append(str(card))
        return '\n'.join(res)

    def pop_card(self, index=-1):
        """
        Remove and return a card from the deck.
        By default, pop the last card.
        """
        return self._cards.pop(index)

    def shuffle(self):
        """Shuffle the cards in this deck."""
        random.shuffle(self._cards)

    def move_cards(self, hand, num):
        """Move the given number of cards from the deck into the Hand."""
        for _ in range(num):
            hand.add_card(self.pop_card())


class AbstractCombination(abc.ABC):
    """Represents a combination in poker."""

    def __init__(self, cards):
        self._cards = cards

    @classmethod
    def from_cards(cls, cards):
        cards = cls._find_cards(cards)
        if cards is not None:
            return cls(cards)
        return None

    @classmethod
    def _find_cards(cls, cards):
        raise NotImplementedError('Method _find_cards not implemented')

    @classmethod
    def _order_a_cards_by_priority_of_their_combinations(cls, input_cards, *args):
        """args is tuple of sets/arrays of elements included in each combination in descending order of priority"""

        cards = copy.deepcopy(input_cards)
        cards.sort(key=lambda card: card.rank_index, reverse=True)
        ordered_cards = []
        cards_used_in_any_combination = set()
        for cards_used_in_current_combination in args:
            ordered_cards += [card for card in cards_used_in_current_combination]
            cards_used_in_any_combination = cards_used_in_any_combination.union(cards_used_in_current_combination)
        ordered_cards += [card for card in cards if card not in cards_used_in_any_combination]
        return ordered_cards

    @classmethod
    def _find_number_of_cards(cls, input_cards, number_of_cards):
        """returning best combination of number_of_card rank equal cards"""

        cards = copy.deepcopy(input_cards)
        combination = set()
        cards.sort(key=lambda card: card.rank_index, reverse=True)
        previous_cards = [Card(suit=None, suit_index=None, rank=None, rank_index=None) for i in
                          range(number_of_cards - 1)]
        for card in cards:
            if all(card.is_rank_equal(previous_card) for previous_card in previous_cards):
                combination.add(card)
                combination.update(previous_cards)
                break
            for i in range(-1, -len(previous_cards), -1):
                previous_cards[i] = previous_cards[i - 1]
            previous_cards[0] = card
        if len(combination) != 0:
            return combination
        else:
            return None

    def _get_kicker_weight(self):
        """Calculating weight of ordered set of cards excluding the combination multiplier"""

        weight = 0
        for i, card in enumerate(self._cards):
            # I multiply by 100 so that each rank_index takes exactly 2 digits; rank_index <= 14
            weight += card.rank_index * (100 ** (5 - 1 - i))
        return weight

    def __str__(self):
        return str(self._cards)

    @classmethod
    def type(cls):
        """returning type of combination"""
        return cls.__name__


@final
class HighCard(AbstractCombination):
    @classmethod
    def _find_cards(cls, cards):
        return cls._order_a_cards_by_priority_of_their_combinations(cards)

    def get_weight(self):
        # _get_kicker_weight() <= 10**10 < 10**12
        return self._get_kicker_weight() + (10 ** 12 * 0)


@final
class Pair(AbstractCombination):
    @classmethod
    def _find_cards(cls, input_cards):
        cards = copy.deepcopy(input_cards)
        pair = cls._find_number_of_cards(cards, 2)

        if pair is not None:
            return cls._order_a_cards_by_priority_of_their_combinations(cards, pair)
        return None

    def get_weight(self):
        return self._get_kicker_weight() + (10 ** 12 * 1)


@final
class TwoPairs(AbstractCombination):
    @classmethod
    def _find_cards(cls, input_cards):
        cards = copy.deepcopy(input_cards)
        pair1 = cls._find_number_of_cards(cards, 2)
        if pair1 is not None:
            for card in pair1:
                cards.remove(card)
            pair2 = cls._find_number_of_cards(cards, 2)
            if pair2 is not None:
                return cls._order_a_cards_by_priority_of_their_combinations(input_cards, pair1, pair2)
        return None

    def get_weight(self):
        return self._get_kicker_weight() + (10 ** 12 * 2)


@final
class Set(AbstractCombination):
    @classmethod
    def _find_cards(cls, input_cards):
        cards = copy.deepcopy(input_cards)
        set_ = cls._find_number_of_cards(cards, 3)

        if set_ is not None:
            return cls._order_a_cards_by_priority_of_their_combinations(cards, set_)
        return None

    def get_weight(self):
        return self._get_kicker_weight() + (10 ** 12 * 3)


class Straight(AbstractCombination):
    @classmethod
    def _find_cards(cls, input_cards):
        cards = copy.deepcopy(input_cards)
        cards.sort(key=lambda card: card.rank_index)

        straight = []
        for card in cards:
            if len(straight) == 5:
                break
            elif len(straight) == 0 or card.is_next_in_rank(straight[-1]):
                straight.append(card)
            else:
                straight = [card]

        if len(straight) == 5:
            if straight[-1].rank == "Ace" and straight[-2].rank == "5":
                straight[-1].rank_index = 1
                straight = [straight[-1]] + straight[:-1]
            straight.reverse()
            return cls._order_a_cards_by_priority_of_their_combinations(cards, straight)
        return None

    def get_weight(self):
        return self._get_kicker_weight() + (10 ** 12 * 4)


@final
class Flush(AbstractCombination):
    @classmethod
    def _find_cards(cls, input_cards):
        cards = copy.deepcopy(input_cards)

        if all(cards[0].suit == other_card.suit for other_card in cards):
            return cls._order_a_cards_by_priority_of_their_combinations(cards)
        return None

    def get_weight(self):
        return self._get_kicker_weight() + (10 ** 12 * 5)


@final
class FullHouse(AbstractCombination):
    @classmethod
    def _find_cards(cls, input_cards):
        cards = copy.deepcopy(input_cards)
        cards.sort(key=lambda card: card.rank_index, reverse=True)

        set_ = cls._find_number_of_cards(cards, 3)
        if set_ is not None:
            for card in set_:
                cards.remove(card)
            pair = cls._find_number_of_cards(cards, 2)
            if pair is not None:
                return cls._order_a_cards_by_priority_of_their_combinations(cards, set_, pair)
        return None

    def get_weight(self):
        return self._get_kicker_weight() + (10 ** 12 * 6)


@final
class Quads(AbstractCombination):
    @classmethod
    def _find_cards(cls, input_cards):
        cards = copy.deepcopy(input_cards)
        quads = cls._find_number_of_cards(cards, 4)

        if quads is not None:
            return cls._order_a_cards_by_priority_of_their_combinations(cards, quads)
        return None

    def get_weight(self):
        return self._get_kicker_weight() + (10 ** 12 * 7)


@final
class StraightFlush(AbstractCombination):
    @classmethod
    def _find_cards(cls, input_cards):
        cards = copy.deepcopy(input_cards)

        if (Straight.from_cards(cards) is not None) and (Flush.from_cards(cards) is not None):
            return cls._order_a_cards_by_priority_of_their_combinations(cards)
        return None

    def get_weight(self):
        return self._get_kicker_weight() + (10 ** 12 * 8)


@final
class RoyalFlush(AbstractCombination):
    @classmethod
    def _find_cards(cls, input_cards):
        cards = copy.deepcopy(input_cards)

        if StraightFlush.from_cards(cards) is None:
            return None
        cards.sort(key=lambda card: card.rank_index, reverse=True)
        if cards[1].rank != 'King':
            return None
        return cls._order_a_cards_by_priority_of_their_combinations(cards)

    def get_weight(self):
        return self._get_kicker_weight() + (10 ** 12 * 9)


@final
class Hand(object):
    """Represents a hand of playing cards."""

    COMBINATIONS = (
        RoyalFlush, StraightFlush, Quads, FullHouse, Flush, Straight, Set, TwoPairs, Pair, HighCard
    )

    def __init__(self):
        self._cards = []

    def add_card(self, card):
        """Add a card to the deck."""
        self._cards.append(card)

    def top_combination(self):
        for combination_type in self.COMBINATIONS:
            combination = combination_type.from_cards(self._cards)
            if combination is not None:
                return combination
        return None  # No combinations found

    def __str__(self):
        return str(self._cards)


def get_winner(player1, player2):
    """This function should print which player wins: first or second."""
    player1_top_combination = player1.top_combination()
    player2_top_combination = player2.top_combination()
    print("1st player's top combination: ", player1_top_combination.type(), str(player1_top_combination))
    print("2nd player's top combination: ", player2_top_combination.type(), str(player2_top_combination))
    print()
    if player1_top_combination.get_weight() > player2_top_combination.get_weight():
        return 'Player1 won!'
    elif player2_top_combination.get_weight() > player1_top_combination.get_weight():
        return 'Player2 won!'
    else:
        return 'Draw'


if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()

    player1 = Hand()
    player2 = Hand()

    deck.move_cards(player1, 5)
    deck.move_cards(player2, 5)

    print("1st player's hand: ", player1)
    print("2nd player's hand: ", player2)
    print()
    print(get_winner(player1, player2))
