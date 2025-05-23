# Klondike Solitaire Game

This repository contains a simple implementation of Klondike Solitaire written in Python. The game can be played in the terminal or with a basic GUI built using `pygame`.

## Requirements

- Python 3.11 or later
- `pygame` (optional, required only for the GUI)

## Playing the Game (CLI)

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

## Playing the Game (GUI)

If you have `pygame` installed, you can launch a basic GUI with:

```bash
python3 klondike_gui.py
```

Click the stock pile to draw cards. Click a card or pile to select it and then click another pile to perform a move.

## Running Tests

Run the following command:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

This will run the unit tests located in the `tests` directory.
