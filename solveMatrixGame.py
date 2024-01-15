import numpy as np
import random


class solveMatrixGame:
    def __init__(self, matrix, c=0, print_pivots=False):
        self.c = c
        self.matrix = matrix.astype(float) + c
        dimensions = matrix.shape
        self.m = dimensions[0]
        self.n = dimensions[1]

        self.print_pivots = print_pivots

        ## Create tableau
        self.tableau = np.column_stack(
            (np.row_stack((self.matrix, np.ones(self.n))), np.ones(self.m + 1))
        )
        self.tableau[self.m, self.n] = 0

        ## Create basic and non-basic variables to print solution
        self.dual_nonbasic_vars = [f"y_{i}" for i in range(1, self.m + 1)]
        self.dual_basic_vars = [
            f"y_{i}" for i in range(self.m + 1, self.m + self.n + 1)
        ]

        self.primal_nonbasic_vars = [f"x_{j}" for j in range(1, self.n + 1)]
        self.primal_basic_vars = [
            f"x_{j}" for j in range(self.n + 1, self.m + self.n + 1)
        ]

    def is_tableau_feasible(self):
        ## Check if all the basic variables are nonnegative.
        return all(self.tableau[i, -1] >= 0 for i in range(self.m))

    def is_tableau_unbounded(self):
        ## Check if there is any column with a positive value in the last row
        ## and nonpositive values in the other rows.
        for j in range(self.n):
            if self.tableau[-1, j] > 0:
                if all(self.tableau[i, j] <= 0 for i in range(self.m)):
                    return True
        return False

    def is_tableau_optimal(self):
        return all(self.tableau[-1, j] <= 0 for j in range(self.n))

    def pivoting_algorithm(self, pivot):
        ## Pivot on t_k_l
        k = pivot[0]
        l = pivot[1]

        for i in range(self.m + 1):
            if i == k:
                continue
            for j in range(self.n + 1):
                if j == l:
                    continue
                self.tableau[i, j] = (
                    self.tableau[i, j] * self.tableau[k, l]
                    - self.tableau[i, l] * self.tableau[k, j]
                ) / self.tableau[k, l]

        for i in range(self.m + 1):
            if i != k:
                self.tableau[i, l] = -self.tableau[i, l] / self.tableau[k, l]

        for j in range(self.n + 1):
            if j != l:
                self.tableau[k, j] = self.tableau[k, j] / self.tableau[k, l]

        self.tableau[k, l] = 1 / self.tableau[k, l]

    def choose_pivot(self):
        ## Choose randomly one of the nonbasic variables with a
        ## positive coefficient in the objective function
        pos_cols = [j for j in range(self.n) if self.tableau[-1, j] > 0]
        l = random.choice(pos_cols)
        k = 0
        min_value = 100000
        for i in range(self.m):
            if self.tableau[i, l] > 0:
                val = self.tableau[i, -1] / self.tableau[i, l]
                if val < min_value:
                    min_value = val
                    k = i
        return [k, l]

    def pivot_variables(self, pivot):
        ## Pivot on t_k_l
        k = pivot[0]
        l = pivot[1]

        ## Update dual variables
        temp = self.dual_nonbasic_vars[k]
        self.dual_nonbasic_vars[k] = self.dual_basic_vars[l]
        self.dual_basic_vars[l] = temp

        ## Update primal variables
        temp = self.primal_nonbasic_vars[l]
        self.primal_nonbasic_vars[l] = self.primal_basic_vars[k]
        self.primal_basic_vars[k] = temp

    def run(self):
        iter = 0
        if self.is_tableau_feasible():
            while not self.is_tableau_optimal():
                iter += 1
                if self.is_tableau_unbounded():
                    print("Tableau is unbounded")
                    break
                else:
                    pivot = self.choose_pivot()
                    self.pivot_variables(pivot)
                    self.pivoting_algorithm(pivot)
                    if self.print_pivots:
                        print("Pivot: ", pivot)
                        print("Iteration: ", iter)
                        print(self.primal_basic_vars)
                        print(self.primal_nonbasic_vars)
                        print(self.tableau)
        else:
            print("Tableau is unfeasible")

    def print_row_player(self):
        val = -1 / self.tableau[-1, -1]
        print("Row value: ", val + self.c)
        for i in range(1, self.m + 1):
            if f"y_{i}" in self.dual_basic_vars:
                print(
                    f"p_{i} = ",
                    -val * self.tableau[-1, self.dual_basic_vars.index(f"y_{i}")],
                )
            else:
                print(f"p_{i} = 0.0")

    def print_column_player(self):
        val = -1 / self.tableau[-1, -1]
        print("Column value: ", val + self.c)
        for i in range(1, self.n + 1):
            if f"x_{i}" in self.primal_basic_vars:
                print(
                    f"q_{i} = ",
                    val * self.tableau[self.primal_basic_vars.index(f"x_{i}"), -1],
                )
            else:
                print(f"q_{i} = 0.0")


def main():
    matrix = np.matrix(
        [
            [40, 70, 10],
            [10, 40, 70],
            [70, 10, 40],
            [20, 50, 50],
            [60, 30, 30],
            [30, 60, 30],
            [50, 20, 50],
            [50, 50, 20],
            [30, 30, 60],
            [40, 40, 40],
        ]
    )

    simplex = solveMatrixGame(matrix, print_pivots=True)
    simplex.run()
    simplex.print_row_player()


if __name__ == "__main__":
    main()