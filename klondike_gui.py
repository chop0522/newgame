import pygame
from klondike import Game, Card, SUITS, RANKS

CARD_WIDTH = 80
CARD_HEIGHT = 120
MARGIN = 20
BACKGROUND_COLOR = (0, 120, 0)
FACE_COLOR = (255, 255, 255)
BACK_COLOR = (0, 100, 0)

class GameGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Klondike Solitaire")
        self.font = pygame.font.SysFont('arial', 20)
        self.game = Game()
        self.selected = None  # selected pile name

    def draw_card(self, card: Card, x: int, y: int):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        color = FACE_COLOR if card.face_up else BACK_COLOR
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        if card.face_up:
            text = self.font.render(f"{card.rank}{card.suit}", True, (0, 0, 0))
            self.screen.blit(text, (x + 5, y + 5))
        return rect

    def draw_pile_placeholder(self, x: int, y: int):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(self.screen, BACK_COLOR, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        return rect

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.rect_map = {}
        # Stock and waste
        stock_x = MARGIN
        stock_y = MARGIN
        if self.game.stock.cards:
            rect = self.draw_card(self.game.stock.cards[-1], stock_x, stock_y)
        else:
            rect = self.draw_pile_placeholder(stock_x, stock_y)
        self.rect_map[rect] = 'STOCK'

        waste_x = stock_x + CARD_WIDTH + MARGIN
        if self.game.waste.cards:
            rect = self.draw_card(self.game.waste.cards[-1], waste_x, stock_y)
        else:
            rect = self.draw_pile_placeholder(waste_x, stock_y)
        self.rect_map[rect] = 'W'

        # Foundations
        base_x = waste_x + CARD_WIDTH + 3 * MARGIN
        for i, suit in enumerate(SUITS):
            x = base_x + i * (CARD_WIDTH + MARGIN)
            pile = self.game.foundations[suit].cards
            if pile:
                rect = self.draw_card(pile[-1], x, stock_y)
            else:
                rect = self.draw_pile_placeholder(x, stock_y)
            self.rect_map[rect] = f'F{suit}'

        # Tableau
        table_y = stock_y + CARD_HEIGHT + MARGIN
        for i, pile in enumerate(self.game.tableau):
            x = MARGIN + i * (CARD_WIDTH + MARGIN)
            for j, card in enumerate(pile):
                y = table_y + j * 30
                rect = self.draw_card(card, x, y)
                self.rect_map[rect] = f'T{i+1}'

        pygame.display.flip()

    def handle_click(self, pos):
        for rect, name in self.rect_map.items():
            if rect.collidepoint(pos):
                if name == 'STOCK':
                    self.game.draw()
                    return
                if self.selected is None:
                    self.selected = name
                else:
                    if self.selected != name:
                        self.game.move(self.selected, name)
                    self.selected = None
                return

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)
            clock.tick(30)
        pygame.quit()

if __name__ == '__main__':
    GameGUI().run()
