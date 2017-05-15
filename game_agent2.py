"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO 4: finish this function!
    #raise NotImplementedError
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves     = len(game.get_legal_moves(player))
    opp_moves     = len(game.get_legal_moves(game.get_opponent(player)))
    filled_spaces = (game.width*game.height) - len(game.get_blank_spaces())

    WEIGHT1_A = 1
    WEIGHT1_B = -3
    WEIGHT1_C = 1

    return (float) (WEIGHT1_A * own_moves) + (WEIGHT1_B * opp_moves) + (WEIGHT1_C * filled_spaces)
    #return (float)(own_moves - 2*opp_moves) * filled_spaces
    #return float(len(game.get_legal_moves(player)))

def custom_score_2(game, player):
    """Defensive scorer!
    This scorer outputs the opponents worst score as the highest score

    Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    # TODO 5: finish this function!

    """
    if game.is_loser(player):
        return float("-inf")
    
    if game.is_winner(player):
        return float("inf")

    WEIGHT2_A = 1
    WEIGHT2_B = 3
    WEIGHT2_C = 1

    return (float) (WEIGHT2_A * own_moves) + (WEIGHT2_B * opp_moves) + (WEIGHT2_C * filled_spaces)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO 6: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    WEIGHT3_A = 1
    WEIGHT3_B = 3
    WEIGHT3_C = 1

    return (float) (WEIGHT3_A * own_moves) + (WEIGHT3_B * opp_moves) + (WEIGHT3_C * filled_spaces)
    

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    #def __init__(self, search_depth=3, score_fn=custom_score_2, timeout=10.):
    def __init__(self, search_depth=4, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """
    
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # -----WIKIPEDIA ALGORITHM
        #
        #01 function minimax(node, depth, maximizingPlayer)
        #02     if depth = 0 or node is a terminal node (No children)
        #03         return the heuristic value of node
        #
        #04     if maximizingPlayer
        #05         bestValue := -8
        #06         for each child of node
        #07             v := minimax(child, depth - 1, FALSE)
        #08             bestValue := max(bestValue, v)
        #09         return bestValue
        # 
        #10     else    (* minimizing player *)
        #11         bestValue := +8
        #12         for each child of node
        #13             v := minimax(child, depth - 1, TRUE)
        #14             bestValue := min(bestValue, v)
        #15         return bestValue
        legal_moves = game.get_legal_moves(game.active_player) 
        if not legal_moves: 
            return 0

        if depth == 0:
            return self.score(game, self)
       
        #max player
        if (game.active_player == self):
            final_score = -100000
            for m in legal_moves:
                new_game = game.forecast_move(m) #create new board with change
                score = self.minimax_value(new_game, depth-1)
                if score > final_score:
                    final_score = score

        #min player
        else:
            final_score = 100000
            for m in legal_moves:
                new_game = game.forecast_move(m) #create new board with change
                score = self.minimax_value(new_game, depth-1)
                if score < final_score:
                    final_score = score
        return final_score

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO 1: finish this function!
        #print("MY LEGAL MOVES", game.get_legal_moves(game.active_player), (game.active_player == self), "dpt=", depth)
        #print("\nBoard:\n{}".format(game.to_string()))

        legal_moves = game.get_legal_moves(game.active_player)

        if not legal_moves:
            #print ("No legal moves, we are about to lose!")
            #print("\nBoard:\n{}".format(game.to_string()))
            return (-1, -1)
        
        if depth == 0: #is this necessary at the root level? shouldn't be...
            #print("dpt=0, score=", self.score(game, self) )
            return self.score(game, self)

        Chosen_Move = (-1,-1)
        #max player - I think this will always be max player!
        if (game.active_player == self):
            Chosen_Score = -100000
            for m in legal_moves:
                new_game = game.forecast_move(m) #create new board with change
                score = self.minimax_value(new_game, depth-1)
                if score > Chosen_Score:
                    Chosen_Score = score
                    Chosen_Move = m

                #print("max mov", m, " score =", score, "depth=", depth )
                
        #min player ---I dont believe this will ever get called!
        else:
            for m in legal_moves:
                Chosen_Score = 100000
                new_game = game.forecast_move(m) #create new board with change
                score = self.minimax_value(new_game, depth-1)
                #print("min mov", m, " score =", score, "depth=", depth )
                if score < Chosen_Score:
                    Chosen_Score = score
                    Chosen_Move = m
                #print("min mov", m, " score =", score, "depth=", depth )
        
        #print("chosen = ", Chosen_Move )
        
        return Chosen_Move

#=== CLASS::AlphaBetaPlayer =============================================================
class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    myChosen_Score = 0 # integer - Used to pass the score of the chosen move to get_move().
                       # This appeared to be the only way to allow get_move() to break out
                       # of the while loop and still pass the UA tests. Any other solution
                       # breaks the interface of alphabeta() and will fail the tests.

    #=== get_move ===============================================================================
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        #best_move    = (-1, -1)
        first_moves = game.get_legal_moves(game.active_player)
        if not first_moves:
            best_move = (-1, -1)
            best_score   = 0
        else:
            best_move    = first_moves[0]
            best_score   = 1
        
        search_depth = 1
        
        """
        function ITERATIVE-DEEPENING-SEARCH(problem) returns a solution, or failure
            for depth = 0 to inf 
                result <= DEPTH-LIMITED-SEARCH(problem,depth)
                if result != cutoff 
                    return result
        """
        try:
            while( 1 == 1 ):
                best_move = self.alphabeta( game, search_depth, float("-inf"), float("inf") )
                search_depth = search_depth + 1
                if( self.myChosen_Score == float("inf")  ):
                    #print("solution found")
                    return best_move


        except SearchTimeout:
            #print("search timeout- best move is (w/ score)", best_move, best_score )
            return best_move  # Handle any actions required after timeout as needed


        #ORIGINAL: try:
        #    # The try/except block will automatically catch the exception
        #    # raised when the timer is about to expire.
        #    return self.alphabeta( game, self.search_depth, float("-inf"), float("inf") )
        #except SearchTimeout:
        #    pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    #===== pr_tabs =============================================================================
    #Use this for debugging to add tabs based on the depth
    def pr_tabs(self, depth):
        returnval = ""
        tabs = 4 - depth
        if( tabs >= 0):
            if( tabs == 1):
                returnval = "\t"
            elif( tabs == 2):
                returnval = "\t\t"
            elif( tabs == 3):
                returnval = "\t\t\t"
            elif( tabs == 4):
                returnval = "\t\t\t\t"

        return returnval

    #====  alphabeta_value  =====================================================================
    def alphabeta_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0:
            if game.is_loser(self):
                #print( self.pr_tabs(depth), "score=-inf" )
                return float("-inf")
            if game.is_winner(self):
                #print( self.pr_tabs(depth), "score=inf" )
                return float("inf")
            #print( self.pr_tabs(depth), "score=", self.score(game, self) )
            return self.score(game, self)

        legal_moves = game.get_legal_moves(game.active_player)
        if not legal_moves: 
            return self.score(game, self)

        #max player
        if (game.active_player == self):
            final_score = float("-inf")
            for m in legal_moves:
                new_game = game.forecast_move(m) #create new board with change
                score = self.alphabeta_value(new_game, depth-1, alpha, beta)
                if score > final_score:
                    final_score = score
                if final_score >= beta:
                    return final_score
                if final_score > alpha:
                    alpha = final_score

        #min player
        else:
            final_score = float("inf")
            for m in legal_moves:
                new_game = game.forecast_move(m) #create new board with change
                score = self.alphabeta_value(new_game, depth-1, alpha, beta)
                if score < final_score:
                    final_score = score
                if final_score <= alpha:
                    return final_score
                if final_score < beta:
                    beta = final_score

        return final_score
    
    #====  alphabeta  =====================================================================
    # TODO 2: finish this function!
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        int self.myChosen_Score  - Used as a return variable to signal when solution is found.
                                   This was needed because changing the interface will fail the UA tests


        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO 3: finish this function!
        legal_moves = game.get_legal_moves(game.active_player)

        if not legal_moves:
            return (-1, -1)

        #TBD experiment with removing this, it implies not making a move is a legal move???!!!
        if depth == 0: #is this necessary at the root level? shouldn't be...
            return self.score(game, game.active_player)

        #Chosen_Move = (-1,-1)
        Chosen_Move = legal_moves[0]
        #max player
        if (game.active_player == self):
            Chosen_Score = float("-inf")
            for m in legal_moves:
                new_game = game.forecast_move(m) #create new board with change
                score = self.alphabeta_value(new_game, depth-1, alpha, beta)
                if score > Chosen_Score:
                    Chosen_Score = score
                    Chosen_Move = m
                if Chosen_Score >= beta:
                    self.myChosen_Score = Chosen_Score 
                    return Chosen_Move
                if Chosen_Score > alpha:
                    alpha = Chosen_Score

        #min player ---I dont believe this should get called, but I fail i/f test when removed!
        else:
            for m in legal_moves:
                Chosen_Score = float("inf")
                new_game = game.forecast_move(m) #create new board with change
                score = self.alphabeta_value(new_game, depth-1, alpha, beta)
                if score < Chosen_Score:
                    Chosen_Score = score
                    Chosen_Move = m
                if Chosen_Score <= alpha:
                    self.myChosen_Score = Chosen_Score # signal to get_move a solution has found (depth limit...)
                    return Chosen_Move
                if Chosen_Score < beta:
                    beta = Chosen_Score

        self.myChosen_Score = Chosen_Score # signal to get_move that a solution has been found (depth limit...)
        return Chosen_Move

    #====  alphabeta_with_score  ===========================================================
    #====   --This method is not used, but kept for future use 
    #=======================================================================================
    def alphabeta_with_score(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        int score
            The score associated with this move. +inf for a win, -inf for a loss, positive
            integer for anything else

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO 3: finish this function!
        legal_moves = game.get_legal_moves(game.active_player)

        if not legal_moves:
            return float("-inf"), (-1, -1)

        #TBD experiment with removing this, it implies not making a move is a legal move???!!!
        if depth == 0: #is this necessary at the root level? shouldn't be...
            return self.score(game, game.active_player)

        Chosen_Move = (-1,-1)
        #max player
        if (game.active_player == self):
            Chosen_Score = float("-inf")
            for m in legal_moves:
                new_game = game.forecast_move(m) #create new board with change
                score = self.alphabeta_value(new_game, depth-1, alpha, beta)
                if score > Chosen_Score:
                    Chosen_Score = score
                    Chosen_Move = m
                if Chosen_Score >= beta:
                    return Chosen_Move, Chosen_Score
                if Chosen_Score > alpha:
                    alpha = Chosen_Score

        #min player ---I dont believe this should get called, but I fail i/f test when removed!
        else:
            for m in legal_moves:
                Chosen_Score = float("inf")
                new_game = game.forecast_move(m) #create new board with change
                score = self.alphabeta_value(new_game, depth-1, alpha, beta)
                if score < Chosen_Score:
                    Chosen_Score = score
                    Chosen_Move = m
                if Chosen_Score <= alpha:
                    return Chosen_Move, Chosen_Score
                if Chosen_Score < beta:
                    beta = Chosen_Score

        return Chosen_Move, Chosen_Score
