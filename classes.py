import uuid
from google.genai import types

class ChatNode:
    def __init__(self, role, content, parent=None):
        self.id = str(uuid.uuid4())[:8]
        self.role = role
        self.content = content
        self.parent = parent
        self.children = []
        self.timestamp = str(uuid.uuid1())

    def add_child(self, node):
        self.children.append(node)
        return node

    def get_history(self):
        history = []
        nodes = []
        current = self
        while current:
            history.insert(0, types.Content(
                role=current.role,
                parts=[types.Part(text=current.content)]
            ))
            nodes.insert(0, current)
            current = current.parent
        return history, nodes

    def get_question_label(self):
        if self.role != "user": return None
        prefix = ""
        ancestor = self.parent
        while ancestor:
            if ancestor.role == "user":
                prefix = ancestor.get_question_label()
                break
            ancestor = ancestor.parent
        
        if self.parent:
            siblings = [child for child in self.parent.children if child.role == "user"]
            try:
                my_index = siblings.index(self) + 1
            except ValueError:
                my_index = 1
        else:
            my_index = 1

        if prefix: return f"{prefix}.{my_index}"
        else: return str(my_index)