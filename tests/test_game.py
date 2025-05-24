import unittest
from klondike import Game, Card, RANKS, SUITS, Pile


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

    def test_scoring_and_win(self):
        game = Game()
        game.stock = Pile()
        game.waste = Pile()
        game.tableau = [[] for _ in range(7)]
        game.foundations = {suit: Pile() for suit in SUITS}

        game.waste.push(Card('5', 'C', True))
        game.tableau[0].append(Card('6', 'D', True))
        game.move('W', 'T1')
        self.assertEqual(game.score, 5)

        game.tableau[1] = [Card('10', 'S', False), Card('9', 'H', True)]
        game.tableau[2] = [Card('10', 'C', True)]
        game.move('T2', 'T3')
        self.assertEqual(game.score, 15)

        game.tableau[3] = [Card('A', 'H', True)]
        game.move('T4', 'FH')
        self.assertEqual(game.score, 25)

        game.draw()  # recycle waste
        self.assertEqual(game.score, 10)

        for suit in SUITS:
            game.foundations[suit].cards = [Card(rank, suit, True) for rank in RANKS]

        self.assertTrue(game.is_won())

    def test_move_same_pile(self):
        game = Game()
        initial_score = game.score
        initial_pile = list(game.tableau[0])

        result = game.move('T1', 'T1')

        self.assertFalse(result)
        self.assertEqual(game.tableau[0], initial_pile)
        self.assertEqual(game.score, initial_score)


if __name__ == '__main__':
    unittest.main()
