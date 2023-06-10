import networkx as nx
from scipy.spatial import Delaunay
from src.generator.services.classes import Edge
from src.generator.services.topology._helper import (
    _extract_node_coordinates,
    _convert_node_coordinates_to_array,
)


def calculate_delaunay_topology_edges(
    graph: nx.Graph,
) -> list[Edge]:
    nodes = _extract_node_coordinates(graph=graph)
    coordinates = _convert_node_coordinates_to_array(nodes=nodes)

    triangulation = Delaunay(
        points=coordinates,
        furthest_site=False,
        incremental=False,
    )

    delaunay_graph = nx.Graph()

    point_to_neighbouring_points_mapping = triangulation.vertex_neighbor_vertices[0]
    neighbouring_points = triangulation.vertex_neighbor_vertices[1]
    for originating_point in range(len(coordinates)):
        for neighbouring_point in neighbouring_points[
            point_to_neighbouring_points_mapping[
                originating_point
            ] : point_to_neighbouring_points_mapping[originating_point + 1]
        ]:
            if originating_point < neighbouring_point:
                delaunay_graph.add_edge(originating_point, neighbouring_point)

    edges = []
    nodes_list = list(nodes)

    for edge in delaunay_graph.edges():
        start = nodes[nodes_list[edge[0]]].label
        end = nodes[nodes_list[edge[1]]].label

        edges.append(
            Edge(
                start=start,
                end=end,
            )
        )

    return edges
