class Node:
    """
    Node to be a part of the data structure (tree) used in the multiple AI algorithms that will be implemented.
    These include: Uniform Cost, Greedy Best First, A*
    """

    def __init__(self, parent, depth, cost, board, zero_coords = None, token = None):
        self.parent = parent
        self.children = None
        self.depth = depth
        self.board = board
        self.cost = cost
        self.zero_coords = zero_coords
        self.root_cost = 0
        self.goal_cost = 0
        self.total_cost = 0
        self.token = token

        if self.zero_coords is None:
            #search for 0
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == 0:
                        self.zero_coords = (i, j)
                        
    #overiding less than and equals
    def __lt__(self, node):
        return self.total_cost < node.total_cost

    def __eq__(self, node):
        return (self.board == node.board).all()