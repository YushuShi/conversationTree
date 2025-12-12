import reflex as rx
import os
import uuid
from typing import List, Dict, Optional, Any
from .classes import ChatNode, flatten_tree, NodeView
from . import config, database
from google.genai import types, Client
import openai
import anthropic

class State(rx.State):
    """The app state."""
    
    # --- Auth State ---
    # --- Auth State ---
    user: Optional[Dict[str, Any]] = None # Includes total_cost, total_tokens, api_keys
    auth_email: str = ""
    auth_password: str = ""
    show_login: bool = False # Toggle modal visibility
    is_signup_mode: bool = False # Toggle Login vs Signup form

    def toggle_auth_mode(self):
        self.is_signup_mode = not self.is_signup_mode

    def toggle_login_modal(self):
        self.show_login = not self.show_login

    def signup(self):
        if not self.auth_email or not self.auth_password:
             return rx.window_alert("Please enter email and password.")
        
        success = database.create_user(self.auth_email, self.auth_password)
        if success:
            # Auto login
            self.login()
        else:
            return rx.window_alert("User already exists or error creating account.")

    def login(self):
        user_data = database.authenticate_user(self.auth_email, self.auth_password)
        if user_data:
            self.user = user_data
            self.show_login = False
            # Load API Keys
            if user_data.get("openai_key"): self.openai_api_key = user_data["openai_key"]
            if user_data.get("anthropic_key"): self.anthropic_api_key = user_data["anthropic_key"]
            if user_data.get("google_key"): self.google_api_key = user_data["google_key"]
        else:
            return rx.window_alert("Invalid email or password.")

    def logout(self):
        self.user = None
        self.auth_email = ""
        self.auth_password = ""
        
        # Reset Session Stats
        self.session_cost = 0.0
        self.session_tokens = 0
        
        # Clear keys 
        self.openai_api_key = config.OPENAI_API_KEY or ""
        self.anthropic_api_key = config.ANTHROPIC_API_KEY or ""
        self.google_api_key = config.GOOGLE_API_KEY or ""
        
        # Reset UI
        self.show_login = True
        self.start_new_chat()

    @rx.var
    def is_logged_in(self) -> bool:
        return self.user is not None

    # --- API Keys ---
    openai_api_key: str = config.OPENAI_API_KEY or ""
    anthropic_api_key: str = config.ANTHROPIC_API_KEY or ""
    google_api_key: str = config.GOOGLE_API_KEY or ""

    @rx.var
    def current_api_key_placeholder(self) -> str:
        model = config.MODELS.get(self.selected_model_key)
        if not model: return "API Key"
        provider = model.get("provider", "google")
        if provider == "openai": return "OpenAI API Key (sk-...)"
        if provider == "anthropic": return "Anthropic API Key (sk-ant...)"
        if provider == "google": return "Google API Key"
        return "API Key"

    @rx.var
    def current_api_key(self) -> str:
        model = config.MODELS.get(self.selected_model_key)
        if not model: return ""
        provider = model.get("provider", "google")
        
        if provider == "openai": return self.openai_api_key
        if provider == "anthropic": return self.anthropic_api_key
        if provider == "google": return self.google_api_key
        return ""

    def set_current_api_key(self, key: str):
        model = config.MODELS.get(self.selected_model_key)
        if not model: return
        provider = model.get("provider", "google")
        
        if provider == "openai": self.openai_api_key = key
        elif provider == "anthropic": self.anthropic_api_key = key
        elif provider == "google": self.google_api_key = key
        
        # Persist if logged in
        if self.user:
            database.update_user_api_keys(
                self.user["email"], 
                self.openai_api_key, 
                self.anthropic_api_key, 
                self.google_api_key
            )

    # --- Deprecated specific setters if generic one works? 
    # Let's keep them for safety if needed, or remove to clean up.
    # User asked to combine, so generic logic replaces specific manual calls.

    # --- Conversation State ---
    nodes: Dict[str, ChatNode] = {}
    root_id: str = ""
    current_node_id: str = ""
    
    # --- Settings ---
    temperature: float = 0.7
    generation_seed: int = 42
    selected_model_key: str = config.DEFAULT_MODEL_KEY
    use_google_search: bool = False

    
    # --- Sidebar State ---
    chat_list: List[Dict] = []

    
    # --- UI State ---
    show_full_history: bool = False
    processing: bool = False
    
    def set_auth_email(self, email: str):
        self.auth_email = email
        
    def set_auth_password(self, password: str):
        self.auth_password = password
        
    def set_use_google_search(self, enable: bool):
        self.use_google_search = enable
    
    def on_load(self):
        """Initialize the app."""
        # Create a default empty conversation if none exists
        if not self.root_id:
            database.init_db() # Ensure DB is initialized/migrated
            # Try to load latest if logged in?
            # For now just start new or keep current
            self.start_new_chat()
            
        if self.user:
            self.load_chat_list()
        else:
            # Reset stats for guest on refresh
            self.session_cost = 0.0
            self.session_tokens = 0
            # Reset keys
            self.openai_api_key = config.OPENAI_API_KEY or ""
            self.anthropic_api_key = config.ANTHROPIC_API_KEY or ""
            self.google_api_key = config.GOOGLE_API_KEY or ""

    def start_new_chat(self):
        """Save current and start new."""
        if self.user and self.root_id:
             database.save_conversation(self.user["email"], self.nodes, self.root_id)
             self.load_chat_list()
             
        root = ChatNode.create(role="system", content="System Prompt: You are a helpful assistant.")
        self.nodes = {root.id: root}
        self.root_id = root.id
        self.current_node_id = root.id
        self.processing = False
        
    def add_new_topic(self):
        """Start a new topic (branch) in the current conversation."""
        if self.root_id and self.root_id in self.nodes:
            self.current_node_id = self.root_id
            self.show_full_history = False # Reset view logic if needed
        
    def load_chat_list(self):
        if self.user:
            self.chat_list = [
                {"id": r[0], "title": r[1], "updated_at": r[2]} 
                for r in database.get_user_conversations(self.user["email"])
            ]
            
    def load_chat(self, chat_id: str):
        if self.user:
            # Save current first
             if self.root_id:
                database.save_conversation(self.user["email"], self.nodes, self.root_id)
            
             nodes = database.load_conversation(chat_id)
             if nodes:
                 self.nodes = nodes
                 self.root_id = chat_id
                 # Set current to last user message or root?
                 # Let's simple check root
                 if chat_id in self.nodes:
                     self.current_node_id = chat_id
                     # Try to find last active node?
                     # For now just root is safe, or last added
                 self.load_chat_list() # Refresh list order

    
    # --- Drag & Drop ---
    dragged_chat_id: str = ""
    
    def set_dragged_chat_id(self, chat_id: str):
        self.dragged_chat_id = chat_id
        
    dragged_node_id: str = ""

    def set_dragged_node_id(self, node_id: str):
        self.dragged_node_id = node_id

    def graft_conversation(self, target_node_id: str):
        """Grafts a conversation (from history or current tree) onto the target_node_id."""
        source_nodes = {}
        source_root_ids = []

        if self.dragged_node_id:
            # Internal Drag: Source is in the current tree
            if self.dragged_node_id == target_node_id:
                return # Can't graft onto self
            
            # Prevent grafting a parent onto its own child (cycle detection)
            # Simple check: Walk up from target to root. If dragged_id is in path, abort.
            curr = target_node_id
            while curr:
                if curr == self.dragged_node_id:
                    return # Cycle detected
                curr = self.nodes[curr].parent_id if curr in self.nodes else None

            source_nodes = self.nodes
            source_root_ids = [self.dragged_node_id]

        elif self.dragged_chat_id:
            # History Drag: Source is a saved chat
            if self.dragged_chat_id == self.root_id:
                return 

            loaded_nodes = database.load_conversation(self.dragged_chat_id)
            if not loaded_nodes or self.dragged_chat_id not in loaded_nodes:
                return
            
            source_nodes = loaded_nodes
            root_node = source_nodes[self.dragged_chat_id]
            
            # Handle System Node skipping
            if root_node.role == "system":
                source_root_ids = root_node.children_ids
            else:
                source_root_ids = [root_node.id]
        else:
            return

        # Perform Grafting
        # Check if target is a User node with a Model child. 
        # If so, graft onto the Model child to preserve Q->A->Q flow.
        target_node = self.nodes.get(target_node_id)
        if target_node and target_node.role == "user":
             for cid in target_node.children_ids:
                 child = self.nodes.get(cid)
                 if child and child.role == "model":
                     target_node_id = cid
                     break

        for root_id in source_root_ids:
            self._clone_subtree_recursive(root_id, target_node_id, source_nodes)
        
        # Save and Cleanup
        # Assuming save_chat is a method, if not, use database.save_conversation directly
        if self.user:
            database.save_conversation(self.user["email"], self.nodes, self.root_id)
        self.dragged_chat_id = ""
        self.dragged_node_id = ""

    def _clone_subtree_recursive(self, old_node_id: str, new_parent_id: str, source_nodes_dict: Dict[str, ChatNode]):
        """Recursively clones a node and its children from source_nodes_dict to self.nodes."""
        if old_node_id not in source_nodes_dict:
            return

        node_to_copy = source_nodes_dict[old_node_id]
        new_id = str(uuid.uuid4())[:8]
        
        # Create new node
        new_node = ChatNode(
            id=new_id,
            role=node_to_copy.role,
            content=node_to_copy.content,
            parent_id=new_parent_id,
            children_ids=[],
            timestamp=node_to_copy.timestamp,
            tokens=node_to_copy.tokens,
            cost=node_to_copy.cost,
            is_grafted=True
        )
        self.nodes[new_id] = new_node

        # Update parent's children list
        if new_parent_id in self.nodes:
            parent = self.nodes[new_parent_id]
            if new_id not in parent.children_ids:
                 parent.children_ids = parent.children_ids + [new_id]
                 self.nodes[new_parent_id] = parent

        # Recurse for children
        for child_id in node_to_copy.children_ids:
            self._clone_subtree_recursive(child_id, new_id, source_nodes_dict)
    
    # --- Tree Operations ---
    
    def set_selected_model_key(self, key: str):
        self.selected_model_key = key
        
    def add_node(self, role: str, content: str, parent_id: str, tokens: int = 0, cost: float = 0.0, model: str = None) -> str:
        # Normalize LaTeX delimiters for Reflex/Remark compatibility
        # \[ ... \] -> $$ ... $$
        # \( ... \) -> $ ... $
        if content:
            content = content.replace("\\[", "$$").replace("\\]", "$$")
            content = content.replace("\\(", "$").replace("\\)", "$")

        new_node = ChatNode.create(role=role, content=content, parent_id=parent_id, tokens=tokens, cost=cost, model=model)
        
        # We must treat self.nodes as immutable-like to trigger updates reliably in some contexts
        # or at least make sure the dict reference updates if Reflex checks that.
        # Ideally, just updating the key should work, but for nested structures, deep reactivity can be tricky.
        
        # Link to parent
        if parent_id in self.nodes:
            parent = self.nodes[parent_id]
            # Create a new instance
            parent_dict = parent.dict()
            parent_dict["children_ids"] = parent_dict["children_ids"] + [new_node.id]
            updated_parent = ChatNode(**parent_dict)
            
            # Update dictionary
            self.nodes[parent_id] = updated_parent
            
        self.nodes[new_node.id] = new_node
        
        # FORCE Reactivity: Reassign the dict to itself to trigger @rx.var dependencies
        self.nodes = {**self.nodes} 

        # Autosave if logged in
            
        # Autosave if logged in
        if self.user:
            database.save_conversation(self.user["email"], self.nodes, self.root_id)
            
        return new_node.id
    
    def delete_node_action(self, node_id: str):
        """Deletes a node and its descendants."""
        # Cannot delete root
        if node_id == self.root_id:
            return
            
        # Recursive delete
        to_delete = [node_id]
        i = 0
        while i < len(to_delete):
            curr_id = to_delete[i]
            if curr_id in self.nodes:
                to_delete.extend(self.nodes[curr_id].children_ids)
            i += 1
            
        # Remove from parent
        node = self.nodes.get(node_id)
        if node and node.parent_id and node.parent_id in self.nodes:
            parent = self.nodes[node.parent_id]
            parent.children_ids = [cid for cid in parent.children_ids if cid != node_id]
            self.nodes[node.parent_id] = parent
            
            # If we deleted the current path, move up
            if self.current_node_id in to_delete:
                self.current_node_id = node.parent_id
 
        # Delete from dict
        for nid in to_delete:
            if nid in self.nodes:
                del self.nodes[nid]

    def select_node(self, node_id: str):
        if node_id in self.nodes:
            self.current_node_id = node_id
            self.show_full_history = False # Default fold on switch
            
            # If we selected a User node, try to auto-select its Model response
            # so the answer is visible in the chat
            node = self.nodes[node_id]
            if node.role == "user" and node.children_ids:
                # Find first model child
                for cid in node.children_ids:
                     if cid in self.nodes and self.nodes[cid].role == "model":
                         self.current_node_id = cid
                         break

    # --- Chat Logic ---
    
    async def process_chat(self, form_data: dict):
        """Handle new user message."""
        user_text = form_data.get("chat_input", "").strip()
        if not user_text:
            return
            
        self.processing = True
        yield
        
        # 1. Add User Node
        user_node_id = self.add_node("user", user_text, self.current_node_id)
        self.current_node_id = user_node_id
        yield
        
        # 2. Generate Response
        await self._generate_model_response()
        yield

    async def regenerate_response(self, node_id: str):
        """Regenerate answer for a given User node."""
        if node_id not in self.nodes: return
        
        # Set context to this user node
        self.current_node_id = node_id
        self.processing = True
        yield
        
        # Generate new sibling response
        await self._generate_model_response()
        yield
             
    async def share_response(self, node_id: str):
        """Share the answer associated with this user node (User + Answer)."""
        if node_id not in self.nodes: return
        node = self.nodes[node_id]
        if node.role != "user": return
        
        # Find the Model response (child) that is currently active or first available
        # Ideally, we find the one that is currently displayed.
        # But simply getting the first model child is a reasonable default for MVP.
        answer_text = ""
        for cid in node.children_ids:
             if cid in self.nodes and self.nodes[cid].role == "model":
                 answer_text = self.nodes[cid].content
                 break
        
        if not answer_text:
            return rx.window_alert("No answer to share yet.")
            
        text_to_copy = f"Q: {node.content}\n\nA: {answer_text}"
        return rx.set_clipboard(text_to_copy)

    async def _generate_model_response(self):
        """Internal method to generate model response based on current_node_id."""
        user_node_id = self.current_node_id
        
        try:
            model_info = config.MODELS[self.selected_model_key]
            provider = model_info.get("provider", "google")
            model_id = model_info["id"]
            
            # Build History (Standard format)
            full_history = self.get_history_list(user_node_id)
            
            model_text = ""
            total_toks = 0
            total_step_cost = 0.0
            
            if provider == "openai":
                if not self.openai_api_key:
                    raise Exception("OpenAI API Key not set.")
                
                client = openai.AsyncOpenAI(api_key=self.openai_api_key)
                msgs = [{"role": "system", "content": "You are a helpful assistant."}]
                for item in full_history:
                    if item["role"] != "system":
                         role = "user" if item["role"] == "user" else "assistant"
                         msgs.append({"role": role, "content": item["content"]})
                
                # Internal mapping removed at user request.
                # Direct call to the ID specified in config.
                api_model_id = model_id
                
                if "o1" in api_model_id or "gpt-5" in api_model_id:
                     response = await client.chat.completions.create(
                        model=api_model_id,
                        messages=msgs
                        # No temperature
                    )
                else:
                    response = await client.chat.completions.create(
                        model=api_model_id,
                        messages=msgs,
                        temperature=self.temperature
                    )
                model_text = response.choices[0].message.content
                if response.usage:
                     prompt_toks = response.usage.prompt_tokens
                     cand_toks = response.usage.completion_tokens
                     total_toks = response.usage.total_tokens
                     pricing = model_info["pricing"]
                     total_step_cost = (prompt_toks/1e6 * pricing["INPUT_PER_1M"]) + (cand_toks/1e6 * pricing["OUTPUT_PER_1M"])
                     self.update_stats(total_step_cost, total_toks)

            elif provider == "anthropic":
                if not self.anthropic_api_key:
                    raise Exception("Anthropic API Key not set.")
                
                client = anthropic.AsyncAnthropic(api_key=self.anthropic_api_key)
                msgs = []
                for item in full_history:
                    if item["role"] != "system": # Claude system prompt is separate
                         role = "user" if item["role"] == "user" else "assistant"
                         msgs.append({"role": role, "content": item["content"]})
                
                response = await client.messages.create(
                    model=model_id,
                    max_tokens=1024,
                    temperature=self.temperature,
                    messages=msgs,
                    system="You are a helpful assistant."
                )
                model_text = response.content[0].text
                
                if response.usage:
                    input_toks = response.usage.input_tokens
                    output_toks = response.usage.output_tokens
                    total_toks = input_toks + output_toks
                    pricing = model_info["pricing"]
                    total_step_cost = (input_toks/1e6 * pricing["INPUT_PER_1M"]) + (output_toks/1e6 * pricing["OUTPUT_PER_1M"])
                    self.update_stats(total_step_cost, total_toks)

            elif provider == "google": # Google Gemini
                if not self.google_api_key:
                     raise Exception("Google API Key not set.")

                # Use async client
                client = Client(api_key=self.google_api_key)
                
                contents = []
                for item in full_history:
                    if item["role"] == "user":
                        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=item["content"])]))
                    elif item["role"] == "model":
                        contents.append(types.Content(role="model", parts=[types.Part.from_text(text=item["content"])]))
                
                # Configure safe defaults if temperature not supported
                config_kwargs = {}
                if model_id != "gemini-2.0-flash-exp": 
                     # 2.0 Flash might have strict temp rules, but usually google is fine.
                     # If issue persists, we can remove it.
                     if self.temperature != 1.0: # Only send if non-default?
                          pass # Actually, just send it. If 2.0 complains, we act.
                
                # Using aio for async
                response = await client.aio.models.generate_content(
                    model=model_id,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        temperature=self.temperature
                    )
                )
                
                model_text = response.text
                
                if response.usage_metadata:
                    prompt_toks = response.usage_metadata.prompt_token_count
                    cand_toks = response.usage_metadata.candidates_token_count
                    total_toks = response.usage_metadata.total_token_count
                    pricing = model_info["pricing"]
                    total_step_cost = (prompt_toks/1e6 * pricing["INPUT_PER_1M"]) + (cand_toks/1e6 * pricing["OUTPUT_PER_1M"])
                    self.update_stats(total_step_cost, total_toks)
            
            # 3. Add Model Node (with stats)
            model_node_id = self.add_node(
                "model",
                model_text,
                self.current_node_id,
                tokens=total_toks,
                cost=total_step_cost,
                model=self.selected_model_key # Save model name
            )
            self.current_node_id = model_node_id
            
        except Exception as e:
            print(f"GenAI Error: {e}")
            # Add error node?
            self.add_node("model", f"Error: {str(e)}", self.current_node_id)
            
        self.processing = False

    # --- Computed Props ---
    
    # --- Folding State ---
    collapsed_nodes: List[str] = []

    def toggle_node_collapse(self, node_id: str):
        if node_id in self.collapsed_nodes:
            self.collapsed_nodes.remove(node_id)
        else:
            self.collapsed_nodes.append(node_id)

    @rx.var(cache=True)
    def flat_tree(self) -> List[Dict[str, Any]]:
        """Returns a flattened list of nodes for rendering with indentation."""
        items = []
        if not self.root_id or self.root_id not in self.nodes:
            return items

        def traverse(node_id, level=0, label_prefix=""):
            if node_id not in self.nodes: return
            node = self.nodes[node_id]
            
            # DEBUG
            # print(f"Traversing {node.id} ({node.role}). Children: {len(node.children_ids)}")

            # Determine folding state
            # Check for VISIBLE children (exclude model/system)
            visible_children = []
            for cid in node.children_ids:
                if cid in self.nodes:
                    child_role = self.nodes[cid].role
                    if child_role != "model" and child_role != "system":
                        visible_children.append(cid)
            
            has_children = len(visible_children) > 0
            is_collapsed = node_id in self.collapsed_nodes
            
            # Determine if we show this node
            # Hide model nodes and system nodes from the tree view
            if node.role != "model" and node.role != "system":
                items.append({
                    "id": node.id,
                    "role": node.role,
                    "content": node.content,
                    "indent": level,
                    "index_label": label_prefix,
                    "is_grafted": node.is_grafted,
                    "is_selected": (node.id == self.current_node_id) or self._is_active_model_parent(node.id),
                    "has_children": has_children,
                    "is_collapsed": is_collapsed
                })
            
            # Skip children if collapsed
            if is_collapsed:
                return

            # Traverse children
            child_idx = 1
            for cid in node.children_ids:
                if cid not in self.nodes: continue
                child_node = self.nodes[cid]
                
                # Calculate prefix & level
                next_level = level
                current_prefix = ""
                
                if child_node.role == "user":
                    next_level = level + 1
                    if label_prefix:
                        current_prefix = f"{label_prefix}.{child_idx}"
                    else:
                        current_prefix = f"{child_idx}"
                    child_idx += 1
                else:
                    next_level = level
                    current_prefix = label_prefix 
                
                traverse(cid, next_level, current_prefix)
        
        # print("--- Starting Flat Tree Rebuild ---")
        traverse(self.root_id)
        # print(f"--- Rebuild Complete. Items: {len(items)} ---")
        return items

    def _is_active_model_parent(self, node_id: str) -> bool:
        """Helper to check if this node is the User parent of the currently active Model response"""
        if not self.current_node_id: return False
        curr = self.nodes.get(self.current_node_id)
        # If current active node is MODEL, its PARENT (User) should be highlighted
        if curr and curr.role == "model" and curr.parent_id == node_id:
            return True
        return False

    @rx.var
    def chat_history(self) -> List[Dict[str, str]]:
        """Returns the list of messages for the current view."""
        return self.get_history_list(self.current_node_id)

    def get_history_list(self, target_id: str) -> List[Dict[str, str]]:
        history = []
        curr = target_id
        print(f"DEBUG: Building history for {target_id}")
        while curr and curr in self.nodes:
            node = self.nodes[curr]
            print(f"DEBUG: Visiting {node.id} ({node.role}) -> Parent: {node.parent_id}")
            history.insert(0, {
                "id": node.id,
                "role": node.role,
                "content": node.content,
                "timestamp": node.timestamp,
                "tokens": node.tokens,
                "cost": node.cost,
                "model": node.model or "" # Handle None
            })
            curr = node.parent_id
        print(f"DEBUG: Final history length: {len(history)}")
        return history
        
    @rx.var
    def displayed_messages(self) -> List[Dict[str, str]]:
        """Handles folding logic for display."""
        hist = self.chat_history
        if not hist: return []
        
        # Filter out system
        visible = [h for h in hist if h["role"] != "system"]
        
        if not self.show_full_history and len(visible) > 1:
            # Show last Q&A pair (or last message if User)
            last = visible[-1]
            if last["role"] == "model":
                return visible[-2:]
            else:
                return [last]
        return visible

    def toggle_history(self):
        self.show_full_history = not self.show_full_history



    # --- Stats ---
    session_cost: float = 0.0
    session_tokens: int = 0
    
    def update_stats(self, cost: float, tokens: int):
        # Update Session Stats (Always)
        self.session_cost += cost
        self.session_tokens += tokens
        
        if self.user:
            # Update local state
            current_cost = float(self.user.get("total_cost", 0.0))
            current_tokens = int(self.user.get("total_tokens", 0))
            
            self.user["total_cost"] = current_cost + cost
            self.user["total_tokens"] = current_tokens + tokens
            
            # Update DB
            database.update_user_stats(self.user["email"], cost, tokens)

