# Connect Four with Monte Carlo AI

A Python-based implementation of the "Connect Four" game featuring an AI opponent powered by **Monte Carlo simulations**.

## 🧠 AI Strategy (How it works)
The core of this project is a simulation-based decision-making algorithm that allows the computer to play intelligently without hard-coded strategy rules.

1. **Candidate Evaluation:** For every possible legal move in the current turn, the AI initiates a testing phase.
2. **Monte Carlo Simulation:** The algorithm runs **300 full-game simulations** (`sim_count=300`) for each candidate move.
   * Inside these simulations, both the PC and the "human" play random valid moves until the game ends (Win/Loss/Tie).
3. **Statistical Analysis:** The AI calculates the win rate for each candidate move based on the simulation results.
4. **Optimal Decision:** It selects the move with the highest statistical probability of victory.

## Game Mechanics
* **Grid:** 6x6 dynamic board (customizable).
* **Rules:** Standard Connect Four logic—gravity applies (symbols drop to the lowest available row).
* **Win Condition:** Connect 4 symbols horizontally, vertically, or diagonally.

## How to Run
Requires Python 3. No external dependencies needed.

```bash
python main.py
```

## Configuration
You can adjust the game parameters at the bottom of the script:
* `tictactoe(rows, cols, human_starts)`: Change board size or starting player.
* `sim_count`: Adjust inside `monte_carlo_sim` to balance between speed (lower count) and intelligence (higher count).
