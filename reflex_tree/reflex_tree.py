import reflex as rx
from . import state, config
from reflex.components.radix.themes.layout.box import Box

class DraggableBox(Box):
    def get_event_triggers(self):
        triggers = super().get_event_triggers()
        triggers.update({"on_drag_start": lambda e0: [e0]})
        return triggers

class DroppableBox(Box):
    def get_event_triggers(self):
        triggers = super().get_event_triggers()
        triggers.update({
            "on_drop": lambda e0: [e0],
            "on_drag_over": lambda e0: [e0]
        })
        return triggers

# --- COMPONENTS ---

def tree_row(node: dict):
    """Row component for flattened tree."""
    # node is a Var (Any) from the list check type
    node = node.to(dict)
    
    # is_active = (state.State.current_node_id == node["id"].to(str)) # Deprecated
    is_selected = node["is_selected"].to(bool)
    indent = node["indent"].to(int)
    
    return rx.context_menu.root(
        rx.context_menu.trigger(
            DroppableBox.create(
                DraggableBox.create(
                    rx.box(
                        rx.hstack(
                            # Fold Arrow
                            rx.cond(
                                node["has_children"].to(bool),
                                rx.icon(
                                    "chevron-right", 
                                    size=16, 
                                    on_click=lambda: state.State.toggle_node_collapse(node["id"].to(str)),
                                    transform=rx.cond(node["is_collapsed"].to(bool), "rotate(0deg)", "rotate(90deg)"),
                                    cursor="pointer",
                                    margin_right="4px"
                                ),
                                rx.box(width="20px") # Spacer for alignment
                            ),
                            # Label
                            rx.cond(
                                node["role"].to(str) == "model",
                                rx.text(f"A: {node['content'].to_string()[:30]}...", color="purple"),
                                rx.hstack(
                                    rx.cond(
                                        node["index_label"].to(str) != "",
                                        rx.text(node["index_label"].to(str), font_weight="bold", color="gray", margin_right="4px"),
                                    ),
                                    rx.text(f"{node['content'].to(str)[:30]}...", color="green")
                                )
                            ),
                            rx.cond(
                                is_selected,
                                rx.text("📌", font_size="14px", margin_left="auto"),
                            )
                        ),
                        padding_y="4px",
                        padding_right="8px",
                        # Indentation logic
                        padding_left=f"{indent * 1}rem", 
                        border_radius="4px",
                        width="100%",
                        bg=rx.cond(
                            is_selected, 
                            rx.color("accent", 3), 
                            rx.cond(
                                node["is_grafted"].to(bool),
                                rx.color("green", 3), # Light green for grafted
                                "transparent"
                            )
                        ),
                        _hover={"bg": rx.color("gray", 3)},
                    ),
                    draggable=True,
                    on_drag_start=lambda: state.State.set_dragged_node_id(node["id"].to(str)),
                    on_click=lambda: state.State.select_node(node["id"].to(str)),
                    cursor="pointer",
                    width="100%"
                ),
                on_drop=lambda: state.State.graft_conversation(node["id"].to(str)),
                on_drag_over=rx.prevent_default,
                width="100%"
            )
        ),
        rx.context_menu.content(
             rx.context_menu.item(
                 "Delete",
                 on_click=lambda: state.State.delete_node_action(node["id"].to(str)),
                 color="red"
             )
        )
    )

def login_modal():
    return rx.dialog.root(
        rx.dialog.content(
             rx.dialog.title(
                 rx.cond(state.State.is_signup_mode, "Sign Up", "Sign In")
             ),
             rx.dialog.description(
                 rx.cond(state.State.is_signup_mode, "Create a new account to save your chats and API keys.", "Enter your credentials to access your account."),
             ),
             rx.vstack(
                 rx.input(placeholder="Email", on_change=state.State.set_auth_email, value=state.State.auth_email),
                 rx.input(placeholder="Password", type="password", on_change=state.State.set_auth_password, value=state.State.auth_password),
                 rx.cond(
                     state.State.is_signup_mode,
                     rx.button("Sign Up", on_click=state.State.signup, width="100%"),
                     rx.button("Log In", on_click=state.State.login, width="100%")
                 ),
                 rx.text(
                     rx.cond(state.State.is_signup_mode, "Already have an account? ", "Don't have an account? "),
                     rx.link(
                         rx.cond(state.State.is_signup_mode, "Sign In", "Sign Up"), 
                         on_click=state.State.toggle_auth_mode
                     ),
                     size="1"
                 ),
                 spacing="3",
                 margin_top="4"
             ),
             rx.dialog.close(
                 rx.button("Close", size="1", color="gray", variant="soft", margin_top="4"),
             ),
        ),
        open=state.State.show_login,
        on_open_change=state.State.toggle_login_modal,
    )

