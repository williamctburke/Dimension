from assembly import Assembly
class Product:
    def __init__(self, name, parts):
        self.name = name
        self.parts = parts
        self.samples = ()
    def __str__(self):
        return str("Assembly Object Named: " + self.name)
