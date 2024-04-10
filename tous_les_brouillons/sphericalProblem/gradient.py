import numpy as np

def gradient_descent_satellites_repartition(problem, eps=1e-6, max_iter=100):
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

    def optimal_alpha(index, grad, eps=1e-6, h=1e-6):
        old_position = np.copy(problem.satellites_position[index])
        def first_derivative(alpha):
            problem.satellites_position[index] += (alpha + h)* grad
            power_plus_h = problem.total_received_power(continuous = True)
            problem.satellites_position[index] -= 2*h*grad
            power_minus_h = problem.total_received_power(continuous = True)
            problem.satellites_position[index] = old_position
            return (power_plus_h - power_minus_h) / (2*h)
        
        def second_derivative(alpha):
            problem.satellites_position[index] += alpha * grad
            power = problem.total_received_power(continuous = True)
            problem.satellites_position[index] += h * grad
            power_plus_h = problem.total_received_power(continuous = True)
            problem.satellites_position[index] -= 2*h*grad
            power_minus_h = problem.total_received_power(continuous = True)
            problem.satellites_position[index] = old_position
            return (power_plus_h - 2*power + power_minus_h) / h**2
        
        alpha_init = 0
        while(True):
            print("alpha: {}, first_derivative: {}, second_derivative: {}".format(alpha_init, first_derivative(alpha_init), second_derivative(alpha_init)))
            alpha = alpha_init - first_derivative(alpha_init) / second_derivative(alpha_init)
            if abs(alpha - alpha_init) < eps:
                break
            alpha_init = alpha
        return alpha


    for i in range(len(problem.satellites_position)):
        n_iter = 0
        print("Init norm of the gradient: {}, total received power: {}".format(np.linalg.norm(approx_grad(i)), problem.total_received_power(continuous = True)))
        while True:
            grad = approx_grad(i)
            alpha = optimal_alpha(i, grad)
            problem.satellites_position[i] += alpha * grad
            n_iter += 1
            if np.linalg.norm(grad) < eps or n_iter > max_iter:
                break
        print("End norm of the gradient: {}, total received power: {}, number of iterations: {}".format(np.linalg.norm(approx_grad(i)), problem.total_received_power(continuous = True), n_iter))
    problem.method = "gradient descent"
    return problem