# connect-4-minmax-alphabeta

## Instructions

You will need python installed. To run this application, just open the main.py file in Python.

You will be prompted for your move selection: 1-7 corresponding to a column.

Your will see the updated board and then press Enter to end your turn.

The AI will quickly complete its turn and then you will be prompted for your next move.

The game will continue until either you or the AI win or if the board completely fills up.


## Analysis

## Comparison of Minimax and Alpha-Beta Pruning

Alpha-beta pruning allowed for significantly deeper exploration of the game tree with little impact to performance. This improved algorithm allowed me to push the potential exploration depth all the way to 42, the deepest that a game tree can reach for Connect 4. Still, the algorithm still averages less than a tenth of a second to find the optimal path.

Minimax performs much worse. I had to limit the depth 4 in order to make the game playable. At a max exploration depth of 5, the AI takes roughly 12 seconds to compute its optimal path.

## Can Alpha-Beta Be Beaten?

During the early stages of developing this algorithm, I started with a max search depth of 7 because I was hesitant to push the algorithm beyond the minimum game depth and cause an error. After changing some of the logic in the algorithm, I felt more comfortable pushing the max search depth to 42 and had no issue. It was interesting to see the change in game performance with that change fro 7 to 42. At 7-ply looks ahead, the AI was difficulty but I could defeat it about %10 percent of the time. Now that I've changed it to 42-ply looks ahead it's quite capable of beating me every time. I'm not sure if it has an undefeatable strategy, but it's certainly difficult to beat.
