import networkx as nx
from app.models.project import Project


class PertAlgorithm:

    @staticmethod
    def calculate(project: Project):

        if not project.activities:
            project.total_duration = 0
            project.critical_path = []
            return project

        # Tiempo esperado y varianza

        for activity in project.activities:

            activity.expected_time = round(
                (
                    activity.optimistic
                    + 4 * activity.most_likely
                    + activity.pessimistic
                ) / 6,
                2,
            )

            activity.variance = round(
                (
                    (
                        activity.pessimistic
                        - activity.optimistic
                    )
                    / 6
                ) ** 2,
                4,
            )

            activity.es = 0
            activity.ef = 0
            activity.ls = 0
            activity.lf = 0
            activity.slack = 0

        graph = nx.DiGraph()

        activity_map = {
            activity.name: activity
            for activity in project.activities
        }

        for activity in project.activities:
            graph.add_node(activity.name)

        for activity in project.activities:

            for predecessor in activity.predecessors:

                if predecessor not in activity_map:
                    continue

                graph.add_edge(predecessor, activity.name)

        if not nx.is_directed_acyclic_graph(graph):
            raise ValueError(
                "Existe un ciclo en las dependencias."
            )

        order = list(nx.topological_sort(graph))

        # Forward Pass

        for node in order:

            activity = activity_map[node]

            predecessors = list(
                graph.predecessors(node)
            )

            if predecessors:

                activity.es = max(
                    activity_map[p].ef
                    for p in predecessors
                )

            else:

                activity.es = 0

            activity.ef = round(
                activity.es
                + activity.expected_time,
                2,
            )

        project.total_duration = max(
            activity.ef
            for activity in project.activities
        )

        # Backward Pass

        for node in reversed(order):

            activity = activity_map[node]

            successors = list(
                graph.successors(node)
            )

            if successors:

                activity.lf = min(
                    activity_map[s].ls
                    for s in successors
                )

            else:

                activity.lf = project.total_duration

            activity.ls = round(
                activity.lf
                - activity.expected_time,
                2,
            )

            activity.slack = round(
                activity.ls
                - activity.es,
                2,
            )

        project.critical_path = [
            activity.name
            for activity in project.activities
            if abs(activity.slack) < 0.0001
        ]

        return project