def settings_modal():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("API Settings"),
            rx.dialog.description("Keys are stored only in this browser and are not saved on the server."),
            rx.vstack(
                rx.checkbox(
                    "Remember keys on this device",
                    checked=state.State.remember_keys_enabled,
                    on_change=state.State.set_remember_keys,
                ),
                rx.vstack(
                    rx.text("OpenAI", size="2", weight="bold"),
                    rx.input(
                        placeholder="OpenAI API Key (sk-...)",
                        type="password",
                        on_change=state.State.set_openai_api_key,
                        value=state.State.openai_api_key_value,
                        width="100%"
                    ),
                    spacing="2",
                    width="100%"
                ),
                rx.vstack(
                    rx.text("Claude (Anthropic)", size="2", weight="bold"),
                    rx.input(
                        placeholder="Anthropic API Key (sk-ant...)",
                        type="password",
                        on_change=state.State.set_anthropic_api_key,
                        value=state.State.anthropic_api_key_value,
                        width="100%"
                    ),
                    spacing="2",
                    width="100%"
                ),
                rx.vstack(
                    rx.text("Gemini (Google)", size="2", weight="bold"),
                    rx.input(
                        placeholder="Google API Key",
                        type="password",
                        on_change=state.State.set_google_api_key,
                        value=state.State.google_api_key_value,
                        width="100%"
                    ),
                    spacing="2",
                    width="100%"
                ),
                rx.vstack(
                    rx.text("Tavily (Deep Search)", size="2", weight="bold"),
                    rx.input(
                        placeholder="TAVILY_API_KEY",
                        type="password",
                        on_change=state.State.set_search_api_key,
                        value=state.State.search_api_key_value,
                        width="100%"
                    ),
                    spacing="2",
                    width="100%"
                ),
                spacing="4",
                width="100%",
                margin_top="4"
            ),
            rx.dialog.close(
                rx.button("Close", size="1", color="gray", variant="soft", margin_top="4"),
            ),
            rx.button("Save", size="1", margin_top="3", on_click=state.State.save_api_keys),
        ),
        open=state.State.show_settings,
        on_open_change=state.State.toggle_settings_modal,
    )

