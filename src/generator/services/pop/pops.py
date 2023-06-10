import collections

import networkx as nx
import numpy as np
from numpy.random import Generator

from src.generator.services.weighted_graph import NodeType, NodeAttribute
from src.generator.services.pop._pop_structure import (
    _generate_level1_pop,
    _generate_level2_pop,
)


def add_pops(
    graph: nx.Graph,
    pops: np.ndarray,
    pop_region_labels: np.ndarray,
    random_generator: Generator,
    l1_amount: int,
) -> None:
    # Connecting PoPs
    core_nodes = [
        node
        for node, data in graph.nodes(data=True)
        if data[NodeAttribute.NodeType] == NodeType.Core
    ]
    pop_region_degree_sums: dict[str, int] = {}
    for node in core_nodes:
        region = graph.nodes[node][NodeAttribute.PopRegion]
        degree = graph.degree[node]
        if region in pop_region_degree_sums:
            pop_region_degree_sums[region] += degree
        else:
            pop_region_degree_sums[region] = degree
    sorted_pop_region_degree_sums = dict(
        collections.Counter(pop_region_degree_sums).most_common()
    )

    pops_per_region = [
        str(x) for x in collections.Counter(pop_region_labels).elements()
    ]

    cluster_assignment_ordered_by_degree = []
    for pop_region in sorted_pop_region_degree_sums.keys():
        while pop_region in pops_per_region:
            cluster_assignment_ordered_by_degree.append(pop_region)
            pops_per_region.remove(pop_region)
    l1_pops = cluster_assignment_ordered_by_degree[0:l1_amount]

    for index, pop in enumerate(pops):
        if str(pop_region_labels[index]) in l1_pops:
            _generate_level1_pop(
                coordinates=(pop[0], pop[1]),
                graph=graph,
                pop_region_labels=pop_region_labels,
                index=index,
                random_generator=random_generator,
                core_border_layer_routers=2,
                distribution_layer_routers=2,
                access_layer_routers=3,
            )
            l1_pops.remove(str(pop_region_labels[index]))
        else:
            _generate_level2_pop(
                coordinates=(pop[0], pop[1]),
                graph=graph,
                pop_region_labels=pop_region_labels,
                index=index,
                random_generator=random_generator,
            )
