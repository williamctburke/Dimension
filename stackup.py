from dimension import Dimension
class Stackup:
    def __init__(self, name, stackup, lower, upper):
        self.name = name
        self.stackup = stackup
        self.min = lower
        self.max = upper
    def __str__(self):
        return str("Assembly Object Named: " + self.name)
    def set_samples(self, n = Dimension.SAMPLE_COUNT):
        samples = []
        for dim in self.stackup:
            dim.set_sample(n=n)
    def get_stackup_sample(self):
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
    def test(self):
        samples = self.get_stackup_sample()
        over = []
        under = []
        correct = []
        results = [False]*len(samples)
        for i in range(0, len(samples)):
            sample = samples[i]
            if sample < self.min:
                under.append(sample)
            elif sample > self.max:
                over.append(sample)
            else:
                correct.append(sample)
                results[i] = True
        return (results, correct, under, over)
