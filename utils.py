import streamlit as st
import database

def track_usage(response, pricing_dict):
    try:
        if hasattr(response, 'usage_metadata'):
            usage = response.usage_metadata
            input_tokens = usage.prompt_token_count or 0
            output_tokens = usage.candidates_token_count or 0
            
            st.session_state.total_input_tokens += input_tokens
            st.session_state.total_output_tokens += output_tokens
            
            input_cost = (input_tokens / 1_000_000) * pricing_dict["INPUT_PER_1M"]
            output_cost = (output_tokens / 1_000_000) * pricing_dict["OUTPUT_PER_1M"]
            total_request_cost = input_cost + output_cost
            
            st.session_state.total_cost += total_request_cost
            
            if "user" in st.session_state and st.session_state.user:
                email = st.session_state.user["email"]
                database.update_user_cost(email, total_request_cost)
                new_total = database.get_user_cost(email)
                st.session_state.user["total_cost"] = new_total
    except Exception as e:
        print(f"Error tracking usage: {e}")

def get_node_by_id(root, target_id):
    if root.id == target_id: return root
    for child in root.children:
        found = get_node_by_id(child, target_id)
        if found: return found
    return None

def is_main_branch(node, depth, parent=None, sibling_index=0, root=None):
    if parent is None or parent.role == "system":
        if root:
            root_children = [n for n in root.children if n.role != "system"]
            if root_children:
                most_recent = max(root_children, key=lambda n: n.timestamp)
                return node == most_recent
        return True
    
    if len(parent.children) > 1:
        most_recent_sibling = max(parent.children, key=lambda n: n.timestamp)
        if node == most_recent_sibling:
            if parent.parent:
                parent_sibling_idx = parent.parent.children.index(parent) if parent in parent.parent.children else 0
                return is_main_branch(parent, depth - 1, parent.parent, parent_sibling_idx, root)
            else:
                if root:
                    root_children = [n for n in root.children if n.role != "system"]
                    if root_children:
                        most_recent_root = max(root_children, key=lambda n: n.timestamp)
                        return parent == most_recent_root
                return True
        else:
            return False
    
    if parent.parent:
        parent_sibling_idx = parent.parent.children.index(parent) if parent in parent.parent.children else 0
        return is_main_branch(parent, depth - 1, parent.parent, parent_sibling_idx, root)
    else:
        if root:
            root_children = [n for n in root.children if n.role != "system"]
            if root_children:
                most_recent_root = max(root_children, key=lambda n: n.timestamp)
                return parent == most_recent_root
        return True