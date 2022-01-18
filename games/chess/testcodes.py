class Paxnar:
    def __init__(self, o):
        self.o = o


pow = Paxnar('s')
shoo = Paxnar('g')
s = [Paxnar('sfg'), Paxnar('dg')]
print(pow in s)
