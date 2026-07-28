import networkx as nx

from app.services.project_service import get_project


def build_graph():

    project = get_project()

    graph = nx.DiGraph()

    for activity in project.activities:

        graph.add_node(activity.name)

    for activity in project.activities:

        for predecessor in activity.predecessors:

            graph.add_edge(
                predecessor,
                activity.name
            )

    return graph