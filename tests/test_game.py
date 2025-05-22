import unittest
from klondike import Game, Card


class GameTest(unittest.TestCase):
    def test_initial_setup(self):
        game = Game()
        total = len(game.stock.cards) + len(game.waste.cards)
        total += sum(len(p) for p in game.tableau)
        total += sum(len(f.cards) for f in game.foundations.values())
        self.assertEqual(total, 52)
        self.assertEqual(len(game.stock.cards), 24)
        self.assertTrue(all(p[-1].face_up for p in game.tableau))

    def test_move_rules(self):
        game = Game()
        card = Card('Q', 'H', True)
        dest = [Card('K', 'C', True)]
        self.assertTrue(game.can_move_to_tableau(card, dest))
        self.assertFalse(game.can_move_to_tableau(Card('J', 'H', True), dest))

    def test_draw(self):
        game = Game()
        initial_stock = len(game.stock.cards)
        game.draw()
        self.assertEqual(len(game.stock.cards), initial_stock - 1)
        self.assertEqual(len(game.waste.cards), 1)
        self.assertTrue(game.waste.cards[-1].face_up)


if __name__ == '__main__':
    unittest.main()
