from io import BytesIO
import networkx as nx
import plotly.graph_objects as go
from app.services.project_service import get_project


def build_graph_figure():
    project = get_project()

    graph = nx.DiGraph()

    for activity in project.activities:
        graph.add_node(activity.name)

    for activity in project.activities:
        for predecessor in activity.predecessors:
            graph.add_edge(predecessor, activity.name)

    if not graph.nodes:
        return None

    pos = nx.spring_layout(graph, seed=42)

    edge_x = []
    edge_y = []

    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=2, color="#9CA3AF"),
        hoverinfo="none"
    )

    activity_map = {
        activity.name: activity
        for activity in project.activities
    }

    node_x = []
    node_y = []
    node_text = []
    node_color = []

    for node in graph.nodes():

        activity = activity_map[node]

        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)

        node_text.append(
            f"{activity.name}<br>"
            f"TE: {activity.expected_time}<br>"
            f"ES: {activity.es}<br>"
            f"EF: {activity.ef}<br>"
            f"LS: {activity.ls}<br>"
            f"LF: {activity.lf}<br>"
            f"Slack: {activity.slack}"
        )

        node_color.append(
            "#DC2626"
            if activity.name in project.critical_path
            else "#7C4DFF"
        )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=list(graph.nodes()),
        textposition="top center",
        customdata=node_text,
        hovertemplate="%{customdata}<extra></extra>",
        marker=dict(
            size=35,
            color=node_color,
            line=dict(color="white", width=2)
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(
        template="plotly_white",
        height=650,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    return fig


def generate_graph():
    fig = build_graph_figure()

    if fig is None:
        return ""

    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )


def export_graph_png():

    fig = build_graph_figure()

    buffer = BytesIO()

    fig.write_image(
        buffer,
        format="png",
        width=1400,
        height=900,
        scale=2
    )

    buffer.seek(0)

    return buffer