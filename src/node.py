class Node:
    """
    Node to be a part of the data structure (tree) used in the multiple AI algorithms that will be implemented.
    These include: Uniform Cost, Greedy Best First, A*
    """

    def __init__(self, parent, depth, board):
        self.parent = parent
        self.children = None
        self.depth = depth
        self.board = board