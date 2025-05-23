# Klondike Solitaire Game

This repository contains a simple implementation of Klondike Solitaire written in Python.
The original version runs in the command line and a basic GUI using `pygame` is also provided.

## Requirements

- Python 3.11 or later
- Optional: `pytest` if you prefer running the tests with it

## Playing the Game

Run the following command for the command line version:

```bash
python3 klondike.py
```

To play the GUI version (requires `pygame`), run:

```bash
python3 klondike_gui.py
```

You will see the game state printed in the terminal. Use the following commands:

- `draw` – draw one card from the stock to the waste. When the stock is empty, the waste is recycled back into the stock.
- `move SRC DST [N]` – move cards from `SRC` pile to `DST` pile. `SRC` and `DST` can be `T1`..`T7` (tableau piles), `F<SUIT>` (foundation piles: `FH` `FD` `FC` `FS`), `W` (waste), or `STOCK`.
  - `N` is optional number of cards to move (default is 1). Moving multiple cards is only allowed within the tableau.
- `quit` – exit the game.

Example move: `move T7 FH` moves the top card from tableau pile 7 to the hearts foundation.

## Running Tests

Run the following command:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

This runs the unit tests located in the `tests` directory. If you have
`pytest` installed you can still run the tests with:

```bash
python3 -m pytest
```
