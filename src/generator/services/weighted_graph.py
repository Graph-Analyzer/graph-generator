from enum import Enum
import networkx as nx


class NodeAttribute(str, Enum):
    CoordinateX = "coordinate_x"
    CoordinateY = "coordinate_y"
    PopRegion = "pop_region"
    NodeType = "node_type"


class NodeType(str, Enum):
    Core = "core"
    CoreRandom = "core_random"
    CoreBorderLayer = "core_border_layer"
    DistributionCoreBorderLayer = "distribution_core_border_layer"
    DistributionLayer = "distribution_layer"
    AccessLayer = "access_layer"


class EdgeAttribute(str, Enum):
    Weight = "weight"
    EdgeType = "edge_type"


class EdgeType(str, Enum):
    CoreToCore = "core_to_core"
    CoreToCoreRandom = "core_to_core_random"
    CoreToCoreOptimization = "core_to_core_random_optimization"
    CoreToPop = "core_to_pop"
    PopToPop = "pop_to_pop"


def graph_add_node(
    graph: nx.Graph,
    label: str,
    coordinate_x: float,
    coordinate_y: float,
    pop_region: str,
    node_type: NodeType,
) -> None:
    graph.add_node(
        label,
        **{
            NodeAttribute.CoordinateX: coordinate_x,
            NodeAttribute.CoordinateY: coordinate_y,
            NodeAttribute.PopRegion: pop_region,
            NodeAttribute.NodeType: node_type,
        }
    )


def graph_add_core_to_core_edge(
    graph: nx.Graph,
    start: str,
    end: str,
) -> None:
    graph.add_edge(
        start,
        end,
        **{
            EdgeAttribute.Weight: 1,
            EdgeAttribute.EdgeType: EdgeType.CoreToCore,
        }
    )


def graph_add_core_to_core_random_edge(
    graph: nx.Graph,
    start: str,
    end: str,
) -> None:
    graph.add_edge(
        start,
        end,
        **{
            EdgeAttribute.Weight: 1,
            EdgeAttribute.EdgeType: EdgeType.CoreToCoreRandom,
        }
    )


def graph_add_core_to_core_optimization_edge(
    graph: nx.Graph,
    start: str,
    end: str,
) -> None:
    graph.add_edge(
        start,
        end,
        **{
            EdgeAttribute.Weight: 1,
            EdgeAttribute.EdgeType: EdgeType.CoreToCoreOptimization,
        }
    )


def graph_add_core_to_pop_edge(
    graph: nx.Graph,
    start: str,
    end: str,
) -> None:
    graph.add_edge(
        start,
        end,
        **{
            EdgeAttribute.Weight: 100,
            EdgeAttribute.EdgeType: EdgeType.CoreToPop,
        }
    )


def graph_add_pop_to_pop_edge(
    graph: nx.Graph,
    start: str,
    end: str,
) -> None:
    graph.add_edge(
        start,
        end,
        **{
            EdgeAttribute.Weight: 10,
            EdgeAttribute.EdgeType: EdgeType.PopToPop,
        }
    )
