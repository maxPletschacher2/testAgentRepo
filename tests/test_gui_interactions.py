import unittest
import tkinter as tk
from gui import GameGUI

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.gui = GameGUI(self.root)

    def test_score_update(self):
        self.gui.game.score = 5
        self.gui.update_score()
        self.assertEqual(self.gui.score_label.cget('text'), 'Score: 5')

    def test_tile_click_handling(self):
        # Simulate tile click event
        mock_tile = Mock()
        mock_tile.winfo_exists.return_value = 1
        self.gui.tiles.append(mock_tile)
        self.gui.on_tile_click(mock_tile)
        self.assertEqual(self.gui.game.score, 1)

if __name__ == '__main__':
    unittest.main()