import networkx as nx
import numpy as np
from numpy.random import Generator
from src.generator.services.weighted_graph import (
    graph_add_node,
    NodeType,
    graph_add_core_to_pop_edge,
    graph_add_pop_to_pop_edge,
    NodeAttribute,
)


def _calculate_offset(
    n: int,
    coordinate: float,
) -> float:
    # n is odd
    if n % 2 == 1:
        return coordinate + (0.01 * (n + 1) / 2)
    # n is even
    else:
        return coordinate - (0.01 * n / 2)


def _generate_level1_pop(
    coordinates: tuple[float, float],
    graph: nx.Graph,
    index: int,
    pop_region_labels: np.ndarray,
    random_generator: Generator,
    core_border_layer_routers: int = 2,
    distribution_layer_routers: int = 2,
    access_layer_routers: int = 3,
) -> None:
    core_nodes = [
        node
        for node, data in graph.nodes(data=True)
        if data[NodeAttribute.PopRegion] == str(pop_region_labels[index])
        and data[NodeAttribute.NodeType] == NodeType.Core
    ]
    random_core_nodes = random_generator.choice(core_nodes, size=2, replace=False)

    # core-border-layer
    for i in range(core_border_layer_routers):
        graph_add_node(
            graph=graph,
            label=f"{pop_region_labels[index]}_level1_{index}_cbl_{i}",
            coordinate_x=_calculate_offset(i, coordinates[0]),
            coordinate_y=coordinates[1] - 0.01,
            pop_region=str(pop_region_labels[index]),
            node_type=NodeType.CoreBorderLayer,
        )
        graph_add_core_to_pop_edge(
            graph=graph,
            start=f"{pop_region_labels[index]}_level1_{index}_cbl_{i}",
            end=random_core_nodes[0 if i % 2 == 0 else 1],
        )

    # distribution-layer
    for i in range(distribution_layer_routers):
        graph_add_node(
            graph=graph,
            label=f"{pop_region_labels[index]}_level1_{index}_dl_{i}",
            coordinate_x=_calculate_offset(i, coordinates[0]),
            coordinate_y=coordinates[1] - 0.02,
            pop_region=str(pop_region_labels[index]),
            node_type=NodeType.DistributionLayer,
        )

        for cbl in range(core_border_layer_routers):
            graph_add_pop_to_pop_edge(
                graph=graph,
                start=f"{pop_region_labels[index]}_level1_{index}_cbl_{cbl}",
                end=f"{pop_region_labels[index]}_level1_{index}_dl_{i}",
            )

    for i in range(distribution_layer_routers - 1):
        graph_add_pop_to_pop_edge(
            graph=graph,
            start=f"{pop_region_labels[index]}_level1_{index}_dl_{i}",
            end=f"{pop_region_labels[index]}_level1_{index}_dl_{i + 1}",
        )

    # access-layer
    for i in range(access_layer_routers):
        graph_add_node(
            graph=graph,
            label=f"{pop_region_labels[index]}_level1_{index}_al_{i}",
            coordinate_x=_calculate_offset(i, coordinates[0]),
            coordinate_y=coordinates[1] - 0.04,
            pop_region=str(pop_region_labels[index]),
            node_type=NodeType.AccessLayer,
        )

        for cbl in range(distribution_layer_routers):
            graph_add_pop_to_pop_edge(
                graph=graph,
                start=f"{pop_region_labels[index]}_level1_{index}_dl_{cbl}",
                end=f"{pop_region_labels[index]}_level1_{index}_al_{i}",
            )


def _generate_level2_pop(
    coordinates: tuple[float, float],
    graph: nx.Graph,
    index: int,
    pop_region_labels: np.ndarray,
    random_generator: Generator,
    distribution_core_border_layer_routers: int = 2,
    access_layer_routers: int = 3,
) -> None:
    core_nodes = [
        node
        for node, data in graph.nodes(data=True)
        if data[NodeAttribute.PopRegion] == str(pop_region_labels[index])
        and data[NodeAttribute.NodeType] == NodeType.Core
    ]
    random_core_nodes = random_generator.choice(core_nodes, size=2, replace=False)

    # distribution-core-border-layer
    for i in range(distribution_core_border_layer_routers):
        graph_add_node(
            graph=graph,
            label=f"{pop_region_labels[index]}_level2_{index}_dcbl_{i}",
            coordinate_x=_calculate_offset(i, coordinates[0]),
            coordinate_y=coordinates[1] - 0.01,
            pop_region=str(pop_region_labels[index]),
            node_type=NodeType.DistributionCoreBorderLayer,
        )
        graph_add_core_to_pop_edge(
            graph=graph,
            start=f"{pop_region_labels[index]}_level2_{index}_dcbl_{i}",
            end=random_core_nodes[0 if i % 2 == 0 else 1],
        )

    for i in range(distribution_core_border_layer_routers - 1):
        graph_add_pop_to_pop_edge(
            graph=graph,
            start=f"{pop_region_labels[index]}_level2_{index}_dcbl_{i}",
            end=f"{pop_region_labels[index]}_level2_{index}_dcbl_{i + 1}",
        )

    # access-layer
    for i in range(access_layer_routers):
        graph_add_node(
            graph=graph,
            label=f"{pop_region_labels[index]}_level2_{index}_al_{i}",
            coordinate_x=_calculate_offset(i, coordinates[0]),
            coordinate_y=coordinates[1] - 0.02,
            pop_region=str(pop_region_labels[index]),
            node_type=NodeType.AccessLayer,
        )

        for dcbl in range(distribution_core_border_layer_routers):
            graph_add_pop_to_pop_edge(
                graph=graph,
                start=f"{pop_region_labels[index]}_level2_{index}_dcbl_{dcbl}",
                end=f"{pop_region_labels[index]}_level2_{index}_al_{i}",
            )
