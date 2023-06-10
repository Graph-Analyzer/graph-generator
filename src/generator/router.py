from fastapi import APIRouter, HTTPException
from src.generator.models import (
    Graph,
    Generator,
    Node,
    NodeAttributes,
    Edge,
    EdgeAttributes,
)
from src.generator.services.exceptions import InternalError, InputError
from src.generator.services.generate_topology import generate_topology

router = APIRouter(tags=["generator"])


@router.post("/generate")
async def generate(gen: Generator) -> Graph:
    try:
        graph = generate_topology(gen)
    except InputError as error:
        raise HTTPException(
            status_code=400,
            detail=error.message,
        )
    except InternalError as error:
        raise HTTPException(
            status_code=500,
            detail=error.message,
        )

    return Graph(
        nodes=[
            Node(node_id=k, attributes=NodeAttributes(**attr))
            for k, attr in graph.nodes(data=True)
        ],
        edges=[
            Edge(node_from=src, node_to=dst, attributes=EdgeAttributes(**attr))
            for src, dst, attr in graph.edges(data=True)
        ],
    )
