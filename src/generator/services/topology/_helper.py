import networkx as nx
import numpy as np
from src.generator.services.classes import _Node
from src.generator.services.weighted_graph import NodeAttribute


def _extract_node_coordinates(
    graph: nx.Graph,
) -> dict[str, _Node]:
    nodes = {}
    for node in graph.nodes(data=True):
        label = node[0]
        x = node[1].get(NodeAttribute.CoordinateX)
        y = node[1].get(NodeAttribute.CoordinateY)

        nodes[label] = _Node(
            label=label,
            x=x,
            y=y,
        )

    return nodes


# Converts a list of nodes into a numpy array representation
# of the x and y coordinates
def _convert_node_coordinates_to_array(
    nodes: dict[str, _Node],
) -> np.ndarray:
    node_coordinates = np.empty(shape=(0, 2))
    for _, node in nodes.items():
        node_coordinates = np.append(
            arr=node_coordinates,
            values=[np.array([node.x, node.y])],
            axis=0,
        )

    return node_coordinates
