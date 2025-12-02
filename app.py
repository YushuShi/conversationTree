import os
import streamlit as st
from google import genai
from google.genai import types
import uuid
from dotenv import load_dotenv

# streamlit run app.py

# --- CONFIGURATION ---
# Replace with your actual API Key or set it in your environment variables
# Get one here: https://aistudio.google.com/app/apikey
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_ID = "gemini-2.0-flash"

client = genai.Client(api_key=API_KEY)

# --- DATA STRUCTURES (The Logic) ---
class ChatNode:
    def __init__(self, role, content, parent=None):
        self.id = str(uuid.uuid4())[:8]  # Short unique ID
        self.role = role  # "user" or "model"
        self.content = content
        self.parent = parent
        self.children = []
        self.timestamp = str(uuid.uuid1()) # Simple sorting mechanism

    def add_child(self, node):
        self.children.append(node)
        return node

    def get_history(self):
        """Backtracks from this node to Root to build context."""
        history = []
        nodes = []  # Track nodes alongside history
        current = self
        while current:
            history.insert(0, types.Content(
                role=current.role,
                parts=[types.Part(text=current.content)]
            ))
            nodes.insert(0, current)  # Track corresponding node
            current = current.parent
        return history, nodes

# --- HELPER FUNCTIONS ---
def get_node_by_id(root, target_id):
    """Recursively find a node."""
    if root.id == target_id:
        return root
    for child in root.children:
        found = get_node_by_id(child, target_id)
        if found:
            return found
    return None

def is_main_branch(node, depth, parent=None, sibling_index=0, root=None):
    """Determine if this node is part of the main branch.
    
    Main branch = the most recently created branch from any given node.
    When a user goes back to a previous node and creates a new branch:
    - The new branch becomes "main"
    - Existing branches from that node become "branch"
    """
    # If no parent, this is root-level - check if it's the most recent root child
    if parent is None or parent.role == "system":
        if root:
            root_children = [n for n in root.children if n.role != "system"]
            if root_children:
                # Sort by timestamp to find most recent
                most_recent = max(root_children, key=lambda n: n.timestamp)
                return node == most_recent
        return True  # Default to main if we can't determine
    
    # Check if parent has multiple children
    if len(parent.children) > 1:
        # Find the most recent child of the parent (by timestamp)
        most_recent_sibling = max(parent.children, key=lambda n: n.timestamp)
        
        # If this node is the most recent child, it's main
        if node == most_recent_sibling:
            # Check if parent is also on main branch
            if parent.parent:
                # Recursively check parent
                parent_sibling_idx = parent.parent.children.index(parent) if parent in parent.parent.children else 0
                return is_main_branch(parent, depth - 1, parent.parent, parent_sibling_idx, root)
            else:
                # Parent is root-level
                if root:
                    root_children = [n for n in root.children if n.role != "system"]
                    if root_children:
                        most_recent_root = max(root_children, key=lambda n: n.timestamp)
                        return parent == most_recent_root
                return True
        else:
            # This is not the most recent child, so it's a branch
            return False
    
    # Parent has only one child - inherit parent's branch status
    if parent.parent:
        parent_sibling_idx = parent.parent.children.index(parent) if parent in parent.parent.children else 0
        return is_main_branch(parent, depth - 1, parent.parent, parent_sibling_idx, root)
    else:
        # Parent is root-level
        if root:
            root_children = [n for n in root.children if n.role != "system"]
            if root_children:
                most_recent_root = max(root_children, key=lambda n: n.timestamp)
                return parent == most_recent_root
        return True

