import ast
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt

node_labels = {}

node_colors = []

colors = {
    ast.Name: '#7CF381',
    ast.arg: '#B6FC6B',
    ast.Call: '#7CB6F3',
    ast.BinOp: '#4EF2DC',
    ast.UnaryOp: '#4EF2DC',
    ast.Add: '#4EF2DC',
    ast.Sub: '#4EF2DC',
    ast.USub: '#4EF2DC',
    ast.Attribute: '#2AA135',
    ast.Constant: '#F1F37C',
    ast.Subscript: '#AD6BFC',
    ast.List: '#F99FFE',
    ast.Slice: '#FE4CB3'
}

default_color = '#FFFFFF'


def get_label(node):
    if isinstance(node, ast.Constant):
        return f'Constant:\n{node.value}'
    elif isinstance(node, ast.Name):
        return f'Name:\n{node.id}'
    elif isinstance(node, ast.Attribute):
        return f'Attribute:\n{node.attr}'
    elif isinstance(node, ast.Add):
        return '+'
    elif isinstance(node, ast.USub) or isinstance(node, ast.Sub):
        return '-'
    elif isinstance(node, ast.arg):
        return f'Argument:\n{node.arg}'
    else:
        return node.__class__.__name__.title()


def get_color(node):
    return colors.get(type(node), default_color)


def build_graph(node, parent, graph):
    idx = len(node_labels)
    graph.add_node(idx)
    label, color = get_label(node), get_color(node)
    node_labels[idx] = label
    node_colors.append(color)
    if parent is not None:
        graph.add_edge(parent, idx)
    for child in ast.iter_child_nodes(node):
        build_graph(child, idx, graph)


if __name__ == '__main__':
    with open('fib.py', 'r') as fib_file:
        fib_code = fib_file.read()

    ast_graph = nx.Graph()
    build_graph(ast.parse(fib_code), None, ast_graph)

    plt.figure(figsize=(35, 15))
    pos = graphviz_layout(ast_graph, prog="dot")
    nx.draw(ast_graph, pos,
            labels=node_labels,
            node_size=6000,
            node_shape='o',
            node_color=node_colors,
            edgecolors='black',
            width=2.0)
    plt.savefig('artifacts/fib_ast.png', format="PNG")
