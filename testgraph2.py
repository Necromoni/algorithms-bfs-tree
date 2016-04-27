import graphviz as gv

class TestGraph:
    def __init__(self):
        g1 = gv.Graph(format='svg')
        g1.node('A')
        g1.node('B')
        g1.edge('A', 'B')
        f = open('file.dot', 'w')
        f.write(g1.source)
        f.close()

tg = TestGraph()

