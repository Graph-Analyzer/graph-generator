import networkx as nx
import numpy as np

from src.generator.services.weighted_graph import (
    graph_add_core_to_core_optimization_edge,
    NodeAttribute,
)
from src.generator.services.classes import Edge
from src.generator.services.topology._helper import _extract_node_coordinates
from src.generator.services.topology.delaunay import calculate_delaunay_topology_edges


# Based on and adapted from https://mkrechetov.github.io/gabriel_graphs
def calculate_gabriel_topology_edges(
    graph: nx.Graph,
) -> list[Edge]:
    nodes = _extract_node_coordinates(graph=graph)

    delaunay_edges = calculate_delaunay_topology_edges(graph=graph)

    gabriel_graph = nx.Graph()

    # Add delaunay edges to graph as a base, gabriel is subset
    for delaunay_edge in delaunay_edges:
        gabriel_graph.add_edge(delaunay_edge.start, delaunay_edge.end)

    # Gabriel graph, delaunay subset
    for edge in gabriel_graph.edges():
        for other in gabriel_graph.nodes():
            if other not in edge:
                point1 = np.array([nodes[edge[0]].x, nodes[edge[0]].y])
                point2 = np.array([nodes[edge[1]].x, nodes[edge[1]].y])
                point3 = np.array([nodes[other].x, nodes[other].y])
                center = 0.5 * (point1 + point2)
                radius = 0.5 * np.linalg.norm(point2 - point1)
                if np.linalg.norm(point3 - center) <= radius:
                    gabriel_graph.remove_edge(edge[0], edge[1])
                    break

    edges = []

    for edge in gabriel_graph.edges():
        edges.append(
            Edge(
                start=nodes[edge[0]].label,
                end=nodes[edge[1]].label,
            )
        )

    return edges


def optimize_gabriel_topology_edges(
    graph: nx.Graph,
) -> None:
    current_connections = set()
    for connection in graph.edges():
        current_connections.add(
            f"{graph.nodes[connection[0]].get(NodeAttribute.PopRegion)}_"
            f"{graph.nodes[connection[1]].get(NodeAttribute.PopRegion)}"
        )
        current_connections.add(
            f"{graph.nodes[connection[1]].get(NodeAttribute.PopRegion)}_"
            f"{graph.nodes[connection[0]].get(NodeAttribute.PopRegion)}"
        )

    core_nodes_articulation_points = list(nx.articulation_points(graph))
    for core_node_articulation_point in core_nodes_articulation_points:
        # Check to make sure it's still in current articulation points
        if core_node_articulation_point in list(nx.articulation_points(graph)):
            point = np.array(
                [
                    graph.nodes[core_node_articulation_point].get(
                        NodeAttribute.CoordinateX
                    ),
                    graph.nodes[core_node_articulation_point].get(
                        NodeAttribute.CoordinateY
                    ),
                ]
            )
            graph_copy = graph.copy()
            graph_copy.remove_node(core_node_articulation_point)
            sub_graphs = list(nx.connected_components(graph_copy))
            sub_graph_closest_nodes = {}
            for index_sub_graph, sub_graph in enumerate(sub_graphs):
                coords_array = np.zeros((len(sub_graph), 2))
                for index2, node in enumerate(sub_graph):
                    coords_array[index2][0] = graph.nodes[node][
                        NodeAttribute.CoordinateX
                    ]
                    coords_array[index2][1] = graph.nodes[node][
                        NodeAttribute.CoordinateY
                    ]
                distances = np.linalg.norm(coords_array - point, axis=1)
                closest_indices = np.argsort(distances)
                sub_graph_closest_nodes[index_sub_graph] = list(closest_indices)

            core_pairs = []
            for i in range(len(sub_graphs) - 1):
                for index, closest_node in enumerate(sub_graph_closest_nodes[i]):
                    for index3, closest_node2 in enumerate(
                        sub_graph_closest_nodes[i + 1]
                    ):
                        core_pairs.append(
                            (
                                list(sub_graphs[i])[closest_node],
                                list(sub_graphs[i + 1])[closest_node2],
                            )
                        )
            len_of_core_pairs = len(core_pairs) - 1
            for i, core_pair in enumerate(core_pairs):
                if core_node_articulation_point not in list(
                    nx.articulation_points(graph)
                ):
                    break
                core_node_1, core_node_2 = core_pair
                if (
                    f"{graph.nodes[core_node_1].get(NodeAttribute.PopRegion)}"
                    f"_"
                    f"{graph.nodes[core_node_2].get(NodeAttribute.PopRegion)}"  # noqa: E501
                    not in current_connections
                    or len_of_core_pairs == i
                ):
                    graph_add_core_to_core_optimization_edge(
                        graph=graph,
                        start=core_node_1,
                        end=core_node_2,
                    )
                    current_connections.add(
                        f"{graph.nodes[core_node_1].get(NodeAttribute.PopRegion)}"
                        f"_"
                        f"{graph.nodes[core_node_2].get(NodeAttribute.PopRegion)}"  # noqa: E501
                    )
                    current_connections.add(
                        f"{graph.nodes[core_node_2].get(NodeAttribute.PopRegion)}"
                        f"_"
                        f"{graph.nodes[core_node_1].get(NodeAttribute.PopRegion)}"  # noqa: E501
                    )
                    if core_node_articulation_point not in list(
                        nx.articulation_points(graph)
                    ):
                        break
