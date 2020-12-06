import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys

G, s = read_input_file('/Users/sreevidyaganga/Desktop/project-fa20-skeleton-master/inputs/small-1.in')
# print(G[2][0]['stress'])
print(G.degree[0])


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    # TODO: your code here!
    pass
    

def greedy(G, s):
    sorted_happiness = [G[x][y] for ] 
    for i in range(len(G.nodes)):
        stress = s/i

def kcluster(G, s):
    i = 1
    best = {}
    while i < len(G.nodes):
        result = {}
        for j in range(i):
            result[j] = []
        cc = 0

        budget = s/i
        
        i += 1


def clearGraph(G, s):
    edges = list(G.edges)
    i = 0
    while i < len(edges):
        element = edges[i]
        if (element['stress'] > s):
            del element


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
