# solveMatrixGame
Python solver for two-player zero-sum games.

## Solution

Consider a two-player zero-sum game and let $M$ be its $m \times n$ matrix game. The row's player problem is to compute the row value $v$ and an optimal mixed strategy $p = (p_1, ..., p_m)$ such that $v$ is as large as possible and 

$$ v = min_{j} \sum_{i=1}^{m} p_i m_{ij}. $$

We can rephrase it in an equivalent way that is a linear programming problem. That is: find $p$ and $v$ such that $v$ is as large as possible, subject to the following conditions:

$$
\begin{align}
(1) \quad & p_i \geq 0 \quad \text{for } 1 \leq i \leq m. \\
(2) \quad & \sum_{i=1}^{m} p_i = 1. \\
(3) \quad & v \leq \sum_{i=1}^{m} p_i m_{ij} \quad \text{for } 1 \leq j \leq n.
\end{align}
$$

We can assume that all entries of $M$ are positive. It can be shown that in such case $v > 0$. Otherwise, we add a constant $c$ to every entry of $M$ such that $m_{ij} + c > 0$, which results in adding the same value to $v$.

We can now make the following change of variables:

$$ y_i = p_i/v \quad \text{for } 1 \leq i \leq m. $$

Then, condition (2) implies that:

$$ \frac{1}{v} = \sum_{i=1}^{m} y_i. $$

And condition (3):

$$ \sum_{i=1}^{m} m_{ij}y_i \geq 1 \quad \text{for } 1 \leq j \leq n. $$

And since maximizing $v$ is equivalent to minimizing $1/v$, we arrive at the formulation of a dual linear programming problem:

$$
\begin{align*}
\text{minimize} \quad & y_1 + \dots + y_m \\
\text{subject to} \quad & \sum_{i=1}^{m} m_{ij}y_i \geq 1, \quad \text{for } 1 \leq j \leq n.
\end{align*}
$$
