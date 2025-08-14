Mancala AI
A competitive Mancala AI implementation using minimax algorithm with alpha-beta pruning, designed for tournament play.

Features

Minimax Algorithm: Uses minimax with alpha-beta pruning for optimal decision making
Time Management: Operates within 900ms time limit per move
Iterative Deepening: Gradually increases search depth up to 12 levels
Move Ordering: Prioritizes moves with higher seed counts for better pruning
PIE Rule Support: Implements the swap rule for competitive play
Capture Detection: Recognizes and evaluates capture opportunities
Extra Turn Logic: Properly handles landing in store for additional moves

Game Rules
The AI follows standard Mancala (Kalah) rules:

6 pits per player with 1 store each
Players alternate turns picking up seeds and distributing them
Landing in your store grants an extra turn
Capturing occurs when your last seed lands in an empty pit on your side
Game ends when one player's side is empty
Player with most seeds in their store wins

Algorithm Details
Minimax with Alpha-Beta Pruning

Search Depth: Up to 12 levels with iterative deepening
Time Limit: 900ms per move with early termination
Evaluation: Focuses on score difference with terminal state bonuses
Move Ordering: Sorts moves by pit seed count for better pruning efficiency

Heuristic Function
Currently uses a simplified evaluation focusing on:

Eventually settled on the score difference and 
terminal state detection with depth bonuses.
Another custom hueristic could imporve performance.

Input Format
The program expects a single line of input with space-separated values:
MOVE N p1_pit1 p1_pit2 ... p1_pit6 p2_pit1 p2_pit2 ... p2_pit6 p1_score p2_score turn player
Where:

MOVE: Command type
N: Number of pits per side (typically 6)
p1_pit1-6: Seeds in player 1's pits
p2_pit1-6: Seeds in player 2's pits
p1_score, p2_score: Current scores
turn: Turn number
player: Current player (1 or 2)

Output

Returns the chosen move (1-6) representing the pit to play
Returns "PIE" when invoking the swap rule (turns 2-3 for player 2)

Usage
Compilation
bashjavac Main.java


GameState: Represents the current game state including board, turn, and player
miniMax(): Core minimax algorithm with alpha-beta pruning
findBestMove(): Main decision-making function with iterative deepening
simulateMove(): Applies moves to create new game states
Turn(): Handles move execution including captures and extra turns
StateParser(): Parses input format into GameState objects

Performance Optimizations

Alpha-Beta Pruning: Reduces search tree size significantly
Move Ordering: Examines promising moves first for better pruning
Time Management: Prevents timeout with early search termination
Iterative Deepening: Ensures best move is always available within time limit

Future Improvements

Enhanced heuristic function with positional evaluation
Opening book for early game optimization
Endgame tablebase for perfect endgame play
Machine learning integration for position evaluation
Transposition tables for repeated position detection

Tournament Performance
This AI is optimized for competitive play with:

Consistent sub-900ms response times
Strategic PIE rule usage
Robust error handling
Deterministic behavior with randomization tie-breaking


Example of a Game Played Against Another Bot

Sending STATE 6 4 4 4 4 4 4 4 4 4 4 4 4 0 0 1 1 to player 1
Turn 1, Player 1 move: 3
Sending STATE 6 4 4 0 5 5 5 4 4 4 4 4 4 1 0 2 1 to player 1
Turn 2, Player 1 move: 6
Sending STATE 6 4 4 0 5 5 0 5 5 5 5 4 4 2 0 3 2 to player 2
Turn 3, Player 2 move: 5
Sending STATE 6 5 5 0 5 5 0 5 5 5 5 0 5 2 1 4 1 to player 1
Turn 4, Player 1 move: 2
Sending STATE 6 5 0 1 6 6 1 5 5 5 5 0 5 3 1 5 1 to player 1
Turn 5, Player 1 move: 6
Sending STATE 6 5 0 1 6 6 0 5 5 5 5 0 5 4 1 6 1 to player 1
Turn 6, Player 1 move: 1
Player 1 captures 6 stones!
Sending STATE 6 0 1 2 7 7 0 0 5 5 5 0 5 10 1 7 2 to player 2
Turn 7, Player 2 move: 6
Sending STATE 6 1 2 3 8 7 0 0 5 5 5 0 0 10 2 8 1 to player 1
Turn 8, Player 1 move: 4
Sending STATE 6 1 2 3 0 8 1 1 6 6 6 1 0 11 2 9 2 to player 2
Turn 9, Player 2 move: 2
Sending STATE 6 2 2 3 0 8 1 1 0 7 7 2 1 11 3 10 1 to player 1
Turn 10, Player 1 move: 6
Sending STATE 6 2 2 3 0 8 0 1 0 7 7 2 1 12 3 11 1 to player 1
Turn 11, Player 1 move: 5
Sending STATE 6 2 2 3 0 0 1 2 1 8 8 3 2 13 3 12 2 to player 2
Turn 12, Player 2 move: 5
Sending STATE 6 3 2 3 0 0 1 2 1 8 8 0 3 13 4 13 1 to player 1
Turn 13, Player 1 move: 1
Player 1 captures 9 stones!
Sending STATE 6 0 3 4 0 0 1 2 1 0 8 0 3 22 4 14 2 to player 2
Turn 14, Player 2 move: 1
Sending STATE 6 0 3 4 0 0 1 0 2 1 8 0 3 22 4 15 1 to player 1
Turn 15, Player 1 move: 2
Player 1 captures 3 stones!
Sending STATE 6 0 0 5 1 0 1 0 0 1 8 0 3 25 4 16 2 to player 2
Turn 16, Player 2 move: 3
Sending STATE 6 0 0 5 1 0 1 0 0 0 9 0 3 25 4 17 1 to player 1
Turn 17, Player 1 move: 4
Sending STATE 6 0 0 5 0 1 1 0 0 0 9 0 3 25 4 18 2 to player 2
Turn 18, Player 2 move: 6
Sending STATE 6 1 1 5 0 1 1 0 0 0 9 0 0 25 5 19 1 to player 1
Turn 19, Player 1 move: 1
Sending STATE 6 0 2 5 0 1 1 0 0 0 9 0 0 25 5 20 2 to player 2
Turn 20, Player 2 move: 4
Sending STATE 6 1 3 6 1 2 2 0 0 0 0 1 1 25 6 21 1 to player 1
Turn 21, Player 1 move: 2
Sending STATE 6 1 0 7 2 3 2 0 0 0 0 1 1 25 6 22 2 to player 2
Turn 22, Player 2 move: 5
Sending STATE 6 1 0 7 2 3 2 0 0 0 0 0 2 25 6 23 1 to player 1
Turn 23, Player 1 move: 1
Sending STATE 6 0 1 7 2 3 2 0 0 0 0 0 2 25 6 24 2 to player 2
Turn 24, Player 2 move: 6
Game Over
Final Scores: Player 1: 41, Player 2: 7
Player 1 wins!
WIN 1
