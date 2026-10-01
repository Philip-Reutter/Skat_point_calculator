# Skat Point Calculator

A Python desktop application and calculation engine designed to automate scorekeeping and rule validation for the card game Skat.

---

## Overview

This project provides an interactive tool for tracking Skat games, applying official scoring rules, and managing players across multiple rounds. It eliminates manual score errors by automatically evaluating game parameters, suit multipliers, and special game modifiers.
The core evaluation logic is kept separate from the user interface and validated using pytest.

---

## Features

- Official Skat scoring logic
- Interactive PySide6 German language GUI (localized for traditional Skat terminology) for seamless match tracking
- Custom dialogs for player setup and starting new rounds
- Unit tests with `pytest` for core scoring functions

---

## How to Play

- **New Game Setup:** Set up player names and optionally avatars and start a new session via the menu.
- **Enter new Game (Round):** Enter game conditions to calculate and log scores automatically in an overview.
- **Delete last Game (Round):** Option to remove last game if error was made entering the game conditions.
- **Add new player:** Option to add a new player (up to five) after the game was started with less players.

---

## Repository Structure

```text
Skat_point_calculator/
├── src/
│   ├── logic/                         # Core calculation rules & game multipliers
│   │   ├── base_values.py             # Constant base values for game types
│   │   └── skat_calculator.py         # Main calculation algorithm & score logic
│   ├── ui/                            # GUI components & user interface
│   │   ├── main_window.py             # Primary application window
│   │   ├── new_game_dialog.py         # Game setup & round configuration dialog
│   │   └── player_setup_dialog.py     # Player setup interface
│   └── main.py                        # Application entry point
├── tests/                             # Automated test suites
│   └── test_skat_calculator.py        # Unit tests for calculation & scoring rules
├── .gitignore
├── environment.yml
├── pytest.ini                         # Pytest setup & PYTHONPATH configuration
└── README.md
```

---

## Dependencies

- Python 3.11
- PySide6
- pytest (for running unit tests)

---

## Usage

```bash
conda env create -f environment.yml
conda activate skat

# execute unit tests
pytest

# run main application
python src/main.py
```
