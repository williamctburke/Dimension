import numpy as np

class Dim:
    num = 100000  # Class variable, controls # of samples in monte carlo
    def __init__(self, name, dim, tol, sigma=3, dist = "normal", shift = 0):
        # basic attributes
        self.name = name
        self.dim = dim
        self.tol = tol
        self.sigma = sigma
        self.stddev = self.tol / self.sigma
        self.dist = "normal"
        self.shift = shift
    def __str__(self):
        return str("Dimension Object Named: " + self.name)
    def set_sample(self,n=num):
        sampler = {
            "normal":np.random.normal
            }
        func = sampler.get(self.dist)
        s = func(self.dim, self.stddev, n)
        self.s = tuple(s)
        self.shifted = [e + self.shift*self.sigma for e in self.s]
    def set_shift(self, shift=1.5):
        self.shift = shift
        self.set_sample()
    def get_sample(self):
        return self.s
    def get_shifted(self):
        return self.shifted

class Assy:
    pass

class Prod:
    pass
