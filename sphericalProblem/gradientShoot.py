import numpy as np

def gradient_descent_satellites_repartition(problem, eps, max_iter, verbose = False):
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
    
    def first_derivative(index, alpha, h, grad):
            old_position = np.copy(problem.satellites_position[index])
            problem.satellites_position[index] += (alpha + h)* grad
            power_plus_h = problem.total_received_power(continuous = True)
            problem.satellites_position[index] -= 2*h*grad
            power_minus_h = problem.total_received_power(continuous = True)
            problem.satellites_position[index] = old_position
            return (power_plus_h - power_minus_h) / (2*h)
    
    def optimal_alpha(index, grad, eps):
        sign = np.sign(first_derivative(index, 0, 1e-6, grad))
        alpha_a = 0
        alpha_b = 0
        while(sign == np.sign(first_derivative(index, alpha_b, 1e-6, grad))):
            alpha_b += 0.1*sign
        if sign == -1:
            a = alpha_a
            alpha_a = alpha_b
            alpha_b = a
        while(True):
            alpha = (alpha_a + alpha_b) / 2
            if first_derivative(index, alpha, 1e-6, grad) > 0:
                alpha_a = alpha
            else:
                alpha_b = alpha
            if abs(alpha_b - alpha_a) < eps:
                break
        return alpha

    for i in range(len(problem.satellites_position)):
        n_iter = 0
        if verbose:
            print("Initial position of the satellite: {}, total received power: {}".format(problem.satellites_position[i], problem.total_received_power(continuous = True)))
        while True:
            grad = approx_grad(i, h=1e-6)
            if np.linalg.norm(grad) < eps or n_iter >= max_iter:
                break
            grad /= np.linalg.norm(grad)
            alpha = optimal_alpha(i, grad, eps)
            problem.satellites_position[i] += alpha * grad/np.linalg.norm(grad)
            n_iter += 1
        if verbose:
            print("End position of the satellite: {}, total received power: {}, number of iterations: {}\n".format(problem.satellites_position[i], problem.total_received_power(continuous = True), n_iter))
    problem.method = "gradient descent"
    return problem