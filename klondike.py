import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

SUITS = ['H', 'D', 'C', 'S']  # Hearts, Diamonds, Clubs, Spades
COLORS = {
    'H': 'red',
    'D': 'red',
    'C': 'black',
    'S': 'black',
}
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

@dataclass
class Card:
    rank: str
    suit: str
    face_up: bool = False

    def color(self):
        return COLORS[self.suit]

    def __str__(self):
        return f"{self.rank}{self.suit}" if self.face_up else "XX"

@dataclass
class Pile:
    cards: List[Card] = field(default_factory=list)

    def top(self) -> Optional[Card]:
        return self.cards[-1] if self.cards else None

    def push(self, card: Card):
        self.cards.append(card)

    def pop(self) -> Optional[Card]:
        return self.cards.pop() if self.cards else None

    def is_empty(self):
        return len(self.cards) == 0

class Game:
    def __init__(self):
        self.stock = Pile()
        self.waste = Pile()
        self.foundations: Dict[str, Pile] = {suit: Pile() for suit in SUITS}
        self.tableau: List[List[Card]] = [[] for _ in range(7)]
        self.score = 0
        self.setup()

    def setup(self):
        deck = [Card(rank, suit, face_up=False) for suit in SUITS for rank in RANKS]
        random.shuffle(deck)
        # deal tableau
        for i in range(7):
            for j in range(i + 1):
                card = deck.pop()
                card.face_up = (j == i)
                self.tableau[i].append(card)
        # remaining cards to stock
        for card in deck:
            self.stock.push(card)

    def draw(self):
        if self.stock.is_empty():
            # recycle waste
            while not self.waste.is_empty():
                card = self.waste.pop()
                card.face_up = False
                self.stock.push(card)
            print("Recycling waste to stock")
            self.score -= 15
            return
        card = self.stock.pop()
        card.face_up = True
        self.waste.push(card)

    def can_move_to_tableau(self, card: Card, dest: List[Card]) -> bool:
        if not dest:
            return card.rank == 'K'
        top = dest[-1]
        return top.face_up and COLORS[top.suit] != COLORS[card.suit] and RANKS.index(card.rank) + 1 == RANKS.index(top.rank)

    def can_move_to_foundation(self, card: Card, foundation: Pile) -> bool:
        if foundation.is_empty():
            return card.rank == 'A'
        top = foundation.top()
        return top.suit == card.suit and RANKS.index(card.rank) == RANKS.index(top.rank) + 1

    def move(self, source: str, target: str, count: int = 1):
        src_pile, src_index = self.get_pile(source)
        dst_pile, dst_index = self.get_pile(target)
        if src_pile is None or dst_pile is None:
            print("Invalid piles")
            return False
        flipped = False
        if source.startswith('T') and count > 1:
            movable = src_pile[src_index][-count:]
            if not all(c.face_up for c in movable):
                print("Cannot move face down cards")
                return False
            if not self.can_move_to_tableau(movable[0], dst_pile[dst_index]):
                print("Invalid move")
                return False
            dst_pile[dst_index].extend(movable)
            del src_pile[src_index][-count:]
        else:
            card = src_pile[src_index].pop()
            if target.startswith('T'):
                if not self.can_move_to_tableau(card, dst_pile[dst_index]):
                    print("Invalid move")
                    src_pile[src_index].append(card)
                    return False
                dst_pile[dst_index].append(card)
            elif target.startswith('F'):
                if not self.can_move_to_foundation(card, self.foundations[target[1]]):
                    print("Invalid move")
                    src_pile[src_index].append(card)
                    return False
                self.foundations[target[1]].push(card)
            else:
                print("Invalid target")
                src_pile[src_index].append(card)
                return False
        if source.startswith('T') and src_pile[src_index]:
            if not src_pile[src_index][-1].face_up:
                src_pile[src_index][-1].face_up = True
                flipped = True
        if target.startswith('F'):
            self.score += 10
        else:
            self.score += 5
        if flipped:
            self.score += 5
        return True

    def is_won(self) -> bool:
        """Return True when all foundation piles contain 13 cards."""
        return all(len(self.foundations[suit].cards) == 13 for suit in SUITS)

    def get_pile(self, name: str) -> Tuple[Optional[List], Optional[int]]:
        name = name.upper()
        if name == 'W':
            return [self.waste.cards], 0
        if name == 'STOCK':
            return [self.stock.cards], 0
        if name.startswith('T'):
            idx = int(name[1]) - 1
            return [self.tableau[idx]], 0
        if name.startswith('F'):
            suit = name[1]
            return [self.foundations[suit].cards], 0
        return None, None

    def show(self):
        print("Stock:", len(self.stock.cards))
        print("Waste:", ' '.join(str(c) for c in self.waste.cards))
        for suit in SUITS:
            print(f"Foundation {suit}:", ' '.join(str(c) for c in self.foundations[suit].cards))
        print("Tableau:")
        for i, pile in enumerate(self.tableau):
            print(i + 1, ' '.join(str(c) for c in pile))
        print("Score:", self.score)


def main():
    game = Game()
    while True:
        game.show()
        cmd = input("Command (draw, move SRC DST [N], quit): ").strip()
        if cmd == 'quit':
            break
        elif cmd == 'draw':
            game.draw()
        elif cmd.startswith('move'):
            parts = cmd.split()
            if len(parts) < 3:
                print("Usage: move SRC DST [N]")
                continue
            src = parts[1]
            dst = parts[2]
            count = int(parts[3]) if len(parts) > 3 else 1
            game.move(src, dst, count)
        else:
            print("Unknown command")

if __name__ == '__main__':
    main()
