from stackup import Stackup
from dimension import Dimension
class Part:
    def __init__(self, name, stackups):
        self.name = name
        self.stackups = stackups
    def __str__(self):
        return str("Assembly Object Named: " + self.name)
    def test(self):
        results = [True]*Dimension.sample_count
        for stackup in self.stackups:
            test,_,_,_ = stackup.test()
            results = [a and b for a, b in zip(results, test)]
        return results

            
