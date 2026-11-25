from typing import Self
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, FiniteFloat, model_validator


class GraphNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    latitude: FiniteFloat | None = None
    longitude: FiniteFloat | None = None


class GraphEdge(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    from_: str = Field(alias="from", min_length=1)
    to: str = Field(min_length=1)
    weight: FiniteFloat = Field(ge=0)
    bidirectional: bool = False


class GraphDataset(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    description: str = ""
    source: str = "local-file"
    region: str = ""
    network_type: str = Field(default="abstract", alias="networkType")
    weight_unit: str = Field(default="relative", alias="weightUnit")
    extracted_at: datetime | None = Field(default=None, alias="extractedAt")
    attribution: str | None = None
    nodes: list[GraphNode] = Field(min_length=1)
    edges: list[GraphEdge] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_graph(self) -> Self:
        node_ids = [node.id for node in self.nodes]
        node_id_set = set(node_ids)

        if len(node_ids) != len(node_id_set):
            raise ValueError("Node id harus unik")

        for edge in self.edges:
            if edge.from_ not in node_id_set:
                raise ValueError(f"Edge from tidak menemukan node: {edge.from_}")
            if edge.to not in node_id_set:
                raise ValueError(f"Edge to tidak menemukan node: {edge.to}")

        return self


class DatasetSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    version: str
    description: str
    source: str
    region: str
    network_type: str = Field(alias="networkType")
    weight_unit: str = Field(alias="weightUnit")
    node_count: int = Field(alias="nodeCount")
    edge_count: int = Field(alias="edgeCount")
    validation_status: str = Field(alias="validationStatus")


class DatasetDetail(GraphDataset):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    node_count: int = Field(alias="nodeCount")
    edge_count: int = Field(alias="edgeCount")
    validation_status: str = Field(alias="validationStatus")
