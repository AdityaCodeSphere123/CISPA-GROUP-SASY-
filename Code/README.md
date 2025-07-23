
# Code Directory Overview

This directory contains several Python scripts, each with a specific purpose related to graph algorithms, queue analysis, and plotting. Here is a summary of each file:

## 1.py (formerly compact.py)
- Contains a function to determine the smallest `n` such that after `k` compactions, all vertices are seen (within a small epsilon).
- Returns the required `n`, final queue size, number of compactions, and convergence status for given parameters.
- Useful for theoretical queue/compaction analysis in graph algorithms.

## 2.py (formerly count.py)
- Plots mathematical expressions related to queue size and graph parameters for various values of `d`.
- Produces both individual and combined plots for different `d` values.
- Useful for visualizing how queue size and related expressions change with graph parameters.

## 3.py (formerly final.py)
- Implements a full graph algorithm with a class `GraphAlgorithm`.
- Handles adjacency matrix creation, queue processing, compaction, and tracks statistics like max queue size and real queue size.
- Includes a function to generate large, well-connected test graphs.
- Runs both a small and a large test case, printing detailed statistics and progress.

## 4.py (formerly main.py)
- Contains a variant of the graph algorithm with a focus on adjacency matrix construction and queue processing.
- Runs a sample test case and prints the adjacency matrix and algorithm progress.
- Useful for debugging and understanding the step-by-step operation of the algorithm.

## 5.py (formerly new.py)
- Contains pseudocode (not executable Python) for oblivious BFS and d-normalized graph representation, suitable for secure computation/TEE settings.
- Includes functions for oblivious queue and array operations, and OKVS-based adjacency list access.
- Useful as a reference for implementing oblivious graph algorithms.

## 6.py (formerly plot.py)
- Provides a 3D plotting tool for the expression `x = v[1-(1-(a/v)^(y-1))] - yn` over ranges of `y` and `n`.
- Asks for user input for `v` and `e`, computes derived parameters, and visualizes the result as a surface plot.
- Prints the minimum value and statistics for the computed surface.
- Useful for visualizing and analyzing the behavior of the compaction/cost function.

## 7.py (formerly prob.py)
- Analyzes and plots the cost function and minimum delta for various `d` and `n` values.
- Prints a table of results and produces both individual and combined plots.
- Useful for understanding the trade-offs in parameter selection for graph/queue algorithms.

---

**Note:**
- All scripts are self-contained and can be run independently (except 5.py, which is pseudocode/reference).
- For plotting scripts, ensure you have `matplotlib` and `numpy` installed.
- For large graph tests, scripts may take time and use significant memory.