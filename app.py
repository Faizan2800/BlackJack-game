import random
import tkinter as tk
from tkinter import messagebox, font as tkFont

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {
    'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
    'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
    'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11
}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.all_cards = [Card(suit, rank) for suit in suits for rank in ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        return ', '.join([str(card) for card in self.cards]) + f" (Value: {self.value})"

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.chips = 100

    def bet(self, amount):
        if amount > self.chips:
            raise ValueError("Insufficient chips!")
        self.chips -= amount
        return amount

    def win(self, amount):
        self.chips += amount * 2

# --- Stylish GUI Game with Instructions ---

class BlackjackGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("🃏 Vegas Blackjack Table")
        self.master.configure(bg='#0b6623')  # Green felt look

        self.deck = Deck()
        self.deck.shuffle()

        self.player = Player("You")
        self.dealer = Player("Dealer")

        self.chip_font = tkFont.Font(family='Courier', size=14, weight='bold')
        self.card_font = tkFont.Font(family='Georgia', size=12, weight='bold')

        self.setup_gui()

    def setup_gui(self):
        # Chips Display
        self.chips_label = tk.Label(self.master, text=f"💰 Chips: {self.player.chips}", font=self.chip_font, fg='gold', bg='#0b6623')
        self.chips_label.pack(pady=5)

        self.dealer_frame = tk.LabelFrame(self.master, text="🎩 Dealer's Hand", font=self.card_font, bg='#0b6623', fg='white')
        self.dealer_frame.pack(padx=10, pady=10, fill="x")
        self.dealer_hand_label = tk.Label(self.dealer_frame, text="", font=self.card_font, bg='#0b6623', fg='white')
        self.dealer_hand_label.pack()

        self.player_frame = tk.LabelFrame(self.master, text="🧑‍💼 Your Hand", font=self.card_font, bg='#0b6623', fg='white')
        self.player_frame.pack(padx=10, pady=10, fill="x")
        self.player_hand_label = tk.Label(self.player_frame, text="", font=self.card_font, bg='#0b6623', fg='white')
        self.player_hand_label.pack()

        self.bet_frame = tk.Frame(self.master, bg='#0b6623')
        self.bet_frame.pack()
        tk.Label(self.bet_frame, text="Bet Amount:", font=self.card_font, fg='white', bg='#0b6623').pack(side='left')
        self.bet_entry = tk.Entry(self.bet_frame, width=5, font=self.card_font)
        self.bet_entry.insert(0, '10')
        self.bet_entry.pack(side='left', padx=5)

        self.place_bet_button = tk.Button(self.master, text="Place Bet", font=self.card_font, bg='gold', command=self.reset_game)
        self.place_bet_button.pack(pady=5)

        self.hit_button = tk.Button(self.master, text="🎯 Hit", font=self.card_font, command=self.hit, state='disabled', bg='white')
        self.hit_button.pack(pady=3)

        self.stand_button = tk.Button(self.master, text="🛑 Stand", font=self.card_font, command=self.stand, state='disabled', bg='white')
        self.stand_button.pack(pady=3)

        self.help_button = tk.Button(self.master, text="📘 How to Play", font=self.card_font, bg='#87CEFA', command=self.show_instructions)
        self.help_button.pack(pady=10)

    def show_instructions(self):
        instructions = (
            "🎰 Welcome to Blackjack! Here's how to play:\n\n"
            "1. 🪙 Place your bet (default is 10 chips).\n"
            "2. 🧑‍💼 You and the dealer are dealt cards.\n"
            "3. 🎯 Press 'Hit' to draw a card.\n"
            "4. 🛑 Press 'Stand' to end your turn.\n"
            "5. 🃏 The dealer will draw until they reach 17 or higher.\n"
            "6. 🏆 Closest to 21 without going over wins!\n"
            "7. 💀 Over 21? That’s a bust – you lose the round.\n"
            "8. ⚖️ Ties return your bet. Winning doubles your bet!\n\n"
            "💡 Tip: Aces count as 11 or 1 – whichever helps most.\n"
            "\nHave fun & good luck!"
        )
        messagebox.showinfo("📘 How to Play Blackjack", instructions)

    def hit(self):
        card = self.deck.deal_one()
        self.player.hand.add_card(card)
        self.update_gui()

        if self.player.hand.value > 21:
            messagebox.showinfo("Bust!", "You busted! Dealer wins.")
            self.check_game_over()
            self.disable_buttons()

    def stand(self):
        while self.dealer.hand.value < 17:
            self.dealer.hand.add_card(self.deck.deal_one())

        self.update_gui()

        if self.dealer.hand.value > 21 or self.player.hand.value > self.dealer.hand.value:
            messagebox.showinfo("🏆 Result", "You win!")
            self.player.win(self.current_bet)
        elif self.player.hand.value < self.dealer.hand.value:
            messagebox.showinfo("💀 Result", "Dealer wins.")
        else:
            messagebox.showinfo("⚖️ Result", "It's a tie!")
            self.player.chips += self.current_bet  # return bet

        self.check_game_over()
        self.disable_buttons()
        self.update_chip_display()

    def reset_game(self):
        try:
            self.current_bet = int(self.bet_entry.get())
            if self.current_bet <= 0:
                raise ValueError
            self.player.bet(self.current_bet)
        except:
            messagebox.showerror("Invalid Bet", "Enter a valid positive number.")
            return

        self.deck = Deck()
        self.deck.shuffle()
        self.player.hand = Hand()
        self.dealer.hand = Hand()

        self.player.hand.add_card(self.deck.deal_one())
        self.player.hand.add_card(self.deck.deal_one())
        self.dealer.hand.add_card(self.deck.deal_one())

        self.update_gui()
        self.update_chip_display()
        self.enable_buttons()

    def update_gui(self):
        self.player_hand_label.config(text=str(self.player.hand))
        self.dealer_hand_label.config(text=str(self.dealer.hand))

    def update_chip_display(self):
        self.chips_label.config(text=f"💰 Chips: {self.player.chips}")

    def disable_buttons(self):
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")

    def enable_buttons(self):
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")

    def check_game_over(self): 
        if self.player.chips <= 0:
            response = messagebox.askyesno("💸 Out of Chips!", "You're out of chips! Do you want to start a new game with 100 chips?")
            if response:
                self.player.chips = 100
                self.update_chip_display()
            else:
                self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    game = BlackjackGUI(root)
    root.mainloop()
