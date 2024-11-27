# connect4.py
# Grayson Whitaker
# CPSC 4420-001
# Assignment 4

# use math library if needed
import math

def get_child_boards(player, board):
    """
    Generate a list of succesor boards obtained by placing a disc 
    at the given board for a given player
   
    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that will place a disc on the board
    board: the current board instance

    Returns
    -------
    a list of (col, new_board) tuples,
    where col is the column in which a new disc is placed (left column has a 0 index), 
    and new_board is the resulting board instance
    """
    res = []
    for c in range(board.cols):
        if board.placeable(c):
            tmp_board = board.clone()
            tmp_board.place(player, c)
            res.append((c, tmp_board))
    return res


def evaluate(player, board):
    """
    This is a function to evaluate the advantage of the specific player at the
    given game board.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the specific player
    board: the board instance

    Returns
    -------
    score: float
        a scalar to evaluate the advantage of the specific player at the given
        game board
    """
    adversary = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    # Initialize the value of scores
    # [s0, s1, s2, s3, --s4--]
    # s0 for the case where all slots are empty in a 4-slot segment
    # s1 for the case where the player occupies one slot in a 4-slot line, the rest are empty
    # s2 for two slots occupied
    # s3 for three
    # s4 for four
    score = [0]*5
    adv_score = [0]*5

    # Initialize the weights
    # [w0, w1, w2, w3, --w4--]
    # w0 for s0, w1 for s1, w2 for s2, w3 for s3
    # w4 for s4
    weights = [0, 1, 4, 16, 1000]

    # Obtain all 4-slot segments on the board
    seg = []
    invalid_slot = -1
    left_revolved = [
        [invalid_slot]*r + board.row(r) + \
        [invalid_slot]*(board.rows-1-r) for r in range(board.rows)
    ]
    right_revolved = [
        [invalid_slot]*(board.rows-1-r) + board.row(r) + \
        [invalid_slot]*r for r in range(board.rows)
    ]
    for r in range(board.rows):
        # row
        row = board.row(r) 
        for c in range(board.cols-3):
            seg.append(row[c:c+4])
    for c in range(board.cols):
        # col
        col = board.col(c) 
        for r in range(board.rows-3):
            seg.append(col[r:r+4])
    for c in zip(*left_revolved):
        # slash
        for r in range(board.rows-3):
            seg.append(c[r:r+4])
    for c in zip(*right_revolved): 
        # backslash
        for r in range(board.rows-3):
            seg.append(c[r:r+4])
    # compute score
    for s in seg:
        if invalid_slot in s:
            continue
        if adversary not in s:
            score[s.count(player)] += 1
        if player not in s:
            adv_score[s.count(adversary)] += 1
    reward = sum([s*w for s, w in zip(score, weights)])
    penalty = sum([s*w for s, w in zip(adv_score, weights)])
    return reward - penalty


def minimax(player, board, depth_limit):
    """
    Minimax algorithm with limited search depth.
    """
    max_player = player
    placement = None

    def value(player, board, depth_limit):
        # Base cases: terminal state or depth limit reached
        if board.terminal() or depth_limit == 0:
            return evaluate(max_player, board)
        
        # Max player's turn
        if player == max_player:
            return max_value(player, board, depth_limit)
        # Min player's turn
        else:
            return min_value(player, board, depth_limit)

    def max_value(player, board, depth_limit):
        v = -math.inf
        # Get all possible moves
        successors = get_child_boards(player, board)
        # No valid moves available
        if not successors:
            return evaluate(max_player, board)
        
        next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
        # Try each possible move
        for _, new_board in successors:
            v = max(v, value(next_player, new_board, depth_limit - 1))
        return v

    def min_value(player, board, depth_limit):
        v = math.inf
        # Get all possible moves
        successors = get_child_boards(player, board)
        # No valid moves available
        if not successors:
            return evaluate(max_player, board)
        
        next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
        # Try each possible move
        for _, new_board in successors:
            v = min(v, value(next_player, new_board, depth_limit - 1))
        return v

    # Get the next player
    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    score = -math.inf

    # Try each possible move and select the one with the highest value
    for col, new_board in get_child_boards(player, board):
        val = value(next_player, new_board, depth_limit - 1)
        if val > score:
            score = val
            placement = col

    return placement


