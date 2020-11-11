class Node:
    """
    Node to be a part of the data structure (tree) used in the multiple AI algorithms that will be implemented.
    These include: Uniform Cost, Greedy Best First, A*
    """

    def __init__(self, parent, depth, cost, board, zero_coords=None):
        self.parent = parent
        self.children = None
        self.depth = depth
        self.board = board
        self.cost = cost
        self.zero_coords = zero_coords
        self.root_cost = 0
        self.goal_cost = 0

        if self.zero_coords is None:
            #search for 0
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == 0:
                        self.zero_coords = (i, j)
                        
    #overiding 
    def __lt__(self, node):
        return self.getTotalCost() < node.getTotalCost()

    def __eq__(self, node):
        return (self.board == node.board).all()


    def getTotalCost(self):
        return self.root_cost + self.goal_cost