def render_tree_sidebar(node, depth=0, is_last=True, prefix="", parent=None, sibling_index=0, root=None, skip_render=False):
    """Recursively draws the tree, combining question-answer pairs."""
    # Skip the root system node in display
    if node.role == "system":
        root_node = node  # Store root reference
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            render_tree_sidebar(child, depth, is_last_child, "", node, i, root_node)
        return
    
    # Skip rendering if this is a model node that's a direct child of a user node
    # (it will be rendered together with its parent user node)
    if skip_render:
        # Still need to render its children though
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            render_tree_sidebar(child, depth + 1, is_last_child, "", node, i, root, skip_render=False)
        return
    
    # Set root on first call if not provided
    if root is None:
        root = st.session_state.root
    
    # Check if this is a user node with a model child (question-answer pair)
    model_child = None
    if node.role == "user" and node.children:
        # Find the first model child (answer)
        for child in node.children:
            if child.role == "model":
                model_child = child
                break
    
    # Get branch label (main or branch) - use the user node for branch determination
    # since branching happens when a user asks a question from a previous node
    target_node_for_branch = node  # Always use the current node (user node if it's a pair)
    is_main = is_main_branch(target_node_for_branch, depth, parent, sibling_index, root)
    branch_badge = "📌 main" if is_main else "🌿 branch"
    
    # Truncate content for display
    max_length = 30
    
    # If we have a question-answer pair, combine them
    if model_child:
        question_label = node.content[:max_length] + '...' if len(node.content) > max_length else node.content
        answer_label = model_child.content[:max_length] + '...' if len(model_child.content) > max_length else model_child.content
        question_label = question_label.replace('\n', ' ').strip()
        answer_label = answer_label.replace('\n', ' ').strip()
        combined_label = f"Q: {question_label} | A: {answer_label}"
        
        # Check if either node is active
        is_active = (st.session_state.current_node.id == node.id or 
                    st.session_state.current_node.id == model_child.id)
        target_node_for_nav = model_child  # Navigate to the answer node
    else:
        # Single node (user or model without pair)
        label = node.content[:max_length] + '...' if len(node.content) > max_length else node.content
        label = label.replace('\n', ' ').strip()
        combined_label = label
        is_active = st.session_state.current_node.id == node.id
        target_node_for_nav = node
    
    # No connector symbols - just use spacing for indentation
    indent_spaces = "  " * depth  # 2 spaces per depth level
    
    # Always show branch label (main/branch) for clarity
    show_branch_label = True
    
    # Use combined icon and styling for question-answer pairs
    if model_child:
        role_color = "#9C27B0"  # Purple for pairs
    elif node.role == "model":
        role_color = "#4285F4"  # Google blue
    else:
        role_color = "#34A853"  # Google green
    
    # Style the node based on active state
    if is_active:
        # Active node styling
        branch_label_html = f'<span style="font-size: 0.75em; color: #666; margin-left: 8px;">{branch_badge}</span>' if show_branch_label else ""
        node_display = f"""
        <div style="
            background-color: #E8F0FE;
            padding: 6px 8px;
            border-radius: 6px;
            border-left: 3px solid {role_color};
            margin: 2px 0;
        ">
            <span style="color: {role_color}; font-weight: bold;">{branch_label_html}</span>
            <div style="margin-left: 20px; color: #333; font-size: 0.9em; margin-top: 4px;">{combined_label}</div>
        </div>
        """
        st.markdown(node_display, unsafe_allow_html=True)
    else:
        # Inactive node - make it clickable with better formatting
        button_key = f"tree_btn_{target_node_for_nav.id}"
        # Add branch label to button text if needed
        branch_label_text = f" {branch_badge}" if show_branch_label else ""
        button_text = f"{branch_label_text} {combined_label}"
        if st.button(
            button_text,
            key=button_key,
            use_container_width=True,
            type="secondary"
        ):
            st.session_state.current_node = target_node_for_nav
            st.rerun()
    
    # Render children
    # If we rendered a question-answer pair, skip the model child and render its children
    if model_child:
        # Render children of the model node (answer)
        for i, child in enumerate(model_child.children):
            is_last_child = (i == len(model_child.children) - 1)
            render_tree_sidebar(child, depth + 1, is_last_child, "", model_child, i, root, skip_render=False)
    else:
        # Render children normally
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            # Skip model children that are direct children of user nodes (they're already rendered)
            skip_child = (node.role == "user" and child.role == "model")
            render_tree_sidebar(child, depth + 1, is_last_child, "", node, i, root, skip_render=skip_child)

# --- MAIN APP ---
st.set_page_config(layout="wide", page_title="Gemini Tree Chat")

# 1. Initialize Session State
if "root" not in st.session_state:
    # Hidden root node to start the tree
    root_node = ChatNode("system", "Start of Conversation")
    st.session_state.root = root_node
    st.session_state.current_node = root_node
    st.session_state.pending_branch_text = None  # For Ctrl+Enter branch creation

