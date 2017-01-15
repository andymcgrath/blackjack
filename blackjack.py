import random


class Participant(object):
    def __init__(self):
        self.hand = []

    def get_hand(self):
        return self.hand

    def add_to_hand(self, card):
        self.hand.append(card)


class Game(object):
    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer

    def play(self):
        print "Let's get ready to rumble"
        self.dealer.deal(self.player)
        while True:
            self.turn()
    # Need something to track player

    @staticmethod
    def busted():
        return False

    def turn(self):
        move = raw_input("Would you like a hit or stay? [H or S] ").upper()
        if move.isalpha() and move == 'H':
            self.dealer.hit(self.player)
            print self.player.get_hand()
        elif move.isalpha() and move == 'S':
            print "I see you are playing it safe"
            return False
        else:
            self.turn()


class Deck(object):
    deck = {}

    def __init__(self):
        self.cards = range(1, 3)
        self.face_cards = ['J', 'Q', 'K']
        self.suits = ['Heart', 'Diamond', 'Spade', 'Club']
        self.card_index = {'Heart': 6, 'Diamond': 6, 'Spade': 6, 'Club': 6}

    def build_deck(self):
        for suit in self.suits:
            self.deck[suit] = self.cards + self.face_cards
        return self.deck


class Player(Participant):
    def __init__(self, bankroll):
        super(Player, self).__init__()
        self.bankroll = bankroll

    def fold(self):
        self.hand = []

    def split(self):
        pass

    def double_down(self):
        pass

    def insurance(self):
        pass

    def get_bankroll(self):
        return self.bankroll


class Bankroll(object):
    def __init__(self, initial_buy_in=100):
        self.value = initial_buy_in
        self.bet = 0.0

    def get_bankroll(self):
        return self.value

    def cash_out(self):
        return self.value

    def make_bet(self, amount):
        self.value -= amount
        self.bet += amount
        return self.bet


class Dealer(Participant):
    def __init__(self):
        super(Dealer, self).__init__()
        self.deck = Deck().build_deck()
        self.card_index = Deck().card_index
        self.dealt = set()

    def deal(self, player):

        for i in xrange(4):
            if i % 2 == 0:
                self.deal_card(player)
            else:
                self.deal_card(self)

        print 'Player:', player.get_hand()
        print 'Dealer:', self.get_hand()

    def deal_card(self, player):

        random_suit = self.get_random_suit()
        index = self.get_card_index(random_suit)-1
        card = self.get_card(index, random_suit)
        try:
            if card not in self.dealt:
                player.add_to_hand(card)
                self.dealt.add(card)
            else:
                print "I'm out of cards. Time to shuffle"
                self.dealt = set()
                player.add_to_hand(card)
        except ValueError:
            print "I'm out of cards. Time to shuffle"
            self.dealt = set()
            player.add_to_hand(card)

    def get_card(self, index, random_suit):

        cards = self.get_cards_for_suit(random_suit)

        random_card = self.get_random_card(cards, index)

        try:
            cards.remove(random_card)
        except ValueError:
            pass

        self.update_deck_tracking(cards, random_card, random_suit)

        # Construct card to be dealt suit + value
        card = random_suit + "-" + str(random_card)
        return card

    def update_deck_tracking(self, cards, random_card, random_suit):

        # Decrement card index to avoid index out of bounds
        if self.card_index[random_suit] >= 1:
            self.card_index[random_suit] -= 1
        else:
            pass

    def get_random_card(self, cards, index):
        # Randomly choose a card and remove it from the deck
        print "get_random_card - Index:", index
        try:
            random_card = cards[random.randint(0, index)]
            print "Random Card:", random_card
        except IndexError:
            random_card = 'OUT OF CARDS'
            print random_card
        return random_card

    def get_cards_for_suit(self, random_suit):
        # Select the list of cards associated to the randomly selected suit
        cards = self.deck[random_suit]
        print "Cards:", cards
        return cards

    def get_random_suit(self):
        # Randomly choose a suit
        suits = self.deck.keys()
        random_suit = suits[random.randint(0, 3)]
        print "Random Suit:", random_suit
        return random_suit

    def get_card_index(self, random_suit):
        # Setup an index to track remaining cards
        index = self.card_index[random_suit]-1
        print "Index", index
        return index

    def hit(self, player):
        self.deal_card(player)

    def sweep(self, player, bet):
        pass

    def payout(self, player, pot):
        pass


def start():
    # play = raw_input('Would you like to play [Y or N}? ').upper()
    play = 'Y'
    if play == 'Y':
        print "Let's play a game!"

        dealer = Dealer()
        player = Player(1000)
        game = Game(player, dealer)
        game.play()
    else:
        print "Maybe next time..."


start()
