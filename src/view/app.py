import tkinter as tk

class Card:
	suits = {
		'h': '♥',
		'd': '♦',
		'c': '♣',
		's': '♠',
	}

	def __init__(self, value, suit) -> None:
		self.value = value
		self.suit = suit
		self.widget: tk.Button
	
	def construct(self, master):
		obj = tk.Button(master, width=2, height=1,
			text=f"{self.value}{self.suits[self.suit]}", font='Helvetica 12',
			command=self._destroy)
		
		self.widget = obj
		return obj
	
	def _destroy(self):
		if self.widget is None:
			return
		
		self.widget.destroy()

class Deck:
	values = ['A'] + list(range(2, 11)) + [*'DJK']
	suits = 'hdcs'

	def __init__(self) -> None:
		pass
	
	def construct(self, master, *, bg="white") -> tk.Frame:
		base = tk.Frame(master, bg=bg)

		for i in range(13):
			for j in range(4):
				# create card and place it
				Card(self.values[i], self.suits[j]).construct(base).grid(column=j, row=i)
		
		return base



class App:
	def __init__(self, *, side_menu_width=200) -> None:
		root = tk.Tk()
		root.geometry("700x500")

		side_menu = tk.Frame(root, width=side_menu_width, bg="#1f1f1f")
		side_menu.pack(side=tk.RIGHT, expand=False, fill=tk.Y, anchor=tk.E)

		game_frame = tk.Frame(root)
		game_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT, anchor=tk.E)

		dealer_frame = tk.Frame(game_frame, bg="#0f0f0f")
		dealer_frame.place(relwidth=1, relheight=.5)

		player_frame = tk.Frame(game_frame, bg="#0f0f0f")
		player_frame.place(relwidth=1, relheight=.5, rely=.5)

		self.root = root
		self.side_menu = side_menu
		self.dealer_frame = dealer_frame
		self.player_frame = player_frame
	
	def run(self):
		self.root.mainloop()
	
	def add_cards(self):
		deck = Deck().construct(self.side_menu, bg=self.side_menu['bg'])
		deck.place(anchor=tk.CENTER, relx=.5, rely=.5)