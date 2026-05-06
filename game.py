# game.py
"""Core game logic for the reaction game.

The :class:`Game` class manages the state of the game: the list of
currently visible tiles, the score, and whether the game is over.  It
provides methods that are used by the GUI layer to spawn tiles, handle
clicks, and reset the game.
"""

import random
from dataclasses import dataclass
from typing import Dict, Tuple

# Constants for the canvas size – used by both the GUI and the logic
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
TILE_SIZE = 40


@dataclass
class Tile:
    """Represents a single tile on the board.

    Attributes
    ----------
    id: int
        Unique identifier used by the GUI to bind click events.
    x: int
        X coordinate of the top‑left corner.
    y: int
        Y coordinate of the top‑left corner.
    """
    id: int
    x: int
    y: int


class Game:
    """Game logic for the reaction game.

    The GUI layer interacts with this class via the public API.
    """

    def __init__(self) -> None:
        self.tiles: Dict[int, Tile] = {}
        self.score: int = 0
        self.game_over: bool = False
        self._next_tile_id: int = 1

    def reset(self) -> None:
        """Reset the game to its initial state."""
        self.tiles.clear()
        self.score = 0
        self.game_over = False
        self._next_tile_id = 1

    def spawn_tile(self) -> Tile:
        """Create a new tile at a random position.

        Returns
        -------
        Tile
            The newly created tile.
        """
        if self.game_over:
            raise RuntimeError("Cannot spawn tiles after game over")

        # Ensure the tile fits inside the canvas
        max_x = CANVAS_WIDTH - TILE_SIZE
        max_y = CANVAS_HEIGHT - TILE_SIZE
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        tile = Tile(id=self._next_tile_id, x=x, y=y)
        self.tiles[tile.id] = tile
        self._next_tile_id += 1

        # Check for game over condition
        if len(self.tiles) >= 10:
            self.game_over = True

        return tile

    def click_tile(self, tile_id: int) -> bool:
        """Handle a click on a tile.

        Parameters
        ----------
        tile_id: int
            Identifier of the tile that was clicked.

        Returns
        -------
        bool
            ``True`` if a tile was removed and the score increased,
            ``False`` if the tile was not found.
        """
        if tile_id in self.tiles:
            del self.tiles[tile_id]
            self.score += 1
            return True
        return False

    def get_score(self) -> int:
        return self.score

    def is_game_over(self) -> bool:
        return self.game_over

    def visible_tile_count(self) -> int:
        return len(self.tiles)


# The module can be imported by the GUI and by the tests.

if __name__ == "__main__":
    # Simple manual test
    g = Game()
    for _ in range(12):
        try:
            g.spawn_tile()
        except RuntimeError:
            print("Game over reached")
            break
    print("Score:", g.get_score(), "Tiles:", g.visible_tile_count(), "Game over:", g.is_game_over())
