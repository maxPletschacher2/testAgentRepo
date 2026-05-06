import unittest

# Importing the GUI should not raise errors
# We do not actually start the mainloop in this test.

class TestGUIStart(unittest.TestCase):
    def test_import(self):
        import gui
        import main
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
