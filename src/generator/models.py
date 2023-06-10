from enum import Enum
from pydantic import BaseModel, Field


class RandomDistribution(str, Enum):
    Uniform = "uniform"
    Normal = "normal"


class Topology(str, Enum):
    Gabriel = "gabriel"
    Ring = "ring"


class Generator(BaseModel):
    l1_pops: int | None = Field(default=5, title="Number of level 1 PoPs", ge=0)
    l2_pops: int | None = Field(default=20, title="Number of level 2 PoPs", ge=0)
    pop_regions: int | None = Field(default=5, title="Number of PoP regions", ge=2)
    core_node_scaling_threshold: int | None = Field(
        default=7, title="Threshold that defines the scaling of the core nodes", ge=1
    )
    random_core_nodes: int | None = Field(
        default=2, title="Number of additional random core nodes", ge=0
    )
    random_core_node_connections: int | None = Field(
        default=2, title="Number of additional random core node connections", ge=0
    )
    random_distribution: RandomDistribution | None = Field(
        default=RandomDistribution.Uniform, title="Random distribution"
    )
    topology: Topology | None = Field(default=Topology.Gabriel, title="Topology type")
    no_cut_edges_and_nodes: bool | None = Field(
        default=True, title="Create a topology without cut edges and cut nodes"
    )


class NodeType(str, Enum):
    Core = "core"
    CoreRandom = "core_random"
    CoreBorderLayer = "core_border_layer"
    DistributionCoreBorderLayer = "distribution_core_border_layer"
    DistributionLayer = "distribution_layer"
    AccessLayer = "access_layer"


class EdgeType(str, Enum):
    CoreToCore = "core_to_core"
    CoreToCoreRandom = "core_to_core_random"
    CoreToCoreOptimization = "core_to_core_random_optimization"
    CoreToPop = "core_to_pop"
    PopToPop = "pop_to_pop"


class NodeAttributes(BaseModel):
    pop_region: str
    node_type: NodeType
    coordinate_x: float
    coordinate_y: float


class EdgeAttributes(BaseModel):
    weight: float
    edge_type: EdgeType


class Node(BaseModel):
    node_id: str
    attributes: NodeAttributes


class Edge(BaseModel):
    node_from: str
    node_to: str
    attributes: EdgeAttributes


class Graph(BaseModel):
    nodes: list[Node] = []
    edges: list[Edge] = []
