**CSC1034 Assessment 3**
========================

*Overview*
========

The aim of this project is to simulate how Google's PageRank works.
To do so:

**page_rank.py** : In this python file, I have implemented four functions:

- load_graph: This function retrieve data from the "args.datafile" file and load its data in a direct graph as 
a dictionary object with lists as items to represent the relations between nodes.

- print_stats: Print number of nodes and edges in the given graph dictionary.

- stochastic_page_rank: This function simulates Page Rank through random walkers. Here, after a random walk 
of "args.steps" steps, the hit count of the last page of the random walk will increase. We will repeat 
"args.repeats" times the random walk process until the rank of every single pages converges (does not change 
significantly between repetition n and repetition n+1).

- distribution_page_rank: This function simulates Page Rank through probability distributions. For this function we use
uniform probability to estimate the PageRank of a page. The PageRank probabilities are iterated "args.steps" times. 
The more iterations, the more precise pages' PageRank will be.

**The PageRank functions are adapted from the given pseudocodes.**

Through the boilerplate code in the "__main__", the top "args.number" ranked pages will appear in the terminal.
The "argparse" library is used in this assessment and has been implemented with its different options.

**school_website.txt** : This file contains information about links among web pages of the School of Computing website.
It is this file we have retrieved data from to exploit them as wanted.

**progress.py** : The module progress.py provides a command line progress bar. However, I didn't use it.



*Code optimization*
===================

After having implemented both algorithms, I tried to improve my solutions with the aim to increase execution speed. 
I use time module to measure code execution times.

**load_graph function:**
--------------------------------

For this function, the optimization consisted in storing constant functions in local variables :

~~~~
 # Store constants in local variables
    file = args.datafile
~~~~

------------------------------------------------------------------------------------------------

**PageRank function through random walkers :**
-------------------------------------------------

**Before code optimization:**

    def stochastic_page_rank(graph, args):
        
        Stochastic PageRank estimation
        Parameters:
        graph -- a graph object as returned by load_graph()
        args -- arguments named tuple

        Returns:
        A dict that assigns each page its hit frequency

        This function estimates the Page Rank by counting how frequently
        a random walk that starts on a random node will after n_steps end
        on each node of the given graph.

    
    # Initialize the hit count frequency of every node to 0
    dict_count = dict()
    for i in graph:
        dict_count[i] = 0

    # Repeat the random walker process "args.repeats" times
    for k in range(args.repeats):
        # Choose a random source node in the graph and increase its hit count
        current_node = random.choice(list(graph))
        # Do a random walk of "args.steps" steps
        for j in range(args.steps):
            # Select randomly a node from the target list of current_node and name it as the new current
            current_node = random.choice(graph[current_node])
            # If the new current_node does not have has no outgoing edges then break the walker steps loop to select a new random node
            if current_node not in graph:
                break
        # Increase the hit value of the finale node reached from the random walk
        dict_count[current_node] += 1 / (args.repeats)

    return dict_count

**_Time execution before optimization: 52.16 seconds_**


**Code optimization:**

To optimize performance:

- I have avoided attribute lookups by only importing the function choice from random and the function time from time
and storing constant functions in local variables :
~~~~
from random import choice
from time import time

n_repetitions = args.repeats
n_steps = args.steps
~~~~

Each time we call a function from a module, the python interpreter has to search at each loop the function in the module.
If the number of repetitions is high the time lost can be significant. So if we avoid these lookups we gain a lot of time.

**Time after this alteration: 49.08 seconds, we gained 5% on the former time**

- I replaced some loops by dict comprehensions where possible, loops are relatively slow compared to dict comprehensions:
~~~~
# Initialize the hit count frequency of every node to 0
    # Use dict comprehension for optimization
    dict_count = {i: 0 for i in graph}
~~~~

**Time after this alteration: 47.76 seconds, we gained 8.46% on the former time**


------------------------------------------------------------------------------------------------

**PageRank function through probability distributions before code optimization:**
---------------------------------------------------------------------------------

**Before code optimization:**

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
    # Initialize each node probability to 1/(number of nodes)
    node_prob = dict()
    for node in graph:
        node_prob[node] = 1/ (len(graph))

    # Repeat iterations "args.steps" times
    for i in range(args.steps):

        #Initialize the next_prob of each node to 0
        next_prob = dict()
        for node in graph:
            next_prob[node] = 0

        for node in graph:
            p = node_prob[node] /(len(graph[node]))
            for target in graph[node]:
                next_prob[target] += p

        for node in next_prob:
            node_prob[node] = next_prob[node]

    return node_prob

**_Time execution before optimization: 0.13 seconds_**


**Code optimization:**

To optimize performance:

- As well as stochastic_page_rank, I have avoided attribute lookups in distribution_page_rank by only importing the 
function time from time and storing constant functions in local variables :
~~~~
from time import time

n_steps = args.steps
number_nodes = len(graph)
~~~~

**Time execution after alterations: 0.13 seconds**
 
- I replaced some loops by dict comprehensions where possible:
~~~~
# Initialize each node probability to 1/(number of nodes)
    # Use dict comprehension for optimization
    node_prob = {node: 1/number_nodes for node in graph}

# Initialize the next_prob of each node to 0
        next_prob = {node: 0 for node in graph}
~~~~

**Time execution after alterations: 0.13 seconds. After all the alterations the time for this function is still the same**

In my opinion because the former time was already very fast (0.13 seconds), the time gained through the alterations made 
to the function was negligible. 

Proofs of both functions' time execution screenshots are in the S220642259 main folder.


PANAMBALOM Soraya
-----------------