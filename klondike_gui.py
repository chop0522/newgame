import pygame
from klondike import Game, SUITS, COLORS

CARD_WIDTH = 80
CARD_HEIGHT = 120
OFFSET_Y = 20
BG_COLOR = (0, 128, 0)
RESET_RECT = pygame.Rect(750, 20, 100, 40)

class KlondikeGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 700))
        pygame.display.set_caption('Klondike Solitaire')
        self.font = pygame.font.SysFont(None, 24)
        self.game = Game()
        self.selected = None  # tuple(source, count)
        self.selected_rect = None
        self.win = False

    def draw_card(self, card, x, y):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        if card.face_up:
            pygame.draw.rect(self.screen, (255, 255, 255), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            text_color = (200, 0, 0) if COLORS[card.suit] == 'red' else (0, 0, 0)
            text = self.font.render(f'{card.rank}{card.suit}', True, text_color)
            self.screen.blit(text, (x + 5, y + 5))
        else:
            pygame.draw.rect(self.screen, (50, 50, 50), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

    def draw_pile(self, pile, x, y):
        if not pile:
            pygame.draw.rect(self.screen, (50, 50, 50), (x, y, CARD_WIDTH, CARD_HEIGHT), 2)
            return
        for i, card in enumerate(pile):
            self.draw_card(card, x, y + i * OFFSET_Y)

    def render(self):
        self.screen.fill(BG_COLOR)
        # stock and waste
        self.draw_pile(self.game.stock.cards[-1:], 20, 20)
        self.draw_pile(self.game.waste.cards[-1:], 120, 20)
        # foundations
        fx = 300
        for suit in SUITS:
            self.draw_pile(self.game.foundations[suit].cards[-1:], fx, 20)
            fx += 100
        # tableau
        ty = 160
        for i, pile in enumerate(self.game.tableau):
            self.draw_pile(pile, 20 + i * 100, ty)
        if self.selected_rect:
            pygame.draw.rect(self.screen, (255, 255, 0), self.selected_rect, 3)

        pygame.draw.rect(self.screen, (200, 200, 200), RESET_RECT)
        pygame.draw.rect(self.screen, (0, 0, 0), RESET_RECT, 2)
        text = self.font.render('Reset', True, (0, 0, 0))
        text_rect = text.get_rect(center=RESET_RECT.center)
        self.screen.blit(text, text_rect)

        score_surface = self.font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (20, 140))

        if self.win:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            win_text = self.font.render('You Won!', True, (255, 255, 0))
            win_rect = win_text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(win_text, win_rect)

        pygame.display.flip()

    def select_from_tableau(self, index, y):
        pile = self.game.tableau[index]
        if not pile:
            return
        card_index = (y - 160) // OFFSET_Y
        if card_index < 0:
            card_index = 0
        if card_index >= len(pile):
            card_index = len(pile) - 1
        if not pile[card_index].face_up:
            return
        count = len(pile) - card_index
        self.selected = (f'T{index + 1}', count)
        x = 20 + index * 100
        y_pos = 160 + card_index * OFFSET_Y
        height = CARD_HEIGHT + OFFSET_Y * (count - 1)
        self.selected_rect = pygame.Rect(x, y_pos, CARD_WIDTH, height)

    def handle_click(self, pos):
        x, y = pos
        if RESET_RECT.collidepoint(x, y):
            self.game = Game()
            self.selected = None
            self.selected_rect = None
            self.win = False
            return
        # stock click
        if 20 <= x <= 20 + CARD_WIDTH and 20 <= y <= 20 + CARD_HEIGHT:
            self.game.draw()
            self.selected = None
            self.selected_rect = None
            self.win = self.game.is_won()
            return
        # waste click
        if 120 <= x <= 120 + CARD_WIDTH and 20 <= y <= 20 + CARD_HEIGHT:
            if self.selected:
                src, count = self.selected
                self.game.move(src, 'W', count)
                self.selected = None
                self.selected_rect = None
                self.win = self.game.is_won()
            else:
                if self.game.waste.cards:
                    self.selected = ('W', 1)
                    self.selected_rect = pygame.Rect(120, 20, CARD_WIDTH, CARD_HEIGHT)
            return
        # foundation clicks
        fx = 300
        for suit in SUITS:
            if fx <= x <= fx + CARD_WIDTH and 20 <= y <= 20 + CARD_HEIGHT:
                if self.selected:
                    src, count = self.selected
                    self.game.move(src, f'F{suit}', count)
                    self.selected = None
                    self.selected_rect = None
                    self.win = self.game.is_won()
                else:
                    if self.game.foundations[suit].cards:
                        self.selected = (f'F{suit}', 1)
                        self.selected_rect = pygame.Rect(fx, 20, CARD_WIDTH, CARD_HEIGHT)
                return
            fx += 100
        # tableau clicks
        for i in range(7):
            tx = 20 + i * 100
            if tx <= x <= tx + CARD_WIDTH and y >= 160:
                if self.selected:
                    src, count = self.selected
                    self.game.move(src, f'T{i + 1}', count)
                    self.selected = None
                    self.selected_rect = None
                    self.win = self.game.is_won()
                else:
                    self.select_from_tableau(i, y)
                return

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
            if not self.win and self.game.is_won():
                self.win = True
            self.render()
            clock.tick(30)
        pygame.quit()


def main():
    KlondikeGUI().run()


if __name__ == '__main__':
    main()
