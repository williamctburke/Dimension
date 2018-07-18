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
        if self.tol != None: # When fitting data self.tol is populated at a later time
            self.stddev = self.tol / self.sigma
        if dist == None:
            dist = "normal"
        self.dist = dist
        if shift == None:
            shift = 0
        self.shift = shift
    def __str__(self):
        return str("Dimension Object Named: " + self.name)
    def set_dist_func(self, dist_func, params):
        self.dist_func = dist_func
        self.params = params
    def set_sample(self,samples):
        self.s = tuple(samples)
    def get_sample(self):
        return self.s
    def get_noshift_sample(self):
        return [e - self.shift*self.sigma for e in self.s]
