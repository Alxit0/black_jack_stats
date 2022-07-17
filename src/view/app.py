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
	
	def __str__(self) -> str:
		return f"{self.value}{self.suits[self.suit]}"

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
		values = ['A'] + list(range(2, 11)) + [*'DVK']
		for i in range(len(values)):
			for j in range(4):
				temp: tk.Button
				temp = tk.Button(self.side_menu,
					text=str(Card(values[i],'hdcs'[j])),
					width=2, height=1, font='Helvetica 12')
				temp['command'] = temp.destroy
				temp.grid(column=j, row=i)