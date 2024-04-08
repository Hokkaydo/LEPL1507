import numpy as np

def stupid_spherical_satellites_repartition(problem):    
    """A stupid algorithm to solve the problem of finding the best position for N satellites"""
    for i in range(problem.N_satellites):
        problem.satellites_position[i] = [np.random.uniform(0, 2*np.pi), np.random.uniform(0, np.pi)]
    problem.method = "stupid"
    return problem