# Klondike Solitaire Game

This repository contains a simple Klondike Solitaire implementation written in Python. A command line interface is always available and a basic GUI built with `pygame` is also provided.

## Requirements

- Python 3.11 or later
- `pytest` for running the tests
- `pygame` for the optional GUI (install via `pip install pygame`)

## Playing on the Command Line

Run the following command:

```bash
python3 klondike.py
```

You will see the game state printed in the terminal. Use the following commands:

- `draw` – draw one card from the stock to the waste. When the stock is empty, the waste is recycled back into the stock.
- `move SRC DST [N]` – move cards from `SRC` pile to `DST` pile. `SRC` and `DST` can be `T1`..`T7` (tableau piles), `F<SUIT>` (foundation piles: `FH` `FD` `FC` `FS`), `W` (waste), or `STOCK`.
  - `N` is optional number of cards to move (default is 1). Moving multiple cards is only allowed within the tableau.
- `quit` – exit the game.

Example move: `move T7 FH` moves the top card from tableau pile 7 to the hearts foundation.

## Playing the GUI Version

Install `pygame` and run:

```bash
python3 klondike_gui.py
```

Click the stock to draw a card. Select a card or pile and then click another pile to move the card(s). Close the window or press the quit button to exit.

## Running Tests

Install `pytest` and run:

```bash
python3 -m pytest
```

This will run the unit tests located in the `tests` directory.
