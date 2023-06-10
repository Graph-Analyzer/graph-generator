import networkx as nx
from src.generator.models import Generator, Topology
from src.generator.services.clustering.kmeans import calc_kmeans
from src.generator.services.exceptions import InternalError, InputError
from src.generator.services.graph.edges import connect_core_nodes, add_random_edges
from src.generator.services.graph.nodes import (
    add_core_nodes_to_pop_regions,
    add_random_core_nodes,
)
from src.generator.services.pop.pops import add_pops
from src.generator.services.random.random import (
    create_random_points,
    create_random_generator,
)
from src.generator.services.topology.gabriel import (
    calculate_gabriel_topology_edges,
    optimize_gabriel_topology_edges,
)
from src.generator.services.topology.ring import calculate_ring_topology_edges


def generate_topology(
    param: Generator,
    seed: int | None = None,
) -> nx.Graph:
    # Create random generator with seed if provided
    # Seed should only be used for development purposes
    random_generator = create_random_generator(seed=seed)

    pop_amount = param.l1_pops + param.l2_pops

    # Check if there are not more regions to generate than PoPs
    # A region requires at least one PoP
    if pop_amount < param.pop_regions:
        raise InputError(
            message="Amount of PoP regions can not be higher than total amount of PoPs."
        )

    # Create randomly distributed points that represent PoPs
    pops = create_random_points(
        points=pop_amount,
        random_distribution=param.random_distribution,
        random_generator=random_generator,
    )

    # Cluster PoPs into regions
    pop_regions, pop_region_labels = calc_kmeans(
        coordinates=pops, clusters=param.pop_regions, seed=seed
    )

    # Create the graph that will hold the generated topology
    topology_graph = nx.Graph()

    # Add core nodes to graph based on the PoP regions
    add_core_nodes_to_pop_regions(
        graph=topology_graph,
        pop_regions=pop_regions,
        pop_region_labels=pop_region_labels,
        scaling_threshold=param.core_node_scaling_threshold,
        random_generator=random_generator,
    )

    # Add random core nodes to graph
    add_random_core_nodes(
        graph=topology_graph,
        amount=param.random_core_nodes,
        random_distribution=param.random_distribution,
        random_generator=random_generator,
    )

    core_node_edges = []

    # Get core node edges for graph according to the selected topology
    match param.topology:
        case Topology.Gabriel:
            core_node_edges = calculate_gabriel_topology_edges(
                graph=topology_graph,
            )
        case Topology.Ring:
            core_node_edges = calculate_ring_topology_edges(
                graph=topology_graph,
            )

    # Connect the core nodes with the previously calculated edges
    connect_core_nodes(
        graph=topology_graph,
        edges=core_node_edges,
        topology=param.topology,
        rearrange_edges=param.no_cut_edges_and_nodes,
    )

    amount_core_nodes = topology_graph.number_of_nodes()
    amount_full_mesh_edges = int(amount_core_nodes * (amount_core_nodes - 1) / 2)

    # Check if the amount of edges does not exceed the potential maximum
    if (
        param.random_core_node_connections + topology_graph.number_of_edges()
        > amount_full_mesh_edges
    ):
        raise InputError(
            message=f"Number of random_core_node_connections is too high, "
            f"would exceed a full mesh with {amount_full_mesh_edges} edges: "
            f"{param.random_core_node_connections} + {topology_graph.number_of_edges()}"
            f"(current core node edges) > {amount_full_mesh_edges})."
        )

    # Add random core node edges to graph
    add_random_edges(
        graph=topology_graph,
        amount=param.random_core_node_connections,
        random_generator=random_generator,
    )

    # Mitigate cut edges and articulation points in the graph for the gabriel topology
    if param.no_cut_edges_and_nodes and param.topology == Topology.Gabriel:
        optimize_gabriel_topology_edges(graph=topology_graph)

    # Create PoP structures
    add_pops(
        graph=topology_graph,
        pops=pops,
        pop_region_labels=pop_region_labels,
        random_generator=random_generator,
        l1_amount=param.l1_pops,
    )

    # Sanity check after mitigation
    # There should be no cut edges or articulation points present
    if (
        param.no_cut_edges_and_nodes
        and len(list(nx.articulation_points(topology_graph))) != 0
    ):
        raise InternalError(
            message="The graph contains cut edges or articulation points."
        )

    return topology_graph