# 2. Sidebar: The Tree & Tools
with st.sidebar:
    st.header("🌳 Conversation Tree")
    st.caption("Click any node to navigate to that point in the conversation.")
    
    # Add custom CSS for tree display
    st.markdown("""
    <style>
    .tree-node {
        font-family: 'Courier New', monospace;
        font-size: 0.85em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add some spacing and a container for the tree
    with st.container():
        render_tree_sidebar(st.session_state.root)
    
    # # Show current branch info
    # if st.session_state.current_node.role != "system":
    #     st.divider()
    #     history, history_nodes = st.session_state.current_node.get_history()
    #     branch_depth = len([n for n in history if n.role != "system"])
        
    #     # Count question-answer pairs in this branch
    #     qa_pairs = 0
    #     for i, node in enumerate(history_nodes):
    #         if node.role == "user":
    #             # A Q&A pair is a user node followed by its model child in the history
    #             if (
    #                 i + 1 < len(history_nodes)
    #                 and history_nodes[i + 1].role == "model"
    #                 and history_nodes[i + 1].parent == node
    #             ):
    #                 qa_pairs += 1
        
    #     num_children = len(st.session_state.current_node.children)
    #     info_text = f"📍 Branch: {branch_depth} messages | {qa_pairs} Q&A pair{'s' if qa_pairs != 1 else ''}"
    #     if num_children > 0:
    #         info_text += f" | {num_children} branch{'es' if num_children > 1 else ''}"
    #     st.caption(info_text)
    
    st.divider()
    
    # # --- HOTKEY INFO ---
    # st.info("""
    # 💡 **Hotkey:** Highlight text in AI responses and press **Ctrl+Enter** (or **Cmd+Enter** on Mac) to create a branch.
    
    # 🔍 **Debugging:** If the hotkey doesn't work, open your browser's Developer Console (F12 or Cmd+Option+I) and look for messages starting with `[Branch Handler]`. You can also use the manual branch creator below.
    # """)
    
    # # Manual branch creation fallback
    # with st.expander("🔀 Create Branch Manually", expanded=False):
    #     branch_text_input = st.text_input(
    #         "Enter text to explain:",
    #         key="manual_branch_text",
    #         placeholder="Paste or type text here..."
    #     )
    #     if st.button("Create Branch", key="manual_branch_btn"):
    #         if branch_text_input and branch_text_input.strip():
    #             # Trigger branch creation directly
    #             prompt = f"Please explain {branch_text_input.strip()}"
                
    #             # Add User Node to Tree (branching from current node)
    #             user_node = ChatNode("user", prompt, parent=st.session_state.current_node)
    #             st.session_state.current_node.add_child(user_node)
    #             st.session_state.current_node = user_node
                
    #             # Get AI Response
    #             with st.spinner("Gemini is thinking..."):
    #                 try:
    #                     full_context, _ = user_node.get_history()
    #                     api_messages = [m for m in full_context if m.role != "system"]
                        
    #                     response = client.models.generate_content(
    #                         model="gemini-2.0-flash",
    #                         contents=api_messages
    #                     )
    #                     ai_text = response.text
                        
    #                     ai_node = ChatNode("model", ai_text, parent=st.session_state.current_node)
    #                     st.session_state.current_node.add_child(ai_node)
    #                     st.session_state.current_node = ai_node
                        
    #                     st.rerun()
    #                 except Exception as e:
    #                     st.error(f"API Error: {e}")
    #         else:
    #             st.warning("Please enter some text to explain.")
    
    # st.divider()
    
    # --- MANUAL SEARCH TOOL (Option 2) ---
    st.header("🔍 Manual Search")
    st.caption("Search without affecting chat context.")
    search_query = st.text_input("Google Query")
    if st.button("Search Google"):
        # NOTE: This uses the Gemini 'Grounding' feature as a proxy for search
        # to avoid needing a separate Custom Search JSON API Key.
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=search_query,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    response_mime_type="text/plain"
                )
            )
            # We display the answer + the source links Gemini found
            st.info(response.text)
            if response.candidates[0].grounding_metadata.grounding_chunks:
                for chunk in response.candidates[0].grounding_metadata.grounding_chunks:
                     st.write(f"- [{chunk.web.title}]({chunk.web.uri})")
        except Exception as e:
            st.error(f"Search failed: {e}")

