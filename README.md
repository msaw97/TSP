# TSP
My work on Travelling Salesman Problem and its approximation algorithms.

# Usage
 Main block solves randomly generated TSP instance with reference to provided CLI arguments
#### main.py N [-h] [-b] [-nn] [-ci] [-rnn] [-hk] [-EDM] [-eps EPS] 
- obligatory argument N sets number the of vertices of a graph;
- -b solves generated TSP instance with brute force algorithm;
- -nn solves generated TSP instance with nearest neighbor algorithm;
- -ci solves generated TSP instance with cheapest insertion algorithm;
- -rnn solves generated TSP instance with repetitive nearest neighbor algorithm;
- -hk solves generated TSP instance with accurate Held-Karp algorithm;
- -EDM sets generated graph edges to satisfy the triangular inequality;
- -eps sets some given scalar EPS which multiplies all of the graph edges weights.

# Other included files
#### - time_experiment.py analyzes time it takes to compute each of the implemented algorithms;
#### - error_experiment.py analyzes relative error of approximation algorithms; 
#### - test_algorithms.py contains unit tests for algorithms.py module.

# Time and error analysis results

![](/images/time_alg(10_350_140_350_17)_iter(35)_EDM(False).png)

![](/images/time_alg(10_350_140_350_17)_iter(35)_EDM(True).png)

![](/images/error_maxN(20)_iter(35)_EDM(False).png)

![](/images/error_maxN(20)_iter(35)_EDM(True).png)

