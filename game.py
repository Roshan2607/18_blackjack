from cards import Deck, hand_value


class Blackjack:
    def __init__(self):
        self.chips = 100

    def show(self, player, dealer, hide=True):
        shown_dealer = ["??"] if hide else [f"{r}{s}" for r, s in dealer]
        print("Dealer:", " ".join(shown_dealer))
        print("Player:", " ".join(f"{r}{s}" for r, s in player),
              "=", hand_value(player))

    def round(self):

        if self.chips <= 0:
            print("No chips remaining.")
            return False

        while True:
            raw_wager = input(
                f"Enter wager (1-{self.chips}): "
            ).strip()

            try:
                wager = int(raw_wager)
            except ValueError:
                print("Invalid wager.")
                continue

            if wager <= 0 or wager > self.chips:
                print("Invalid wager.")
                continue

            break

        deck = Deck()

        try:
            player = [deck.draw(), deck.draw()]
            dealer = [deck.draw(), deck.draw()]
        except (IndexError, RuntimeError):
            print("Deck is depleted. Round cancelled.")
            return True

        self.show(player, dealer)

        pv = hand_value(player)
        dv = hand_value(dealer)

        if pv == 21:
            if dv == 21:
                print("Both have blackjack. Push.")
            else:
                print("Blackjack! Player wins.")
                self.chips += wager

            return True

        if dv == 21:
            print("Dealer has blackjack. Dealer wins.")
            self.chips -= wager
            return True

        while True:

            pv = hand_value(player)

            if pv > 21:
                print("Player busts. Dealer wins.")
                self.chips -= wager
                return True

            if pv == 21:
                print("Player has 21.")
                break

            key = input("[h]it [s]tand [q]uit: ").strip().lower()

            if key == "q":
                print("Quitting. Wager not settled.")
                return False

            elif key == "s":
                break

            elif key == "h":
                try:
                    card = deck.draw()
                except (IndexError, RuntimeError):
                    print("Deck is depleted. Round cancelled.")
                    return True

                player.append(card)
                print(f"Player drew {card}.")
                self.show(player, dealer)

            else:
                print("Invalid command. Use h, s, or q.")

        while hand_value(dealer) < 17:

            try:
                card = deck.draw()
            except (IndexError, RuntimeError):
                print("Deck is depleted. Round cancelled.")
                return True

            dealer.append(card)
            print(f"Dealer drew {card}.")

        self.show(player, dealer, hide=False)

        pv = hand_value(player)
        dv = hand_value(dealer)

        if dv > 21:
            print("Dealer busts. Player wins.")
            self.chips += wager

        elif pv > dv:
            print("Player wins.")
            self.chips += wager

        elif pv < dv:
            print("Dealer wins.")
            self.chips -= wager

        else:
            print("Push.")

        print(f"Chips: {self.chips}")

        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)
        while self.chips > 0:
            if not self.round():
                return
            if input("Play again? [y/n]: ").strip().lower() != "y":
                return