def sidebar():
    return rx.vstack(
        rx.hstack(
            rx.heading("Conversation Tree", size="3"),
            rx.spacer(),
            rx.color_mode.button(size="1"),
            width="100%",
            align_items="center"
        ),
        rx.divider(margin_y="4"),
        rx.select(
           list(config.MODELS.keys()),
           value=state.State.selected_model_key,
           on_change=state.State.set_selected_model_key,
           width="100%"
        ),
        rx.button("API Settings", on_click=state.State.toggle_settings_modal, size="1", variant="outline", width="100%"),
        settings_modal(),
        # Usage Stats Moved to Bottom
        rx.divider(margin_bottom="4"),
        # Stats Block removed from here
        rx.hstack(
            rx.icon("search", size=16, color="gray"),
            rx.input(
                placeholder="Search",
                on_change=state.State.set_history_search_query,
                value=state.State.history_search_query,
                width="100%"
            ),
            align="center",
            width="100%",
            padding="2",
            bg=rx.color("gray", 2),
            border_radius="4px",
        ),
        rx.button("➕ New Topic", on_click=state.State.add_new_topic, width="100%"),
        rx.cond(
            state.State.user,
            rx.vstack(
                rx.hstack(
                    rx.text("History", size="2", weight="bold"),
                    rx.spacer(),
                    rx.button(
                        rx.cond(state.State.show_history_panel, "▼", "▶"),
                        on_click=state.State.toggle_history_panel,
                        size="1",
                        variant="ghost",
                    ),
                    width="100%",
                    align="center",
                    margin_top="4"
                ),
                rx.cond(
                    state.State.show_history_panel,
                    rx.scroll_area(
                        rx.vstack(
                            rx.foreach(
                                state.State.chat_groups,
                                lambda group: rx.vstack(
                                    rx.text(
                                        group.date,
                                        size="1",
                                        weight="bold",
                                        color="gray",
                                        margin_top="2",
                                    ),
                                    rx.foreach(
                                        group.chats,
                                        lambda chat: rx.vstack(
                                            rx.context_menu.root(
                                                rx.context_menu.trigger(
                                                    rx.box(
                                                        DraggableBox.create(
                                                            rx.button(
                                                                chat["title"],
                                                                on_click=lambda: state.State.load_chat(chat["id"].to(str)),
                                                                variant="ghost",
                                                                width="100%",
                                                                justify_content="start",
                                                                font_size="14px",
                                                                color=rx.cond(
                                                                    chat["id"] == state.State.active_chat_id,
                                                                    "green",
                                                                    "gray",
                                                                ),
                                                                font_weight=rx.cond(
                                                                    chat["id"] == state.State.active_chat_id,
                                                                    "bold",
                                                                    "normal",
                                                                ),
                                                            ),
                                                            draggable=True,
                                                            on_drag_start=lambda: state.State.set_dragged_chat_id(chat["id"].to(str)),
                                                            width="100%"
                                                        ),
                                                        width="100%",
                                                    ),
                                                ),
                                                rx.context_menu.content(
                                                    rx.context_menu.item(
                                                        "Delete",
                                                        on_click=lambda: state.State.delete_chat(chat["id"]),
                                                        color="red",
                                                    ),
                                                ),
                                            ),
                                            rx.cond(
                                                chat["id"] == state.State.active_chat_id,
                                                rx.box(
                                                    rx.vstack(
                                                        rx.foreach(
                                                            state.State.flat_tree.to(list),
                                                            tree_row
                                                        ),
                                                        spacing="0",
                                                        width="100%"
                                                    ),
                                                    width="100%",
                                                    padding_left="12px",
                                                    padding_y="1",
                                                ),
                                            ),
                                            spacing="1",
                                            width="100%",
                                            align_items="start",
                                        ),
                                    ),
                                    spacing="1",
                                    width="100%",
                                    align_items="start",
                                ),
                            ),
                            spacing="1"
                        ),
                        max_height="200px",
                        width="100%",
                    ),
                ),
                width="100%",
            )
        ),
        rx.cond(
            ~state.State.user,
            rx.vstack(
                rx.divider(),
                rx.vstack(
                    rx.foreach(
                        state.State.flat_tree.to(list),
                        tree_row
                    ),
                    spacing="0", # Tight spacing
                    width="100%"
                ),
            ),
        ),
        # Removed Spacer to eliminate gap
        rx.divider(margin_y="2"),
        rx.vstack(
            rx.hstack(
                rx.text("Token Usage & Cost", size="2", weight="bold"),
                rx.spacer(),
                rx.button(
                    rx.cond(state.State.show_usage_panel, "▼", "▶"),
                    on_click=state.State.toggle_usage_panel,
                    size="1",
                    variant="ghost",
                ),
                width="100%",
                align="center",
            ),
            rx.cond(
                state.State.show_usage_panel,
                rx.vstack(
                    rx.text("Session Usage", size="2", weight="bold"),
                    rx.hstack(
                        rx.text("Cost:", size="1", color="gray"),
                        rx.text(f"${state.State.session_cost}", size="1", weight="bold"),
                        justify="between",
                        width="100%"
                    ),
                    rx.hstack(
                        rx.text("Tokens:", size="1", color="gray"),
                        rx.text(f"{state.State.session_tokens}", size="1", weight="bold"),
                        justify="between",
                        width="100%"
                    ),
                    rx.cond(
                        state.State.user,
                        rx.vstack(
                            rx.divider(margin_y="2"),
                            rx.text("Daily Usage", size="2", weight="bold"),
                            rx.hstack(
                                rx.text("Cost:", size="1", color="gray"),
                                rx.text(f"${state.State.daily_cost}", size="1", weight="bold"),
                                justify="between",
                                width="100%"
                            ),
                            rx.hstack(
                                rx.text("Tokens:", size="1", color="gray"),
                                rx.text(f"{state.State.daily_tokens}", size="1", weight="bold"),
                                justify="between",
                                width="100%"
                            ),
                            rx.divider(margin_y="2"),
                            rx.text("Weekly Usage", size="2", weight="bold"),
                            rx.hstack(
                                rx.text("Cost:", size="1", color="gray"),
                                rx.text(f"${state.State.weekly_cost}", size="1", weight="bold"),
                                justify="between",
                                width="100%"
                            ),
                            rx.hstack(
                                rx.text("Tokens:", size="1", color="gray"),
                                rx.text(f"{state.State.weekly_tokens}", size="1", weight="bold"),
                                justify="between",
                                width="100%"
                            ),
                            rx.divider(margin_y="2"),
                            rx.text("Overall Usage", size="2", weight="bold"),
                            rx.hstack(
                                rx.text("Cost:", size="1", color="gray"),
                                rx.text(f"${state.State.user['total_cost']}", size="1", weight="bold"),
                                justify="between",
                                width="100%"
                            ),
                            rx.hstack(
                                rx.text("Tokens:", size="1", color="gray"),
                                rx.text(f"{state.State.user['total_tokens']}", size="1", weight="bold"),
                                justify="between",
                                width="100%"
                            ),
                            width="100%"
                        ),
                    ),
                    width="100%",
                ),
            ),
            width="100%",
            padding="2",
            bg=rx.color("gray", 2),
            border_radius="4px",
            margin_y="4"
        ),
        id="sidebar",
        data_min_width="250",
        data_max_percent="0.5",
        width="300px",
        min_width="250px",
        max_width="50%",
        height="100vh",
        padding="4",
        border_right=f"1px solid {rx.color('gray', 3)}",
        bg=rx.color("gray", 1),
        style={"overflow": "auto", "z_index": "10"}
    )

