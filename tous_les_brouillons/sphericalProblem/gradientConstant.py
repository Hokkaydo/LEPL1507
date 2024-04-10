import numpy as np

def gradient_descent_satellites_repartition(problem, alpha, eps, max_iter):
    def approx_grad(index, h=1e-6):
        grad = np.zeros(2)
        old_position = np.copy(problem.satellites_position[index])
        for i in range(2):
            problem.satellites_position[index][i] += h
            power_plus_h = problem.total_received_power(continuous = True)
            problem.satellites_position[index][i] -= 2*h
            power_minus_h = problem.total_received_power(continuous = True)
            grad[i] = (power_plus_h - power_minus_h) / (2*h)
            problem.satellites_position[index] = old_position
        return grad

    for i in range(len(problem.satellites_position)):
        n_iter = 0
        print("Init norm of the gradient: {}, total received power: {}".format(np.linalg.norm(approx_grad(i)), problem.total_received_power(continuous = True)))
        while True:
            grad = approx_grad(i, h=1e-6)
            if np.linalg.norm(grad) < eps or n_iter >= max_iter:
                break
            problem.satellites_position[i] += alpha * grad/np.linalg.norm(grad)
            n_iter += 1
        print("End norm of the gradient: {}, total received power: {}, number of iterations: {}".format(np.linalg.norm(approx_grad(i)), problem.total_received_power(continuous = True), n_iter))
    problem.method = "gradient descent"
    return problem