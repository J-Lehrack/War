# A single-card version of the game war

import game_cards
import game_questions


class WarCard(game_cards.Card):
    """A War Card"""
    ace_value = 1

    @property
    def value(self):
        if self.is_face_up:
            v = WarCard.RANKS.index(self.rank) + 1
        else:
            v = None
        return v


class WarDeck(game_cards.Deck):
    """A War deck"""

    def populate(self):
        for suit in WarCard.SUITS:
            for rank in WarCard.RANKS:
                self.cards.append(WarCard(rank, suit))

    def is_empty(self):
        check = self.cards
        return check


class WarHand(game_cards.Hand):
    """A hand in War (1 card only)"""

    def __init__(self, name, score=0):
        super(WarHand, self).__init__()
        self.name = name
        self.score = score

    def __str__(self):
        rep = self.name + ":\t" + super(WarHand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    @property
    def total(self):
        # add up card values, treat each Ace as 1, for now
        t = 0
        for card in self.cards:
            t += card.value

        # determine if hand contains an Ace
        contains_ace = False
        for card in self.cards:
            if card.value == WarCard.ace_value:
                contains_ace = True

        # if hand contains Ace, add 14 to make Ace High
        if contains_ace:
            t += 13

        return t


class WarPlayer(WarHand):
    """A War Player"""

    def is_drawing(self):
        response = game_questions.ask_yes_no("\n" + self.name + ", do you want to Draw? (Y/N: ")
        return response

    def lose(self):
        print(self.name, "loses.")

    def win(self):
        print(self.name, "wins")

    @staticmethod
    def war():
        print("Its a War!!")

    def score_up(self):
        self.score += 1

    def display_score(self):
        print(f"{self.name}'s current score: {self.score}")

    def final_score(self):
        print(f"{self.name}'s score: {self.score}")


class WarComputer(WarHand):
    """A War Player"""

    def lose(self):
        print(self.name, "loses.")

    def win(self):
        print(self.name, "wins")

    def score_up(self):
        self.score += 1

    def display_score(self):
        print(f"{self.name}'s current score: {self.score}")

    def final_score(self):
        print(f"{self.name}'s score: {self.score}")


class WarGame(object):
    """A game of War"""

    def __init__(self, names):
        self.players = []
        for name in names:
            player = WarPlayer(name)
            self.players.append(player)

        self.computer = WarPlayer("Computer")

        self.deck = WarDeck()
        self.deck.populate()
        self.deck.shuffle()

    def play(self):
        # deal a card to both players
        self.deck.deal(self.players + [self.computer], per_hand=1)
        for player in self.players:
            print(player)
        print(self.computer)
        not_empty = self.deck.is_empty()

        if len(not_empty) != 0:
            for player in self.players:
                if player.total > self.computer.total:
                    player.win()
                    player.score_up()
                    player.display_score()
                    self.computer.display_score()

                elif player.total < self.computer.total:
                    player.lose()
                    self.computer.score_up()
                    player.display_score()
                    self.computer.display_score()

                elif player.total == self.computer.total:
                    player.war()
                    WarGame.play(self)

                else:
                    print("I don't know what to do anymore?!?!")

                player.clear()
            self.computer.clear()

        elif len(not_empty) == 0:
            for player in self.players:
                player.final_score()
                self.computer.final_score()
            reshuffle = game_questions.ask_yes_no("\nDo you want to reshuffle? (y/n): ")
            if reshuffle == "y":
                self.deck.populate()
                self.deck.shuffle()
                WarGame.play(self)
            elif reshuffle == "n":
                print("Thank you for playing.")
            else:
                print("Please use y/n")

        else:
            print("Houston we have an issue.")


if __name__ == "__main__":
    print("\t\tWelcome to War!\n")

    names = []
    for i in range(1):
        name = input("Enter player name: ")
        names.append(name)
    print()

    game = WarGame(names)

    again = None
    while again != "n":
        game.play()
        again = game_questions.ask_yes_no("\nContinue? (y/n) ")
    else:
        print("Thank you for playing")