def alphabeta(player, board, depth_limit):
    """
    Minimax algorithm with alpha-beta pruning.
    """
    max_player = player
    placement = None

    def value(player, board, depth_limit, alpha, beta):
        # Base cases: terminal state or depth limit reached
        if board.terminal() or depth_limit == 0:
            return evaluate(max_player, board)
        
        # Max player's turn
        if player == max_player:
            return max_value(player, board, depth_limit, alpha, beta)
        # Min player's turn
        else:
            return min_value(player, board, depth_limit, alpha, beta)

    def max_value(player, board, depth_limit, alpha, beta):
        v = -math.inf
        # Get all possible moves
        successors = get_child_boards(player, board)
        # No valid moves available
        if not successors:
            return evaluate(max_player, board)
        
        next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
        # Try each possible move
        for _, new_board in successors:
            v = max(v, value(next_player, new_board, depth_limit - 1, alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:  # Pruning condition
                break
        return v

    def min_value(player, board, depth_limit, alpha, beta):
        v = math.inf
        # Get all possible moves
        successors = get_child_boards(player, board)
        # No valid moves available
        if not successors:
            return evaluate(max_player, board)
        
        next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
        # Try each possible move
        for _, new_board in successors:
            v = min(v, value(next_player, new_board, depth_limit - 1, alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:  # Pruning condition
                break
        return v

    # Get the next player
    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    score = -math.inf
    alpha = -math.inf
    beta = math.inf

    # Try each possible move and select the one with the highest value
    for col, new_board in get_child_boards(player, board):
        val = value(next_player, new_board, depth_limit - 1, alpha, beta)
        if val > score:
            score = val
            placement = col
        alpha = max(alpha, score)
        if beta <= alpha:
            break

    return placement


def expectimax(player, board, depth_limit):
    """
    Expectimax algorithm with random adversary.
    """
    max_player = player
    placement = None

    def value(player, board, depth_limit):
        # Base cases: terminal state or depth limit reached
        if board.terminal() or depth_limit == 0:
            return evaluate(max_player, board)
        
        # Max player's turn
        if player == max_player:
            return max_value(player, board, depth_limit)
        # Chance node (opponent plays randomly)
        else:
            return exp_value(player, board, depth_limit)

    def max_value(player, board, depth_limit):
        v = -math.inf
        # Get all possible moves
        successors = get_child_boards(player, board)
        # No valid moves available
        if not successors:
            return evaluate(max_player, board)
        
        next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
        # Try each possible move
        for _, new_board in successors:
            v = max(v, value(next_player, new_board, depth_limit - 1))
        return v

    def exp_value(player, board, depth_limit):
        v = 0
        # Get all possible moves
        successors = get_child_boards(player, board)
        # No valid moves available
        if not successors:
            return evaluate(max_player, board)
        
        next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
        # Calculate expected value (average) of all possible moves
        probability = 1.0 / len(successors)  # Uniform random probability
        for _, new_board in successors:
            v += probability * value(next_player, new_board, depth_limit - 1)
        return v

    # Get the next player
    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    score = -math.inf

    # Try each possible move and select the one with the highest expected value
    for col, new_board in get_child_boards(player, board):
        val = value(next_player, new_board, depth_limit - 1)
        if val > score:
            score = val
            placement = col

    return placement


if __name__ == "__main__":
    from utils.app import App
    import tkinter

    algs = {
        "Minimax": minimax,
        "Alpha-beta pruning": alphabeta,
        "Expectimax": expectimax
    }

    root = tkinter.Tk()
    App(algs, root)
    root.mainloop()
