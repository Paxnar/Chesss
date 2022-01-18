class Paxnar:
    def __init__(self, o):
        self.o = o


pow = Paxnar('s')
shoo = Paxnar('g')
print(pow is Paxnar)
print(pow is not None)
print(type(shoo) == Paxnar)
print(pow is shoo)