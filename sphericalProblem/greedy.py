import numpy as np

def greedy_spherical_satellites_repartition(problem, n_iter = 100):
    """A greedy algorithm to solve the problem of finding the best position for N satellites"""
    N_satellites = problem.N_satellites
    problem.N_satellites = 0
    problem.satellites_position = []
    for i in range(N_satellites):
        problem.N_satellites += 1
        problem.satellites_position.append([0, 0])
        best_coverage = problem.coverage()
        best_position = [0, 0]
        for phi in np.linspace(0, 2*np.pi, n_iter):
            for theta in np.linspace(0, np.pi, n_iter):
                problem.satellites_position[i] = [phi, theta]
                if problem.coverage() > best_coverage:
                    best_coverage = problem.coverage()
                    best_position = [phi, theta]
        problem.satellites_position[i] = best_position
    problem.method = "greedy"
    return problem