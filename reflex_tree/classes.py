import reflex as rx
import uuid
from typing import List, Optional
from pydantic import BaseModel

class ChatNode(BaseModel):
    id: str
    role: str = "user"
    content: str = ""
    parent_id: Optional[str] = None
    children_ids: List[str] = []
    timestamp: str = ""
    tokens: int = 0
    cost: float = 0.0
    model: Optional[str] = None # Added model field

    is_grafted: bool = False

    @staticmethod
    def create(role: str, content: str, parent_id: Optional[str] = None, tokens: int = 0, cost: float = 0.0, is_grafted: bool = False, model: Optional[str] = None) -> "ChatNode":
        return ChatNode(
            id=str(uuid.uuid4())[:8],
            role=role,
            content=content,
            parent_id=parent_id,
            children_ids=[],
            timestamp=str(uuid.uuid1()),
            tokens=tokens,
            cost=cost,
            is_grafted=is_grafted,
            model=model
        )

def flatten_tree(node_data: dict, parent_id: Optional[str] = None) -> dict[str, ChatNode]:
    """
    recursively parses nested dict (from DB) into a flat dict of {id: ChatNode}.
    """
    nodes = {}
    
    # Ensure ID exists
    if "id" not in node_data:
        node_data["id"] = str(uuid.uuid4())[:8]
    
    current_id = node_data["id"]
    
    # Create Children Objects first to get their IDs
    children_ids = []
    
    # Process children
    for child_data in node_data.get("children", []):
        child_flat = flatten_tree(child_data, parent_id=current_id)
        nodes.update(child_flat)
        children_ids.append(child_data["id"])

    # Create current node
    node = ChatNode(
        id=current_id,
        role=node_data.get("role", "user"),
        content=node_data.get("content", ""),
        parent_id=parent_id,
        children_ids=children_ids,
        timestamp=node_data.get("timestamp", str(uuid.uuid1())),
        tokens=node_data.get("tokens", 0),
        cost=node_data.get("cost", 0.0),
        is_grafted=node_data.get("is_grafted", False),
        model=node_data.get("model", None)
    )
    nodes[current_id] = node
    return nodes

def build_tree_dict(nodes: dict[str, ChatNode], root_id: str) -> dict:
    """
    Reconstructs nested dict from flat dict for DB saving.
    """
    if root_id not in nodes:
        return {}
        
    root = nodes[root_id]
    return {
        "id": root.id,
        "role": root.role,
        "content": root.content,
        "timestamp": root.timestamp,
        "tokens": root.tokens,
        "cost": root.cost,
        "is_grafted": root.is_grafted,
        "model": root.model,
        "children": [build_tree_dict(nodes, child_id) for child_id in root.children_ids]
    }

class NodeView(BaseModel):
    id: str
    role: str
    content: str
    children: List["NodeView"] = []

NodeView.update_forward_refs()
