# main.py
"""Entry point for the reaction game.

Running this script will launch the Tkinter GUI.
"""

import tkinter as tk
from gui import GameGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
