from cost_function import *
from utilities import *

class Fletcher_Reeves :
    def __init__(self, f, grad, x0) :
        self.f = f
        self.grad = grad
        self.x = cart2spher(x0)
        self.p = grad(self.x)
    
    def maximize(self) :
        new_x = self.x + alpha*self.p
        self.p = -self.grad(new_x)