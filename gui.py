# gui.py
"""Tkinter GUI for the reaction game.

This module contains the :class:`GameGUI` class which creates a window
with a canvas for the tiles, a score label, a game‑over message and a
restart button.  It uses the :class:`Game` class from ``game.py`` for
the underlying logic.
"""

import tkinter as tk
from tkinter import messagebox

from game import Game, Tile, CANVAS_WIDTH, CANVAS_HEIGHT, TILE_SIZE


class GameGUI:
    """Tkinter GUI wrapper around the :class:`Game` logic."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Reaction Game")

        # Main frame
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        # Score label
        self.score_var = tk.StringVar(value="Score: 0")
        self.score_label = tk.Label(self.frame, textvariable=self.score_var, font=("Arial", 14))
        self.score_label.pack()

        # Canvas for tiles
        self.canvas = tk.Canvas(self.frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.canvas.pack(pady=5)

        # Restart button
        self.restart_button = tk.Button(self.frame, text="Restart", command=self.restart_game)
        self.restart_button.pack(pady=5)

        # Game logic instance
        self.game = Game()

        # Mapping from canvas item id to tile id
        self.canvas_item_to_tile_id: dict[int, int] = {}

        # Start the spawn loop
        self.spawn_interval_ms = 1000  # 1 second
        self.spawn_job = None
        self.start_spawning()

    def start_spawning(self) -> None:
        """Begin spawning tiles every second."""
        self.spawn_job = self.root.after(self.spawn_interval_ms, self.spawn_tile)

    def spawn_tile(self) -> None:
        """Spawn a new tile via the game logic and draw it on the canvas."""
        try:
            tile = self.game.spawn_tile()
        except RuntimeError:
            # Game over – stop spawning
            self.game_over()
            return

        # Draw rectangle on canvas
        rect = self.canvas.create_rectangle(
            tile.x,
            tile.y,
            tile.x + TILE_SIZE,
            tile.y + TILE_SIZE,
            fill="skyblue",
            outline="black",
        )
        # Store mapping for click handling
        self.canvas_item_to_tile_id[rect] = tile.id
        # Bind click event
        self.canvas.tag_bind(rect, "<Button-1>", self.on_tile_click)

        # Update score display
        self.update_score_label()

        # Schedule next spawn
        self.spawn_job = self.root.after(self.spawn_interval_ms, self.spawn_tile)

    def on_tile_click(self, event: tk.Event) -> None:
        """Handle a click on a tile rectangle."""
        # Find the canvas item that was clicked
        item = self.canvas.find_closest(event.x, event.y)[0]
        tile_id = self.canvas_item_to_tile_id.get(item)
        if tile_id is None:
            return

        # Remove tile via game logic
        removed = self.game.click_tile(tile_id)
        if removed:
            # Remove from canvas and mapping
            self.canvas.delete(item)
            del self.canvas_item_to_tile_id[item]
            self.update_score_label()

    def update_score_label(self) -> None:
        self.score_var.set(f"Score: {self.game.get_score()}")

    def game_over(self) -> None:
        """Handle game over: stop spawning and show a message."""
        if self.spawn_job is not None:
            self.root.after_cancel(self.spawn_job)
            self.spawn_job = None
        messagebox.showinfo("Game Over", f"Game Over! Final score: {self.game.get_score()}")

    def restart_game(self) -> None:
        """Reset the game state and clear the canvas."""
        # Cancel any pending spawn
        if self.spawn_job is not None:
            self.root.after_cancel(self.spawn_job)
            self.spawn_job = None

        # Clear canvas
        self.canvas.delete("all")
        self.canvas_item_to_tile_id.clear()

        # Reset game logic
        self.game.reset()
        self.update_score_label()

        # Restart spawning
        self.start_spawning()


# If this module is run directly, start the GUI.
if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
