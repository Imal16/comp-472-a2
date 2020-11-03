from node import Node

def run():
    root = Node(None, 0, [3,0,1,4,2,6,5,7])     #numbers taken from the first sample puzzle

    print(root.__doc__)
    print(root.__dict__)



if __name__ == "__main__":
    run()