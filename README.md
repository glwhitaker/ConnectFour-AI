# Connect Four AI

A Python implementation of Connect Four featuring three different AI algorithms: Minimax, Alpha-Beta Pruning, and Expectimax. The game includes a graphical interface and supports Human vs Human, Human vs AI, and AI vs AI gameplay.

## Features

- **Multiple Game Modes**
  - Human vs Human
  - Human vs AI
  - AI vs AI

- **Three AI Algorithms**
  - Standard Minimax with depth limiting
  - Alpha-Beta Pruning (optimized Minimax)
  - Expectimax (for random/probabilistic opponents)

- **Configurable Settings**
  - Adjustable search depth for AI
  - Choice of AI algorithm for each player
  - Interactive GUI interface

## AI Implementation

### Minimax
Standard depth-limited minimax algorithm where:
- MAX player tries to maximize their score
- MIN player tries to minimize MAX's score
- Evaluation is always from MAX's perspective

### Alpha-Beta Pruning
Enhanced version of minimax that:
- Maintains identical decision-making
- Improves efficiency by pruning irrelevant branches
- Typically allows for greater search depths

### Expectimax
Probabilistic version of minimax where:
- MAX nodes behave as in standard minimax
- MIN nodes are replaced with chance nodes
- Opponent moves are assumed to be uniformly random

## Usage

Run the game using:
```python
python connect4.py
```

The GUI will allow you to:
1. Select player types (Human/AI)
2. Choose AI algorithms
3. Set search depths
4. Start and play the game

## Technical Details

The implementation uses:
- Tkinter for the GUI
- Depth-limited search to manage complexity
- Heuristic evaluation function for non-terminal states
- Object-oriented design for game state management

## Evaluation Function

The game uses a sophisticated evaluation function that considers:
- Number of potential winning sequences
- Weighted scoring based on piece configurations
- Both offensive and defensive positions

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)