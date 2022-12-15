import sys
import os
import argparse

#Import the needed functions from the modules
from random import choice
from time import time



def load_graph(args):
    """Load graph from text file
    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapling a URL (str) to a list of target URLs (str).
    """
    # Create a graph
    graph = dict()
    # Store constants in local variables
    file = args.datafile

    # Iterate through the file line by line>W
    for line in file:
        # And split each line into two URLs
        node, target = line.split()
        if node not in graph:
            graph[node] = []
            graph[node].append(target)
        elif node in graph:
            graph[node].append(target)
    return graph


def print_stats(graph):
    """Print number of nodes and edges in the given graph"""
    # Number of nodes
    number_nodes = len(graph)
    # Number of edges
    count = 0
    for i in graph:
        count += len(graph[i])
    return f'The number of nodes is {number_nodes} and the number of edges is {count}'


def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """
    # Initialize the hit count frequency of every node to 0
    # Use dict comprehension for optimization
    dict_count = {i: 0 for i in graph}

    # Store constants in local variables
    n_repetitions = args.repeats
    n_steps = args.steps

    # Repeat the random walker process "args.repeats" times
    for k in range(n_repetitions):
        # Choose a random source node in the graph and increase its hit count
        current_node = choice(list(graph))
        # Do a random walk of "args.steps" steps
        for j in range(n_steps):
            # Select randomly a node from the target list of current_node and name it as the new current
            current_node = choice(graph[current_node])
            # If the new current_node does not have has no outgoing edges then break the walker steps loop to select
            # a new random node
            if current_node not in graph:
                break
        # Increase the hit value of the finale node reached from the random walk
        dict_count[current_node] += 1 / n_repetitions

    return dict_count



def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    # Store constants in local variables
    n_steps = args.steps
    number_nodes = len(graph)

    # Initialize each node probability to 1/(number of nodes)
    # Use dict comprehension for optimization
    node_prob = {node: 1/number_nodes for node in graph}

    # Repeat iterations "args.steps" times
    for i in range(n_steps):

        # Initialize the next_prob of each node to 0
        next_prob = {node: 0 for node in graph}

        for node in graph:
            # Store constant number in  variable
            number_target = len(graph[node])
            p = node_prob[node] / number_target
            for target in graph[node]:
                next_prob[target] += p
        node_prob = next_prob

    return node_prob


# Implementations of argparse command line arguments
parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")


if __name__ == '__main__':

    # Instantiate the parser
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time()
    ranking = algorithm(graph, args)
    stop = time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
