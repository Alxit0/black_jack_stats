import tkinter as tk
from typing import List

class Card:
	suits_prety = {
		'h': '♥',
		't': '♦',
		'c': '♣',
		's': '♠'
	}

	def __init__(self, value=None, suit=None) -> None:
		self.value = value
		self.suit = suit

		self.text = '?'
		self._widget = tk.Button
	
	def construct(self, master, command=None, *, width=2, height=1):
		color: str
		if self.suit is None or self.value is None:
			color = "blue"
		else:
			color = ["red", "black"][self.suit in 'cs']
			self.update_text()
	
		temp = tk.Button(master ,width=width, height=height, 
					font="Helvica 12", fg=color,
					text=self.text,
					command=lambda: command(self),
				)
		self._widget = temp
		return temp
	
	def construct_display(self, master):
		return tk.Label(master, text=self.text,
			fg=["red", "black"][self.suit in 'cs'],
			width=2, height=2, font="Helvica 12"
		)
	
	def update_text(self):
		self.text = f"{self.value}{self.suits_prety[self.suit]}"

	def destroy(self):
		self._widget.destroy()

class Hand:
	def __init__(self) -> None:
		self.cards = []
		self.card_base: tk.Frame = None
	
	def construct(self, master, main_app):
		base = tk.Frame(master, bg="#0f0f0f")

		self.card_base = tk.Frame(base, bg="#0f0f0f")

		# butao para selecionar a hand ativa
		tk.Button(base, width=2,
			command=lambda: main_app.set_active_hand(self)
		).place(x=10, rely=.5, anchor=tk.W)

		self.card_base.place(relx=.5, rely=.5, anchor=tk.CENTER)

		return base
	
	def add_card(self, card:Card):
		print(self.cards)
		self.cards.append(card)

		if self.card_base is None:
			return
		
		card.construct_display(self.card_base)\
			.pack(side=tk.LEFT, padx=2)

class GameArea:
	def __init__(self, main_app) -> None:
		self.main_app = main_app
		
		self.dealer_frame = Hand()
		self.player_frame = Hand()
	
	def construct(self, master):
		base = tk.Frame(master)

		self.dealer_frame.construct(base, self.main_app)\
			.place(relwidth=1, relheight=.5)
		
		self.player_frame.construct(base, self.main_app)\
			.place(relwidth=1, relheight=.5, rely=.5)

		return base

class SideMenu:
	def __init__(self, main_app, deck:List[List[Card]], *, bg="#1f1f1f") -> None:
		self.main_app = main_app
		
		self.deck = deck
		self.bg = bg
		pass

	def construct(self, master, *, width=200) -> tk.Frame:
		base = tk.Frame(master, bg=self.bg, width=width)

		self._build_deck(base)\
			.place(relx=.5, y=10, anchor=tk.N)
		
		return base

	def _build_deck(self, master):
		base = tk.Frame(master, bg=self.bg)

		row = 0
		col = 0
		for i in self.deck:
			col = 0
			for j in i:
				j.construct(base, command=self.main_app.add_card)\
					.grid(row=row, column=col)
				col += 1
			row += 1
		
		return base

class App:
	def __init__(self) -> None:
		self.deck = self._create_deck()
		self.active_hand: Hand = None 
		
		self.side_menu = SideMenu(self, self.deck)
		self.game_area = GameArea(self)

	def construct(self):
		root = tk.Tk()
		root.geometry("800x500")

		self.side_menu.construct(root, width=200)\
			.pack(side=tk.RIGHT, anchor=tk.E, fill=tk.Y, expand=False)
		
		self.game_area.construct(root)\
			.pack(side=tk.LEFT, anchor=tk.W, fill=tk.BOTH, expand=True)

		return root
	
	def set_active_hand(self, hand):
		self.active_hand = hand
		print("[DEBUG] Active hand set")

	def add_card(self, card:Card):
		if self.active_hand is None:
			return
		
		card.destroy()
		self.active_hand.add_card(card)

	def run(self):
		root = self.construct()
		root.mainloop()
	
	def _create_deck(self):
		values = ['A'] + list(range(2, 11)) +  [*'DJK']
		suits = 'htcs'

		resp = []
		for i in range(13):
			temp = []
			for j in range(4):
				temp.append(Card(values[i], suits[j]))
			resp.append(temp)
		
		return resp

if __name__ == '__main__':
	app = App()
	app.run()

	# print(*map(chr, range(3, 7)))