def chat_message(message: dict):
    return rx.box(
        rx.vstack(
            rx.cond(
                message["role"].to(str) == "user",
                # User Message Bubble
                rx.box(
                    rx.vstack(
                        rx.text(message["content"], white_space="pre-wrap"),
                        rx.hstack(
                           rx.tooltip(
                               rx.button(
                                   rx.icon("refresh-ccw", size=14), 
                                   on_click=lambda: state.State.regenerate_response(message["id"].to(str)),
                                   variant="ghost", 
                                   size="1", 
                                   padding="1"
                               ),
                               content="Regenerate Answer"
                           ),
                           rx.tooltip(
                               rx.button(
                                   rx.icon("share-2", size=14),
                                   on_click=lambda: state.State.share_response(message["id"].to(str)),
                                   variant="ghost",
                                   size="1",
                                   padding="1"
                               ),
                               content="Copy Q&A to Clipboard"
                           ),
                           # align="end",
                           justify="end",
                           width="100%",
                           spacing="1",
                           padding_right="20px"
                        ),
                        width="100%"
                    ),
                    bg=rx.color("gray", 3),
                    padding="2",
                    border_radius="8px",
                    width="100%" 
                ),
                # Model Message Bubble
                rx.box( 
                    rx.vstack(
                        # Model Badge
                        rx.cond(
                            message["model"].to(str) != "", 
                            rx.badge(message["model"], color_scheme="purple", variant="soft", margin_bottom="2px"),
                        ),
                        # Content
                        rx.markdown(message["content"], math_jax=True),
                        # Stats Footer
                        rx.hstack(
                            rx.text("Tokens: " + message["tokens"].to(str), size="1", color="gray"),
                            rx.text("|", size="1", color="gray"),
                            rx.text("Cost: $" + message["cost"].to(str), size="1", color="gray"),
                            margin_top="2",
                            spacing="2"
                        ),
                        align_items="start",
                        spacing="1",
                        width="100%"
                    ),
                    bg=rx.color("accent", 3),
                    padding="2",
                    border_radius="8px",
                    width="100%"
                )
            ),
            align_items="start",
            spacing="2", # Spacing between bubble and whatever else, or just internal structural spacing
            width="100%"
        ),
        padding_y="2", # Vertical spacing between messages in the list
        width="100%"
    )