# 3. Main Chat Area
st.title("Gemini Tree Chat")

# Add JavaScript for text selection and Ctrl+Enter hotkey
# Using a more direct approach with inline script
st.markdown("""
<script>
(function() {
    'use strict';
    
    // Wait for DOM to be ready
    function init() {
        let selectedText = '';
        let lastSelectionTime = 0;
        
        console.log('[Branch Handler] Initialized');
        
        // Store selection when user selects text
        function storeSelection() {
            try {
                const selection = window.getSelection();
                const text = selection.toString().trim();
                if (text && text.length > 0) {
                    console.log('[Branch Handler] Text selected:', text.substring(0, 50));
                    selectedText = text;
                    lastSelectionTime = Date.now();
                    window.lastSelectedText = text;
                    window.lastSelectionTime = lastSelectionTime;
                }
            } catch (e) {
                console.error('[Branch Handler] Error storing selection:', e);
            }
        }
        
        // Listen for text selection
        document.addEventListener('mouseup', storeSelection, true);
        document.addEventListener('keyup', function(e) {
            if (e.shiftKey || e.ctrlKey || e.metaKey) {
                setTimeout(storeSelection, 10);
            }
        }, true);
        
        // Listen for Ctrl+Enter or Cmd+Enter
        document.addEventListener('keydown', function(e) {
            try {
                const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
                const modifier = isMac ? e.metaKey : e.ctrlKey;
                
                if (modifier && (e.key === 'Enter' || e.keyCode === 13)) {
                    console.log('[Branch Handler] Cmd/Ctrl+Enter detected');
                    
                    const selection = window.getSelection();
                    let text = selection.toString().trim();
                    
                    // If no current selection, use last selected text (if recent, within 10 seconds)
                    if (!text && window.lastSelectedText && window.lastSelectionTime) {
                        const timeDiff = Date.now() - window.lastSelectionTime;
                        if (timeDiff < 10000) {
                            text = window.lastSelectedText;
                            console.log('[Branch Handler] Using last selected text (age: ' + timeDiff + 'ms):', text.substring(0, 50));
                        }
                    }
                    
                    if (text && text.length > 0) {
                        console.log('[Branch Handler] Creating branch with:', text.substring(0, 50));
                        e.preventDefault();
                        e.stopPropagation();
                        
                        // Use URL parameter approach
                        try {
                            const currentUrl = window.location.href.split('?')[0];
                            const newUrl = currentUrl + '?branch_text=' + encodeURIComponent(text);
                            console.log('[Branch Handler] Navigating to:', newUrl.substring(0, 100));
                            window.location.href = newUrl;
                        } catch (err) {
                            console.error('[Branch Handler] Error setting URL:', err);
                            alert('Error creating branch. Please try selecting text and using the button in the sidebar.');
                        }
                    } else {
                        console.log('[Branch Handler] No text available for branch creation');
                    }
                }
            } catch (e) {
                console.error('[Branch Handler] Error in keydown handler:', e);
            }
        }, true);
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
</script>
""", unsafe_allow_html=True)

# Display History for Current Branch
history, history_nodes = st.session_state.current_node.get_history()

# Helper function to get branch label for a node
def get_node_branch_label(node, root):
    """Get branch label for a node in the chat display."""
    if node.role == "system":
        return None
    
    # Find node's depth and parent info
    depth = 0
    parent = node.parent
    actual_parent = parent  # Keep reference to actual parent
    
    # Calculate depth
    while parent and parent.role != "system":
        depth += 1
        parent = parent.parent
    
    # Get sibling index
    if actual_parent and actual_parent.role != "system":
        sibling_index = actual_parent.children.index(node) if node in actual_parent.children else 0
        parent_for_check = actual_parent
    else:
        # Root level
        root_children = [n for n in root.children if n.role != "system"]
        sibling_index = root_children.index(node) if node in root_children else 0
        parent_for_check = None
    
    # Determine if main or branch
    is_main = is_main_branch(node, depth, parent_for_check, sibling_index, root)
    
    # Always show label (main/branch) for clarity
    return "📌 main" if is_main else "🌿 branch"

