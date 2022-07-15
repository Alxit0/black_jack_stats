from logging import root
import tkinter as tk

class App:
	def __init__(self, *, side_menu_width=200) -> None:
		root = tk.Tk()
		root.geometry("700x500")

		side_menu = tk.Frame(root, width=side_menu_width, bg="#1f1f1f")
		side_menu.pack(side=tk.RIGHT, expand=False, fill=tk.Y, anchor=tk.CENTER)

		game_frame = tk.Frame(root)
		game_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

		dealer_frame = tk.Frame(game_frame, bg="#0f0f0f")
		dealer_frame.place(relwidth=1, relheight=.5)

		player_frame = tk.Frame(game_frame, bg="#0f0f0f")
		player_frame.place(relwidth=1, relheight=.5, rely=.5)

		self.root = root
	
	def run(self):
		self.root.mainloop()