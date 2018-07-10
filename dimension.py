import numpy as np

class Dimension:
    SAMPLE_COUNT = 100000  # Class variable, controls # of samples in monte carlo
    instances = []
    def __init__(self, name, dim, tol, sigma=3, dist = "normal", shift = 0):
        # basic attributes
        self.name = name
        self.dim = dim
        self.tol = tol
        self.sigma = sigma
        self.stddev = self.tol / self.sigma
        self.dist = "normal"
        self.shift = shift
        Dimension.instances.append(self)
    def __str__(self):
        return str("Dimension Object Named: " + self.name)
    @staticmethod
    def set_all_samples(n=SAMPLE_COUNT):
        Dimension.SAMPLE_COUNT = n
        for instance in Dimension.instances:
            instance.set_sample(n=n)
    def set_sample(self,n=SAMPLE_COUNT):
        Dimension.SAMPLE_COUNT = n
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
