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
    def get_assy_sample(self):
        samples = []
        for dim in self.stackup:
            samples.append(dim.get_sample())
        samples = [sum(x) for x in zip(*samples)]
        samples = tuple(samples)
        return samples
    def get_nominal(self):
        nom = 0
        for dim in self.stackup:
            nom += dim.dim
        return nom
    def check(self, lower, upper):
        over = []
        under = []
        correct = []
        for i in self.get_assy_sample():
            if i < lower:
                under.append(i)
            elif i > upper:
                over.append(i)
            else:
                correct.append(i)
        n = len(correct) + len(under) + len(over)
        print("Pass %: ",(len(correct)/n))
        print("Undersized %: ",(len(under)/n))
        print("Oversized %: ",(len(over)/n))
        return (correct, under, over)
