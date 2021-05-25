import sys
import networkx as nx
import matplotlib.pyplot as plt
import timeit

printSteps = False


def prepare_graph(graph):
    for node in graph.nodes:
        graph.nodes[node]['visited'] = 0
    return graph


def getGraphFromFile(fileName):
    graph = nx.Graph()

    with open(fileName) as f:
        for line in f:
            edge = []
            for word in line.split():
                edge.append(int(word))
            graph.add_edge(edge[0], edge[1])
            del edge[:]
    return graph


def writeGraph(graph, maxSet):
    f = open("results.txt", "w")

    f.write("\nNumber of nodes in maximum independent set: ")
    f.write(str(len(maxSet)))
    f.write("\nMaximum independent set: ")
    f.write(" ".join(str(node) for node in maxSet))

    f.write("\nList of edges:\n")
    for edge in graph.edges:
        stringEdges = str(edge[0]) + " " + str(edge[1]) + '\n'
        f.write(stringEdges)

    f.close()


def find_independent_set(G):
    final_set = set()
    sub_graphs = (G.subgraph(c) for c in nx.connected_components(G))
    for graph in sub_graphs:
        max_set = set()
        for node in graph.nodes:
            new_set = backtrack_nodes(graph, node, {node})
            if printSteps:
                print(new_set)
            if len(new_set) > len(max_set):
                max_set = new_set
            graph.nodes[node]['visited'] = 1
        final_set.update(max_set)

    return final_set


def backtrack_nodes(graph, node, independentSet):
    neighbors = set(graph[node].keys())
    graph.nodes[node]['visited'] = 1
    if not(neighbors & independentSet):
        independentSet.add(node)

    for neighbor in neighbors:
        if graph.nodes[neighbor]['visited'] != 1:
            independentSet = backtrack_nodes(graph, neighbor, independentSet)
    graph.nodes[node]['visited'] = 0
    return independentSet


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Wrong arguments")
        sys.exit()

    if "-r" in sys.argv:
        printSteps = True

    mode = sys.argv[1]
    if mode == "-f":
        graph = getGraphFromFile(sys.argv[2])

    elif mode == "-c":
        nodes = int(sys.argv[2])
        edges = int(sys.argv[3])
        graph = nx.gnm_random_graph(nodes, edges)

    elif mode == "-t":
        nodes = int(sys.argv[2])
        edges = int(sys.argv[3])
        times = int(sys.argv[4])

        start = timeit.default_timer()
        for i in range(0, times):
            graph = nx.gnm_random_graph(nodes, edges)
            prepare_graph(graph)
            listOfNodes = set(graph.nodes)
            maxSet = find_independent_set(graph)

        stop = timeit.default_timer()
        print("Average execution time: ", (stop - start) / times)
        sys.exit()

    else:
        sys.exit("Wrong arguments list.")

    listOfNodes = set(graph.nodes)
    prepare_graph(graph)
    start = timeit.default_timer()
    maxSet = find_independent_set(graph)
    stop = timeit.default_timer()

    print("Number of nodes in maximum independent set: ", len(maxSet))
    print("Maximum independent set: ", maxSet)

    print("Execution time: ", stop - start)

    if "-w" in sys.argv:
        writeGraph(graph, maxSet)

    if "-d" in sys.argv:
        plt.subplot(121)
        nx.draw(graph, with_labels=True, font_weight='bold')
        plt.show()
