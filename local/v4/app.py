from graph_builder import build_graph, plot_graph

graph = build_graph()

# afficher graphe agents
# plot_graph(graph)

for s in graph.stream(
    {"messages": [("user", "Find information about climate change")]}, subgraphs=True
):
    print(s)
    print("----")
