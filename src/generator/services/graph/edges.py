import itertools

import networkx as nx
import numpy as np
from numpy.random import Generator
from src.generator.services.weighted_graph import (
    graph_add_core_to_core_edge,
    graph_add_core_to_core_random_edge,
    NodeAttribute,
)
from src.generator.models import Topology
from src.generator.services.classes import Edge


def connect_core_nodes(
    graph: nx.Graph,
    edges: list[Edge],
    topology: Topology,
    rearrange_edges: bool,
) -> None:
    # Connect core nodes based on the chosen topology
    connected_pop_regions = {}
    for core_node_edge in edges:
        core_node_1 = core_node_edge.start
        core_node_2 = core_node_edge.end

        # Always add edge when topology is a ring
        if topology == Topology.Ring:
            graph_add_core_to_core_edge(
                graph=graph,
                start=core_node_1,
                end=core_node_2,
            )
            continue

        # Only allow one edge between a pair of pop regions
        pop_region_1 = graph.nodes[core_node_1].get(NodeAttribute.PopRegion)
        pop_region_2 = graph.nodes[core_node_2].get(NodeAttribute.PopRegion)

        pop_region_connection_key = (
            f"{pop_region_1}_{pop_region_2}"
            if pop_region_1 <= pop_region_2
            else f"{pop_region_2}_{pop_region_1}"
        )

        # Add edge only if PoP regions are not yet connected
        # or the core nodes are in the same PoP region
        if (
            pop_region_connection_key not in connected_pop_regions
            or pop_region_1 == pop_region_2
        ):
            connected_pop_regions[pop_region_connection_key] = True

            if not (rearrange_edges and topology == Topology.Gabriel):
                graph_add_core_to_core_edge(
                    graph=graph,
                    start=core_node_1,
                    end=core_node_2,
                )
            else:
                core_nodes_region_1 = [
                    node
                    for node in graph.nodes()
                    if graph.nodes[node][NodeAttribute.PopRegion] == str(pop_region_1)
                ]
                core_nodes_degrees_region_1 = sorted(
                    graph.degree(core_nodes_region_1), key=lambda x: x[1]
                )

                core_nodes_region_2 = [
                    node
                    for node in graph.nodes()
                    if graph.nodes[node][NodeAttribute.PopRegion] == str(pop_region_2)
                ]
                core_nodes_degrees_region_2 = sorted(
                    graph.degree(core_nodes_region_2), key=lambda x: x[1]
                )

                possible_core_nodes_region_1 = [
                    node
                    for node, degree in core_nodes_degrees_region_1
                    if degree == core_nodes_degrees_region_1[0][1]
                ]

                possible_core_nodes_region_2 = [
                    node
                    for node, degree in core_nodes_degrees_region_2
                    if degree == core_nodes_degrees_region_2[0][1]
                ]

                distances = _calculate_distances(
                    graph=graph,
                    possible_core_nodes_region_1=possible_core_nodes_region_1,
                    possible_core_nodes_region_2=possible_core_nodes_region_2,
                )

                # Both core nodes that the edge connects can be in the same PoP region
                # The lowest degree core node of the two PoPs thus could be the same
                # Ensure that no self-connection happens
                if not distances:
                    possible_core_nodes_region_2 = [
                        node
                        for node, degree in core_nodes_degrees_region_2
                        if degree == core_nodes_degrees_region_2[1][1]
                    ]
                    distances = _calculate_distances(
                        graph=graph,
                        possible_core_nodes_region_1=possible_core_nodes_region_1,
                        possible_core_nodes_region_2=possible_core_nodes_region_2,
                    )

                min_distance_core_node1, min_distance_core_node2 = distances[0]
                graph_add_core_to_core_edge(
                    graph=graph,
                    start=min_distance_core_node1,
                    end=min_distance_core_node2,
                )


def add_random_edges(
    graph: nx.Graph,
    amount: int,
    random_generator: Generator,
) -> None:
    # Random core node connections
    core_nodes = [node for node, data in graph.nodes(data=True)]

    combinations = list(itertools.combinations(core_nodes, 2))
    for _ in range(amount):
        random_generator.shuffle(combinations)

        for core_node_1, core_node_2 in combinations:
            if not graph.has_edge(core_node_1, core_node_2):
                graph_add_core_to_core_random_edge(
                    graph=graph,
                    start=core_node_1,
                    end=core_node_2,
                )
                break


def _calculate_distances(
    graph: nx.Graph,
    possible_core_nodes_region_1: list[str],
    possible_core_nodes_region_2: list[str],
) -> list[tuple[str, str]]:
    distances = []

    # Loop over all pairs of nodes
    for possible_core_node_region_1 in possible_core_nodes_region_1:
        x1, y1 = (
            graph.nodes[possible_core_node_region_1][NodeAttribute.CoordinateX],
            graph.nodes[possible_core_node_region_1][NodeAttribute.CoordinateY],
        )
        for possible_core_node_region_2 in possible_core_nodes_region_2:
            # Continue if node is the same
            if possible_core_node_region_1 == possible_core_node_region_2:
                continue
            x2, y2 = (
                graph.nodes[possible_core_node_region_2][NodeAttribute.CoordinateX],
                graph.nodes[possible_core_node_region_2][NodeAttribute.CoordinateY],
            )
            # Calculate the distance between the two nodes a vector norm
            distance = np.linalg.norm([x2 - x1, y2 - y1])
            # Store the distance and node pair in the list
            distances.append(
                (distance, possible_core_node_region_1, possible_core_node_region_2)
            )

    # Sort the list by distance in ascending order
    distances.sort()
    # Extract only the relevant information from it and return
    node_pairs = [(node1, node2) for _, node1, node2 in distances]
    return node_pairs
