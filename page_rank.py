import sys
import os
import time
import argparse
from progress import Progress
import random


def load_graph(args):
    """Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapling a URL (str) to a list of target URLs (str).
    """
    # Create a graph
    Graph = dict()
    # Iterate through the file line by line
    for line in args.datafile:
        # And split each line into two URLs
        node, target = line.split()
        if node not in Graph:
            Graph[node] = []
            Graph[node].append(target)
        elif node in Graph:
            Graph[node].append(target)
    return Graph



def print_stats(graph):
    """Print number of nodes and edges in the given graph"""
    # Number of nodes
    number_nodes = len(graph)
    # Number of edges
    s = 0
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
    dict_count = dict()
    for i in graph:
        dict_count[i] = 0

    #Repeat the random walker process "args.repeats" times
    for k in range(args.repeats):
        # Choose a random source node in the graph and increase its hit count
        current_node = random.choice(list(graph))
        #Repeat the walker steps "args.steps" time
        for j in range(args.steps):
            # Select randomly a node from the target list of current_node and name it as the new current
            current_node = random.choice(graph[current_node])
            # Increase the hit value of the new current_node
            dict_count[current_node] += 1 / (args.repeats)
            # If the new current_node does not have has no outgoing edges then break the walker steps loop to select a new random node
            if current_node not in graph:
                break
    return dict_count


"""""
if len(graph[random_node_source]) == 0:
    random_node_source = random.choice(list(graph))
    dict_count[random_node_source] += 1 / (args.repeats)
    
    else:
        random_node_source = random.choice(graph[random_node_source])
        dict_count[random_node_source] += 1/(args.repeats)

=============

#Choose a target nodes in the random node's  edges
    for k in range(args.repeats):
        # Choose a random source node in the graph and increase its hit count
        random_node_source = random.choice(list(graph))
        dict_count[random_node_source] += 1 / (args.repeats)
        if len(graph[random_node_source]) != None: #0 or None here
            random_node_source = random.choice(graph[random_node_source])
            dict_count[random_node_source] += 1 / (args.repeats)

    return dict_count
    
"""""






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
    # Initialize the hit count frequency of every node to 0
    dict_count = dict()
    for i in graph:
        dict_count[i] = 1/ (len(graph))




parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")


if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)
    #print(graph)

    #result = '\n'.join(f'{key}: {value}' for key, value in graph.items())
    #print(result)

    print(print_stats(graph))
    #print(list(graph))

    #print(stochastic_page_rank(graph, args))



    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
