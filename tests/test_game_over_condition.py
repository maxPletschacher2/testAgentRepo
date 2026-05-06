import unittest
from unittest.mock import Mock
from game import Game

class TestGameOver(unittest.TestCase):
    def test_game_over_at_10_tiles(self):
        game = Game()
        # Simulate 10 unclicked tiles
        game.tile_count = 10
        self.assertTrue(game.is_game_over())

    def test_click_prevents_game_over(self):
        game = Game()
        game.tile_count = 9
        game.click_tile()
        self.assertFalse(game.is_game_over())

if __name__ == '__main__':
    unittest.main()