for i, msg in enumerate(history):
    if msg.role != "system": # Hide the hidden root
        node = history_nodes[i] if i < len(history_nodes) else None
        branch_label = get_node_branch_label(node, st.session_state.root) if node else None
        
        with st.chat_message(msg.role):
            # Extract text from Part objects
            text_content = ""
            if msg.parts:
                for part in msg.parts:
                    if part.text:
                        text_content += part.text
            
            # Display with branch label if applicable
            if branch_label:
                st.markdown(f"{text_content} <span style='font-size: 0.85em; color: #666; margin-left: 8px;'>{branch_label}</span>", unsafe_allow_html=True)
            else:
                st.write(text_content)

# 4. Handle Branch Creation from Ctrl+Enter (via query parameter)
# Check if we need to process a branch creation from hotkey or manual button
if "branch_text" in st.query_params and "processed_branch" not in st.session_state:
    branch_text = st.query_params["branch_text"]
    # Mark as processed to avoid reprocessing on rerun
    st.session_state.processed_branch = branch_text
    
    # Clear the query parameter
    if "branch_text" in st.query_params:
        # Remove branch_text from query params
        params = dict(st.query_params)
        params.pop("branch_text", None)
        st.query_params.clear()
        for k, v in params.items():
            st.query_params[k] = v
    
    prompt = f"Please explain {branch_text}"
    
    # A. Display User Message
    with st.chat_message("user"):
        st.write(prompt)
    
    # B. Add User Node to Tree (branching from current node)
    user_node = ChatNode("user", prompt, parent=st.session_state.current_node)
    st.session_state.current_node.add_child(user_node)
    st.session_state.current_node = user_node  # Move pointer forward

    # C. Get AI Response
    with st.spinner("Gemini is thinking..."):
        try:
            # Send full history of THIS branch to Gemini
            full_context, _ = user_node.get_history()
            
            # Filter out 'system' role
            api_messages = [
                m for m in full_context if m.role != "system"
            ]

            response = client.models.generate_content(
                model=MODEL_ID,
                contents=api_messages
            )
            ai_text = response.text
            
            # D. Display & Save AI Node
            with st.chat_message("model"):
                st.write(ai_text)
            
            ai_node = ChatNode("model", ai_text, parent=st.session_state.current_node)
            st.session_state.current_node.add_child(ai_node)
            st.session_state.current_node = ai_node  # Move pointer forward
            
            # Clear the processed flag
            if "processed_branch" in st.session_state:
                del st.session_state.processed_branch
            
            st.rerun()  # Refresh to update sidebar tree

        except Exception as e:
            st.error(f"API Error: {e}")
            # Clear the processed flag on error too
            if "processed_branch" in st.session_state:
                del st.session_state.processed_branch

# Reset processed flag if query param is gone (user navigated away)
if "branch_text" not in st.query_params and "processed_branch" in st.session_state:
    del st.session_state.processed_branch

# 5. Chat Input
if prompt := st.chat_input("Type a message..."):
    # A. Display User Message
    with st.chat_message("user"):
        st.write(prompt)
    
    # B. Add User Node to Tree
    user_node = ChatNode("user", prompt, parent=st.session_state.current_node)
    st.session_state.current_node.add_child(user_node)
    st.session_state.current_node = user_node # Move pointer forward

    # C. Get AI Response
    with st.spinner("Gemini is thinking..."):
        try:
            # Send full history of THIS branch to Gemini
            full_context, _ = user_node.get_history()
            
            # Filter out 'system' role if model doesn't support it, or keep it.
            # Gemini usually prefers 'user'/'model'.
            api_messages = [
                m for m in full_context if m.role != "system"
            ]

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=api_messages
            )
            ai_text = response.text
            
            # D. Display & Save AI Node
            with st.chat_message("model"):
                st.write(ai_text)
            
            ai_node = ChatNode("model", ai_text, parent=st.session_state.current_node)
            st.session_state.current_node.add_child(ai_node)
            st.session_state.current_node = ai_node # Move pointer forward
            
            st.rerun() # Refresh to update sidebar tree

        except Exception as e:
            st.error(f"API Error: {e}")