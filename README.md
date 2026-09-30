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

## Dependencies

- Python 3.11
- PySide6
- pytest (for running unit tests)

---

## Usage

```bash
conda env create -f environment.yml
conda activate skat
python src/main.py
```
