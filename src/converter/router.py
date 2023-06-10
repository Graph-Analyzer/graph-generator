import networkx as nx
from fastapi import APIRouter, Response

from src.converter.models import FileFormat
from src.generator.models import (
    Graph,
)

router = APIRouter(tags=["converter"])


@router.post(
    "/convert",
    responses={200: {"content": {"application/xml": {}}}},
    response_class=Response,
)
async def convert(file_format: FileFormat, input_graph: Graph) -> Response:
    graph = nx.Graph()
    for node in input_graph.nodes:
        node_attributes = node.attributes.dict()

        # Extract enum values as writers can not handle it
        node_attributes["node_type"] = node.attributes.node_type.value

        graph.add_node(node.node_id, **node_attributes)

    for edge in input_graph.edges:
        edge_attributes = edge.attributes.dict()

        # Extract enum values as writers can not handle it
        edge_attributes["edge_type"] = edge.attributes.edge_type.value

        graph.add_edge(edge.node_from, edge.node_to, **edge_attributes)

    networkx_generator = None
    match file_format:
        case FileFormat.Gexf:
            networkx_generator = nx.generate_gexf(graph, version="1.2draft")
        case FileFormat.GraphML:
            networkx_generator = nx.generate_graphml(graph)

    # headers = {
    #      "Content-Disposition": "attachment; filename=graph.gexf",
    # }
    xml = "".join(networkx_generator)
    return Response(content=xml.encode("utf-8"), media_type="application/xml")
