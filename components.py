import streamlit as st
from utils import is_main_branch

def render_tree_sidebar(node, depth=0, is_last=True, prefix="", parent=None, sibling_index=0, root=None, skip_render=False):
    if node.role == "system":
        root_node = node
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            render_tree_sidebar(child, depth, is_last_child, "", node, i, root_node)
        return
    
    if skip_render:
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            render_tree_sidebar(child, depth + 1, is_last_child, "", node, i, root, skip_render=False)
        return
    
    if root is None: root = st.session_state.root
    
    model_child = None
    if node.role == "user" and node.children:
        for child in node.children:
            if child.role == "model":
                model_child = child
                break
    
    is_main = is_main_branch(node, depth, parent, sibling_index, root)
    branch_badge = "📌 main" if is_main else "🌿 branch"
    
    max_length = 30
    if model_child:
        q = node.content.replace('\n', ' ').strip()
        a = model_child.content.replace('\n', ' ').strip()
        combined_label = f"Q: {q[:max_length]}... | A: {a[:max_length]}..."
        is_active = (st.session_state.current_node.id == node.id or 
                     st.session_state.current_node.id == model_child.id)
        target_node = model_child
    else:
        l = node.content.replace('\n', ' ').strip()
        combined_label = f"{l[:max_length]}..."
        is_active = st.session_state.current_node.id == node.id
        target_node = node
    
    role_color = "#9C27B0" if model_child else ("#4285F4" if node.role == "model" else "#34A853")
    
    if is_active:
        st.markdown(f"""
        <div style="
            background-color: rgba(66, 133, 244, 0.1); 
            padding: 6px 8px; 
            border-radius: 6px; 
            border-left: 3px solid {role_color}; 
            margin: 2px 0;
            color: var(--text-color);
        ">
            <span style="font-size: 0.75em; opacity: 0.7;">{branch_badge}</span>
            <div style="font-size: 0.9em;">{combined_label}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.button(f"{branch_badge} {combined_label}", key=f"tree_btn_{target_node.id}", use_container_width=True, type="secondary"):
            st.session_state.current_node = target_node
            st.rerun()
    
    if model_child:
        for i, child in enumerate(model_child.children):
            render_tree_sidebar(child, depth + 1, i==len(model_child.children)-1, "", model_child, i, root, False)
    else:
        for i, child in enumerate(node.children):
            skip = (node.role == "user" and child.role == "model")
            render_tree_sidebar(child, depth + 1, i==len(node.children)-1, "", node, i, root, skip)

def inject_custom_js():
    st.markdown("""
    <script>
    (function() {
        'use strict';
        function init() {
            let selectedText = '';
            let lastSelectionTime = 0;
            
            document.addEventListener('mouseup', () => {
                 const txt = window.getSelection().toString().trim();
                 if(txt) { selectedText = txt; lastSelectionTime = Date.now(); window.lastSelectedText = txt; window.lastSelectionTime = lastSelectionTime; }
            }, true);
            
            document.addEventListener('keydown', function(e) {
                const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
                const modifier = isMac ? e.metaKey : e.ctrlKey;
                if (modifier && (e.key === 'Enter' || e.keyCode === 13)) {
                    let text = window.getSelection().toString().trim();
                    if (!text && window.lastSelectedText && (Date.now() - window.lastSelectionTime < 10000)) {
                        text = window.lastSelectedText;
                    }
                    if (text) {
                        e.preventDefault(); e.stopPropagation();
                        const url = window.location.href.split('?')[0] + '?branch_text=' + encodeURIComponent(text);
                        window.location.href = url;
                    }
                }
            }, true);
        }
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
        else init();
    })();
    </script>
    """, unsafe_allow_html=True)