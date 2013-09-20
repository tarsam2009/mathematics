# mathematics

The mathematics package contains many useful packages I built to help in my own curious projects.

## Packages

* graph
* coverings
* combinatorics

## Graphs

The graphs package has many important sub-modules: most important being the graph module which contains the Graph class. All proper methods of this package expect graphs to be represented with the mathematics.graphs.graph.Graph class.

## Coverings

In tribute to Erdos, there is a coverings package, which helps organize a covering system of the integers into a single class. For personal enjoyment, if pyglet is available in the environment, then interactive.coverings.InteractiveCovering( moduli, lcm, [resiudes] ) class should be experimented with. It displays coverings as a puzzle game. Use the up and down arrows to choose a modulus to work with, and use the left and right arrows to change the residue. The top row displays how well a residue class of the LCM is covered: the darker a square is, the more the class is covered. You have a covering when the top row has no white squares! Press Escape to exit the game.

## Combinatorics

Provides helper functions for many combinatorial tasks such as combinations and transforming an integer polynomial into a polynomial with binomial coefficients.
