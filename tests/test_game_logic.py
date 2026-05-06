import unittest

from game import Game


class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_initial_state(self):
        self.assertEqual(self.game.get_score(), 0)
        self.assertFalse(self.game.is_game_over())
        self.assertEqual(self.game.visible_tile_count(), 0)

    def test_spawn_and_click(self):
        tile = self.game.spawn_tile()
        self.assertEqual(self.game.visible_tile_count(), 1)
        # Click the tile
        removed = self.game.click_tile(tile.id)
        self.assertTrue(removed)
        self.assertEqual(self.game.visible_tile_count(), 0)
        self.assertEqual(self.game.get_score(), 1)

    def test_game_over_condition(self):
        # Spawn 9 tiles – should not be game over
        for _ in range(9):
            self.game.spawn_tile()
        self.assertFalse(self.game.is_game_over())
        # 10th tile triggers game over
        self.game.spawn_tile()
        self.assertTrue(self.game.is_game_over())
        # After game over, spawning raises RuntimeError
        with self.assertRaises(RuntimeError):
            self.game.spawn_tile()

    def test_reset(self):
        self.game.spawn_tile()
        self.game.click_tile(1)
        self.game.reset()
        self.assertEqual(self.game.get_score(), 0)
        self.assertFalse(self.game.is_game_over())
        self.assertEqual(self.game.visible_tile_count(), 0)


if __name__ == "__main__":
    unittest.main()
