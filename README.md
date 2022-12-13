CSC1034 Assessement 3



Overview

The aim of this project is to simulate how Google's PageRank works.
To do so:

**page_rank.py** : In this python file, I have implemented four functions:
- load_graph: This function retrieve data from the "args.datafile" file and load thel in a direct graph as a dictionnary object
to represent the relations between newcastle university website's pages.
The initial node is placed as the key in the dictionnary and its targets node are placed in a list as the item.
- print_stats: Print number of nodes and edges in the given graph dictioannary.
- stochastic_page_rank: 