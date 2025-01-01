from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from IPython.display import display, Image

from agents.search_engine import research_node
from agents.analyst_engine import problem_solver_node
from agents.supervisor import supervisor_node
import os
from datetime import datetime



def build_graph():
    builder = StateGraph(MessagesState)
    builder.add_edge(START, "supervisor")
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("researcher", research_node)
    builder.add_node("analyst", problem_solver_node)
    graph = builder.compile()

    return graph


def plot_graph(graph, save_path="data/imgs/"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(save_path, f"graph_{timestamp}.png")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    png_data = graph.get_graph().draw_mermaid_png()

    with open(save_path, "wb") as file:
        file.write(png_data)

    print(f"Graph saved at {save_path}")
