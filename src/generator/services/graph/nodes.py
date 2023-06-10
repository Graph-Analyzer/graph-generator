import math
import networkx as nx
import numpy as np
from numpy.random import Generator
from src.generator.models import RandomDistribution
from src.generator.services.weighted_graph import (
    graph_add_node,
    NodeType,
    graph_add_core_to_core_edge,
)
from src.generator.services.random.random import create_random_points
from src.generator.services.topology.delaunay import calculate_delaunay_topology_edges


def add_core_nodes_to_pop_regions(
    graph: nx.Graph,
    pop_regions: np.ndarray,
    pop_region_labels: np.ndarray,
    scaling_threshold: int,
    random_generator: Generator,
) -> None:
    # Add core nodes based on PoP regions
    # Currently at least 2 core nodes and one more for every 7 PoPs
    unique_pop_regions, unique_pop_regions_pop_count = np.unique(
        pop_region_labels, return_counts=True
    )

    for pop_region_index in range(len(pop_regions)):
        # At least 2 core nodes are placed per PoP region
        # Depending on the scaling threshold additional core nodes will be added
        core_nodes_scaled = math.floor(
            (unique_pop_regions_pop_count[pop_region_index] / scaling_threshold)
        )

        amount_of_core_nodes_to_generate = 2

        if core_nodes_scaled >= 1:
            amount_of_core_nodes_to_generate = 2 + core_nodes_scaled

        # Place core nodes randomly in radius of PoP region center
        random_x_coordinates = random_generator.uniform(
            low=pop_regions[pop_region_index][0] - 0.01,
            high=pop_regions[pop_region_index][0] + 0.01,
            size=amount_of_core_nodes_to_generate,
        )
        random_y_coordinates = random_generator.uniform(
            low=pop_regions[pop_region_index][1] - 0.01,
            high=pop_regions[pop_region_index][1] + 0.01,
            size=amount_of_core_nodes_to_generate,
        )

        # Used for meshing the core nodes of a pop region
        pop_region_graph = nx.Graph()

        for i in range(amount_of_core_nodes_to_generate):
            label = f"{pop_region_index}_{i}"
            coordinate_x = random_x_coordinates[i]
            coordinate_y = random_y_coordinates[i]

            graph_add_node(
                graph=pop_region_graph,
                label=label,
                coordinate_x=coordinate_x,
                coordinate_y=coordinate_y,
                pop_region=str(pop_region_index),
                node_type=NodeType.Core,
            )

            graph_add_node(
                graph=graph,
                label=label,
                coordinate_x=coordinate_x,
                coordinate_y=coordinate_y,
                pop_region=str(pop_region_index),
                node_type=NodeType.Core,
            )

        # Mesh core nodes in same PoP region
        # Just connect the core nodes when only 2 core nodes are present
        node_list = list(pop_region_graph.nodes())

        if 3 > pop_region_graph.number_of_nodes():
            graph_add_core_to_core_edge(
                graph=graph,
                start=node_list[0],
                end=node_list[1],
            )
        else:
            delaunay_edges = calculate_delaunay_topology_edges(graph=pop_region_graph)

            for delaunay_edge in delaunay_edges:
                graph_add_core_to_core_edge(
                    graph=graph,
                    start=delaunay_edge.start,
                    end=delaunay_edge.end,
                )


# Add additional random core nodes to graph
def add_random_core_nodes(
    graph: nx.Graph,
    amount: int,
    random_distribution: RandomDistribution,
    random_generator: Generator,
) -> None:
    random_core_nodes = create_random_points(
        points=amount,
        random_distribution=random_distribution,
        random_generator=random_generator,
    )

    for i in range(len(random_core_nodes)):
        random_core_node_name = f"random_{i}_1"

        # Random core nodes belong to their own PoP region
        graph_add_node(
            graph=graph,
            label=random_core_node_name,
            coordinate_x=random_core_nodes[i][0],
            coordinate_y=random_core_nodes[i][1],
            pop_region=random_core_node_name,
            node_type=NodeType.CoreRandom,
        )
