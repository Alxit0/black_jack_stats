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
		self.value = str(value)
		self.suit = suit

		self.text = self._string_format()
		self._widget = tk.Button
	
	def construct(self, master, command=None, *, width=2, height=1):
		color: str
		if self.suit is None or self.value is None:
			color = "blue" 
		else:
			color = ["red", "black"][self.suit in 'cs']
	
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
	
	def destroy(self):
		self._widget.destroy()

	def _string_format(self):
		if self.value is None or self.suit is None:
			return '?'
		
		return f"{self.value}{self.suits_prety[self.suit]}"

class Stats:
	def __init__(self, hand) -> None:
		self.hand: Hand = None
		
		self.score: tk.IntVar
		self.hit_sucess: tk.DoubleVar
	
	def construct(self, master):
		base = tk.Frame(master, bg="#2f2f2f", width=200)
		base.pack_propagate(False)

		self.score = tk.IntVar(base, value=0)
		# tk.Label(base, textvariable=self.score,
		# bg=base['bg'], fg='white'
		# ).pack(pady=10)

		self._construct_stat(base, "Score: ", self.score
		).pack(pady=10, fill=tk.X, padx=20)

		return base
	
	def increase(self, value:str):
		cur_value = self.score.get()

		if value == 'A':
			value = [1, 11][cur_value < 11]
		elif value.isalpha():
			value = 10
		else:
			value = int(value)

		self.score.set(cur_value + value)

	@staticmethod
	def _construct_stat(master, name:str, variable:tk.Variable):
		base = tk.Frame(master, bg=master['bg'])

		tk.Label(base, text=name,
			bg=master['bg'], fg='white'
		).pack(side=tk.LEFT)

		tk.Label(base, textvariable=variable,
			bg=master['bg'], fg='white'
		).pack(side=tk.LEFT)

		return base

class Hand:
	def __init__(self) -> None:
		self.cards = []
		self.stats_base = Stats(self)
		self.card_base: tk.Frame = None

		self._widget: tk.Frame
		self._widget_cards: tk.Frame
	
	def construct(self, master, main_app):
		base = tk.Frame(master, bg="#0f0f0f")
		
		# butao para selecionar a hand ativa
		tk.Button(base, width=2,
			command=lambda: main_app.set_active_hand(self)
		).pack(side=tk.LEFT, padx=5, anchor=tk.CENTER)
			# .place(x=10, rely=.5, anchor=tk.W)
		
		# onde vao ficar as cartas
		temp = tk.Frame(base, bg=base['bg'])
		self.card_base = tk.Frame(temp, bg=base['bg'])
		self.card_base.place(relx=.5, rely=.5, anchor=tk.CENTER)
		temp.pack(side=tk.LEFT, pady=5, fill=tk.BOTH, expand=True)

		# onde se vai mostrar os stats
		self.stats_base.construct(base)\
			.pack(side=tk.RIGHT, anchor=tk.E, fill=tk.Y, padx=10, pady=5)

		self._widget = base
		self._widget_cards = temp
		return base
	
	def add_card(self, card:Card):
		# print(self.cards)
		self.cards.append(card)

		if self.card_base is None:
			return
		
		self.stats_base.increase(card.value)

		card.construct_display(self.card_base)\
			.pack(side=tk.LEFT, padx=2)

	def change_bg(self, new_bg):
		self._widget['bg'] = new_bg
		self.card_base['bg'] = new_bg
		self._widget_cards['bg'] = new_bg



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
	
	def set_active_hand(self, hand:Hand):
		if self.active_hand is not None:
			self.active_hand.change_bg("#0f0f0f")
		
		if self.active_hand is hand:
			self.active_hand = None
			return
		
		self.active_hand = hand
		self.active_hand.change_bg("#1f1f1f")

	def add_card(self, card:Card):
		if self.active_hand is None:
			return
		
		if self.active_hand.stats_base.score.get() >= 21:
			return

		self.active_hand.add_card(card)
		card.destroy()
		
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
