import numpy as np

class Dimension:
    sample_count = 100000
    def __init__(self, name, dim, tol, sigma=3, dist = "normal", shift = 0):
        # basic attributes
        self.name = name
        self.dim = dim
        self.tol = tol
        if sigma == None:
            sigma = 3
        self.sigma = sigma
        self.stddev = self.tol / self.sigma
        if dist == None:
            dist = "normal"
        self.dist = dist
        if shift == None:
            shift = 0
        self.shift = shift
    def __str__(self):
        return str("Dimension Object Named: " + self.name)
    def set_sample(self,n):
        Dimension.sample_count = n
        sampler_dict = {
            "normal":np.random.normal
            }
        sampler = sampler_dict.get(self.dist)
        s = sampler(self.dim, self.stddev, n)
        self.s = tuple(s)
        self.shifted = [e + self.shift*self.sigma for e in self.s]
    def set_shift(self, shift=1.5):
        self.shift = shift
        self.set_sample()
    def get_sample(self):
        return self.shifted
    def get_true_sample(self):
        return self.s
