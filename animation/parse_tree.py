import textwrap
from graphviz import Digraph, nohtml, Source

# generate dot source code
#define a class to represent each nodes
class Node(object):
    def __init__(self,n,value,leaf=False):
        self.n = n
        self.value = value
        self.leaf = leaf
    def __repr__(self):
        return str(self.value)+str(self.n)
    def isLeaf(self):
        return self.leaf

class Graph(object):
    def __init__(self,tree):
        self.tree = tree
        self.dot_header = [textwrap.dedent("""
                            digraph {
                            node [shape=circle, fontsize=12, fontname="Courier", height=.1];
                            ranksep=.3;
                            edge [arrowsize=.5]
                            """)]
        self.dot_node = []
        self.dot_edge = []
        self.n_count = 0
        self.dot_footer = ['}']
        self.g = ""
    
    #replace each node label with Node object in abstract syntax tree
    #using depth first search to iterate each node
    def re_node(self,tree):
        s = '  node{} [label="{}"]\n'.format(self.n_count, tree.label())
        self.dot_node.append(s)
        tree.set_label(Node(self.n_count,tree.label()))
        self.n_count += 1
        for i in range(len(tree)):
            if not isinstance(tree[i],str):
                self.re_node(tree[i])
            else:
                s = '  node{} [label="{}"]\n'.format(self.n_count, tree[i])
                self.dot_node.append(s)
                tree[i] = Node(self.n_count,tree[i])
                self.n_count += 1
        
    #navigate each edges in ast recursively using dfs
    def dfs(self,tree):
        src = tree.label()
        for item in tree:
            if not isinstance(item,Node):
                dest = item.label()
                s = '  node{} -> node{}\n'.format(src.n, dest.n)
                self.dot_edge.append(s)
                self.dfs(item)
            else:
                src = tree.label()
                dest = item
                self.n_count += 1
                s = '  node{} -> node{}\n'.format(src.n, dest.n)
                self.dot_edge.append(s)
                
    def draw(self):
        self.re_node(self.tree)
        self.dfs(self.tree)
        g = "".join(self.dot_header + self.dot_node + self.dot_edge + self.dot_footer)
        return g