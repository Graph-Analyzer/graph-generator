import networkx as nx
from python_tsp.distances import euclidean_distance_matrix
from python_tsp.heuristics import solve_tsp_local_search, solve_tsp_simulated_annealing
from src.generator.services.classes import Edge
from src.generator.services.topology._helper import (
    _extract_node_coordinates,
    _convert_node_coordinates_to_array,
)


def calculate_ring_topology_edges(
    graph: nx.Graph,
) -> list[Edge]:
    nodes = _extract_node_coordinates(graph=graph)
    coordinates = _convert_node_coordinates_to_array(nodes=nodes)

    # Return values are index based
    distance_matrix = euclidean_distance_matrix(sources=coordinates)

    permutation, distance = solve_tsp_simulated_annealing(
        distance_matrix=distance_matrix,
    )
    permutation2, distance2 = solve_tsp_local_search(
        distance_matrix,
        x0=permutation,
        perturbation_scheme="ps3",
    )

    edges = []
    nodes_list = list(nodes)

    for i in range(len(permutation2) - 1):
        start = nodes[nodes_list[permutation2[i]]].label
        end = nodes[nodes_list[permutation2[i + 1]]].label

        edges.append(
            Edge(
                start=start,
                end=end,
            )
        )

    # Add edge from last node to first node
    start = nodes[nodes_list[permutation2[-1]]].label
    end = nodes[nodes_list[permutation2[0]]].label

    edges.append(
        Edge(
            start=start,
            end=end,
        )
    )

    return edges
