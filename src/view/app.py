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
	
	def construct(self, master, *, width=2, height=1):
		color: str
		text: str
		if self.suit is None or self.value is None:
			color = "blue"
			text = '?'
		else:
			color = ["red", "black"][self.suit in 'cs']
			text = f"{self.value}{self.suits_prety[self.suit]}"

		temp = tk.Button(master ,width=width, height=height, 
					font="Helvica 12", fg=color,
					text=text
				)
		
		return temp

class Hand:
	def __init__(self) -> None:
		self.cards = [Card(), Card()]
	
	def construct(self, master):
		base = tk.Frame(master, bg="#0f0f0f")

		card_base = tk.Frame(base, bg="#0f0f0f")

		for i in self.cards:
			i.construct(card_base, width=4, height=2).pack(side=tk.LEFT, padx=5)

		card_base.place(relx=.5, rely=.5, anchor=tk.CENTER)

		return base

class GameArea:
	def __init__(self) -> None:
		self.dealer_frame = Hand()
		self.player_frame = Hand()
	
	def construct(self, master):
		base = tk.Frame(master)

		self.dealer_frame.construct(base)\
			.place(relwidth=1, relheight=.5)
		
		self.player_frame.construct(base)\
			.place(relwidth=1, relheight=.5, rely=.5)

		return base

class SideMenu:
	def __init__(self, deck:List[List[Card]], *, bg="#1f1f1f") -> None:
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
				j.construct(base).grid(row=row, column=col)
				col += 1
			row += 1
		
		return base

class App:
	def __init__(self) -> None:
		self.deck = self._create_deck()
		
		self.side_menu = SideMenu(self.deck)
		self.game_area = GameArea()

	def construct(self):
		root = tk.Tk()
		root.geometry("800x500")

		self.side_menu.construct(root, width=200)\
			.pack(side=tk.RIGHT, anchor=tk.E, fill=tk.Y, expand=False)
		
		self.game_area.construct(root)\
			.pack(side=tk.LEFT, anchor=tk.W, fill=tk.BOTH, expand=True)

		return root

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