def chat_area():
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading("Chat", size="4"),
            rx.spacer(),
            # Cost Display Removed (Moved to Sidebar)

            # Auth Section (Moved from Sidebar)
            rx.cond(
                state.State.is_logged_in,
                rx.hstack(
                     rx.vstack(
                        rx.text(state.State.user["email"], size="1", weight="bold"),
                        rx.text("Logged In", size="1", color="green"),
                        spacing="0",
                        align_items="end"
                    ),
                    rx.avatar(fallback=state.State.user["email"].to(str)[0], size="2"),
                    rx.button("Log Out", on_click=state.State.logout, size="1", variant="ghost", color_scheme="red"),
                    align_items="center",
                    spacing="3"
                ),
                rx.button("Sign In / Sign Up", on_click=state.State.toggle_login_modal, size="2", variant="solid")
            ),
            login_modal(), # Include modal here
            width="100%",
            padding="4",
            border_bottom=f"1px solid {rx.color('gray', 3)}"
        ),
        
        # Messages
        rx.scroll_area(
            rx.vstack(
                rx.cond(
                    state.State.chat_history.length() > 3,
                    rx.button(
                        rx.cond(state.State.show_full_history, "Hide Previous Messages", "Show Previous Messages"),
                        on_click=state.State.toggle_history, 
                        variant="outline", 
                        width="100%"
                    )
                ),
                rx.foreach(
                    state.State.displayed_messages,
                    chat_message
                ),
                width="100%",
                padding="6"
            ),
            flex="1",
            width="100%"
        ),
        
        # Input
        rx.box(
            rx.form(
                rx.hstack(
                    rx.input(placeholder="Type a message...", id="chat_input", flex="1"),
                    rx.checkbox("Deep Search (Tavily)", checked=state.State.use_google_search, on_change=state.State.set_use_google_search),
                    rx.button("Send", type="submit", loading=state.State.processing),
                    align_items="center",
                    spacing="4"
                ),
                on_submit=state.State.process_chat,
                reset_on_submit=True
            ),
            padding="4",
            width="100%",

            border_top=f"1px solid {rx.color('gray', 3)}"
        ),
        height="100vh",
        flex="1",
        bg=rx.color("gray", 2)
    )

def index():
    return rx.hstack(
        sidebar(),
        rx.box(
            id="sidebar-resizer",
            width="6px",
            height="100vh",
            bg=rx.color("gray", 3),
            cursor="col-resize",
            _hover={"bg": rx.color("gray", 5)},
            flex_shrink="0",
        ),
        chat_area(),
        rx.el.script(
            """
(() => {
  if (window.__sidebarResizerInstalled) return;
  window.__sidebarResizerInstalled = true;

  const sidebar = document.getElementById("sidebar");
  const resizer = document.getElementById("sidebar-resizer");
  if (!sidebar || !resizer) return;

  const minWidth = parseInt(sidebar.dataset.minWidth || "250", 10);
  const maxPercent = parseFloat(sidebar.dataset.maxPercent || "0.5");
  let startX = 0;
  let startWidth = 0;

  const clampWidth = (width) => {
    const maxWidth = Math.floor(window.innerWidth * maxPercent);
    return Math.min(Math.max(width, minWidth), maxWidth);
  };

  const onMove = (event) => {
    const dx = event.clientX - startX;
    sidebar.style.width = `${clampWidth(startWidth + dx)}px`;
  };

  const stopDrag = () => {
    document.removeEventListener("pointermove", onMove);
    document.removeEventListener("pointerup", stopDrag);
    document.body.style.userSelect = "";
  };

  const startDrag = (event) => {
    if (!event.isPrimary) return;
    event.preventDefault();
    startX = event.clientX;
    startWidth = sidebar.getBoundingClientRect().width;
    document.body.style.userSelect = "none";
    document.addEventListener("pointermove", onMove);
    document.addEventListener("pointerup", stopDrag);
  };

  resizer.addEventListener("pointerdown", startDrag);
})();
            """
        ),
        spacing="0",
        height="100vh",
        width="100vw"
    )

# --- APP DEFINITION ---
app = rx.App(
    stylesheets=[
        "https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css",
    ],
    head_components=[
        rx.el.link(
            rel="icon",
            href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ctext y='50' font-size='50'%3E%F0%9F%8C%B3%3C/text%3E%3C/svg%3E",
        ),
        rx.el.link(
            rel="shortcut icon",
            href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ctext y='50' font-size='50'%3E%F0%9F%8C%B3%3C/text%3E%3C/svg%3E",
        ),
        rx.el.link(
            rel="apple-touch-icon",
            href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ctext y='50' font-size='50'%3E%F0%9F%8C%B3%3C/text%3E%3C/svg%3E",
        ),
        rx.el.link(
            rel="mask-icon",
            href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ctext y='50' font-size='50'%3E%F0%9F%8C%B3%3C/text%3E%3C/svg%3E",
            color="transparent",
        ),
    ],
)
app.add_page(index, on_load=state.State.on_load, title="Conversation Tree")
