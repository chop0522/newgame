import sys

try:
    import pygame
except ImportError:
    print("pygame is required for the GUI")
    sys.exit(1)

from klondike import Game, SUITS

CARD_WIDTH = 80
CARD_HEIGHT = 120
OFFSET_Y = 30

SCREEN_WIDTH = CARD_WIDTH * 7 + 80
SCREEN_HEIGHT = 600

GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (0, 0, 200)


def draw_card(screen, card, x, y, font):
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    if card.face_up:
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        color = RED if card.color() == 'red' else BLACK
        text = font.render(f"{card.rank}{card.suit}", True, color)
        screen.blit(text, (x + 5, y + 5))
    else:
        pygame.draw.rect(screen, BLUE, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)


class GameGUI:
    def __init__(self):
        pygame.init()
        self.game = Game()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Klondike Solitaire")
        self.font = pygame.font.SysFont(None, 24)
        self.selected = None  # (pile_name, count)

        self.positions = self.build_positions()

    def build_positions(self):
        pos = {}
        # top row
        pos['STOCK'] = (20, 20)
        pos['W'] = (20 + CARD_WIDTH + 20, 20)
        fx = 20 + 2 * (CARD_WIDTH + 20)
        for i, suit in enumerate(SUITS):
            pos[f'F{suit}'] = (fx + i * (CARD_WIDTH + 20), 20)
        # tableau
        for i in range(7):
            pos[f'T{i+1}'] = (20 + i * (CARD_WIDTH + 20), 180)
        return pos

    def hit_test(self, pos):
        x, y = pos
        for name, (px, py) in self.positions.items():
            if name.startswith('T'):
                pile = self.game.tableau[int(name[1]) - 1]
                for idx in range(len(pile)):
                    rx = px
                    ry = py + idx * OFFSET_Y
                    rect = pygame.Rect(rx, ry, CARD_WIDTH, CARD_HEIGHT)
                    if rect.collidepoint(x, y):
                        count = len(pile) - idx
                        return name, count
            else:
                rect = pygame.Rect(px, py, CARD_WIDTH, CARD_HEIGHT)
                if rect.collidepoint(x, y):
                    return name, 1
        return None, None

    def draw_board(self):
        self.screen.fill(GREEN)
        # draw piles
        for name, (px, py) in self.positions.items():
            if name.startswith('T'):
                pile = self.game.tableau[int(name[1]) - 1]
                for i, card in enumerate(pile):
                    y = py + i * OFFSET_Y
                    draw_card(self.screen, card, px, y, self.font)
            elif name == 'STOCK':
                if self.game.stock.cards:
                    pygame.draw.rect(self.screen, BLUE, (px, py, CARD_WIDTH, CARD_HEIGHT))
                    pygame.draw.rect(self.screen, BLACK, (px, py, CARD_WIDTH, CARD_HEIGHT), 1)
                else:
                    pygame.draw.rect(self.screen, BLACK, (px, py, CARD_WIDTH, CARD_HEIGHT), 1)
            elif name == 'W':
                if self.game.waste.cards:
                    card = self.game.waste.cards[-1]
                    draw_card(self.screen, card, px, py, self.font)
                else:
                    pygame.draw.rect(self.screen, BLACK, (px, py, CARD_WIDTH, CARD_HEIGHT), 1)
            elif name.startswith('F'):
                suit = name[1]
                pile = self.game.foundations[suit]
                if pile.cards:
                    card = pile.cards[-1]
                    draw_card(self.screen, card, px, py, self.font)
                else:
                    pygame.draw.rect(self.screen, BLACK, (px, py, CARD_WIDTH, CARD_HEIGHT), 1)

        # highlight selection
        if self.selected:
            name, count = self.selected
            px, py = self.positions[name]
            if name.startswith('T'):
                pile = self.game.tableau[int(name[1]) - 1]
                idx = len(pile) - count
                y = py + idx * OFFSET_Y
            else:
                y = py
            pygame.draw.rect(self.screen, RED, (px - 2, y - 2, CARD_WIDTH + 4, CARD_HEIGHT + 4), 2)

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    name, count = self.hit_test(event.pos)
                    if not name:
                        continue
                    if name == 'STOCK':
                        self.game.draw()
                    else:
                        if self.selected is None:
                            self.selected = (name, count)
                        else:
                            src, cnt = self.selected
                            self.game.move(src, name, cnt)
                            self.selected = None
            self.draw_board()
            clock.tick(30)
        pygame.quit()


def main():
    gui = GameGUI()
    gui.run()


if __name__ == '__main__':
    main()
