from dimension import Dimension
class Assembly:
    def __init__(self, name, stackup):
        self.name = name
        self.stackup = stackup
        self.samples = ()
    def __str__(self):
        return str("Assembly Object Named: " + self.name)
    def set_samples(self, n = Dimension.SAMPLE_COUNT):
        samples = []
        for dim in self.stackup:
            dim.set_sample(n=n)
            samples.append(dim.get_sample())
        self.samples = [sum(x) for x in zip(*samples)]
        self.samples = tuple(self.samples)
    def get_sample(self):
        return self.samples
    def get_nominal(self):
        nom = 0
        for dim in self.stackup:
            nom += dim.dim
        return nom
    def check(self, lower, upper):
        over = []
        under = []
        correct = []
        for i in self.get_sample():
            if i < lower:
                under.append(i)
            elif i > upper:
                over.append(i)
            else:
                correct.append(i)
        n = len(self.get_sample())
        print("Pass %: ",(len(correct)/n))
        print("Undersized %: ",(len(under)/n))
        print("Oversized %: ",(len(over)/n))
        return (correct, under, over)
