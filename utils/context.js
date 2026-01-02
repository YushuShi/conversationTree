import { createContext, useContext, useMemo, useReducer, useState, createElement, useEffect } from "react"
import { applyDelta, ReflexEvent, hydrateClientStorage, useEventLoop, refs } from "$/utils/state"
import { jsx } from "@emotion/react";

export const initialState = {"reflex___state____state": {"is_hydrated_rx_state_": false, "router_rx_state_": {"session": {"client_token": "", "client_ip": "", "session_id": ""}, "headers": {"host": "", "origin": "", "upgrade": "", "connection": "", "cookie": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": "", "raw_headers": {}}, "page": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}, "url": "", "route_id": ""}}, "reflex___state____state.reflex___state____frontend_event_exception_state": {}, "reflex___state____state.reflex___state____on_load_internal_state": {}, "reflex___state____state.reflex___state____update_vars_internal_state": {}, "reflex___state____state.reflex_tree___state____state": {"active_generation_user_id_rx_state_": "", "anthropic_api_key_rx_state_": "", "auth_email_rx_state_": "", "auth_password_rx_state_": "", "canceled_generation_user_ids_rx_state_": [], "chat_groups_rx_state_": [], "chat_history_rx_state_": [], "chat_list_rx_state_": [], "collapsed_nodes_rx_state_": [], "current_api_key_rx_state_": "", "current_api_key_placeholder_rx_state_": "OpenAI API Key (sk-...)", "current_node_id_rx_state_": "", "daily_cost_rx_state_": 0.0, "daily_tokens_rx_state_": 0, "displayed_messages_rx_state_": [], "dragged_chat_id_rx_state_": "", "dragged_node_id_rx_state_": "", "flat_tree_rx_state_": [], "generation_seed_rx_state_": 42, "google_api_key_rx_state_": "", "google_model_status_rx_state_": "", "guest_keys_saved_rx_state_": "False", "has_any_api_key_rx_state_": false, "is_logged_in_rx_state_": false, "is_signup_mode_rx_state_": false, "nodes_rx_state_": {}, "openai_api_key_rx_state_": "", "processing_rx_state_": false, "root_id_rx_state_": "", "search_api_key_rx_state_": "", "selected_model_key_rx_state_": "ChatGPT (GPT-5.2)", "selected_provider_rx_state_": "openai", "session_cost_rx_state_": 0.0, "session_tokens_rx_state_": 0, "show_full_history_rx_state_": false, "show_login_rx_state_": false, "show_settings_rx_state_": false, "temperature_rx_state_": 0.7, "use_deep_search_rx_state_": false, "user_rx_state_": null, "validated_google_model_ids_rx_state_": [], "weekly_cost_rx_state_": 0.0, "weekly_tokens_rx_state_": 0}}

export const defaultColorMode = "system"
export const ColorModeContext = createContext(null);
export const UploadFilesContext = createContext(null);
export const DispatchContext = createContext(null);
export const StateContexts = {reflex___state____state: createContext(null),reflex___state____state__reflex___state____frontend_event_exception_state: createContext(null),reflex___state____state__reflex___state____on_load_internal_state: createContext(null),reflex___state____state__reflex___state____update_vars_internal_state: createContext(null),reflex___state____state__reflex_tree___state____state: createContext(null),};
export const EventLoopContext = createContext(null);
export const clientStorage = {"cookies": {}, "local_storage": {"reflex___state____state.reflex_tree___state____state.guest_keys_saved_rx_state_": {"sync": false}, "reflex___state____state.reflex_tree___state____state.openai_api_key_rx_state_": {"sync": false}, "reflex___state____state.reflex_tree___state____state.anthropic_api_key_rx_state_": {"sync": false}, "reflex___state____state.reflex_tree___state____state.google_api_key_rx_state_": {"sync": false}, "reflex___state____state.reflex_tree___state____state.search_api_key_rx_state_": {"sync": false}}, "session_storage": {}}


export const state_name = "reflex___state____state"

export const exception_state_name = "reflex___state____state.reflex___state____frontend_event_exception_state"

// These events are triggered on initial load and each page navigation.
export const onLoadInternalEvent = () => {
    const internal_events = [];

    // Get tracked cookie and local storage vars to send to the backend.
    const client_storage_vars = hydrateClientStorage(clientStorage);
    // But only send the vars if any are actually set in the browser.
    if (client_storage_vars && Object.keys(client_storage_vars).length !== 0) {
        internal_events.push(
            ReflexEvent(
                'reflex___state____state.reflex___state____update_vars_internal_state.update_vars_internal',
                {vars: client_storage_vars},
            ),
        );
    }

    // `on_load_internal` triggers the correct on_load event(s) for the current page.
    // If the page does not define any on_load event, this will just set `is_hydrated = true`.
    internal_events.push(ReflexEvent('reflex___state____state.reflex___state____on_load_internal_state.on_load_internal'));

    return internal_events;
}

// The following events are sent when the websocket connects or reconnects.
export const initialEvents = () => [
    ReflexEvent('reflex___state____state.hydrate'),
    ...onLoadInternalEvent()
]
    

export const isDevMode = true;

export function UploadFilesProvider({ children }) {
  const [filesById, setFilesById] = useState({})
  refs["__clear_selected_files"] = (id) => setFilesById(filesById => {
    const newFilesById = {...filesById}
    delete newFilesById[id]
    return newFilesById
  })
  return createElement(
    UploadFilesContext.Provider,
    { value: [filesById, setFilesById] },
    children
  );
}

export function ClientSide(component) {
  return ({ children, ...props }) => {
    const [Component, setComponent] = useState(null);
    useEffect(() => {
      async function load() {
        const comp = await component();
        setComponent(() => comp);
      }
      load();
    }, []);
    return Component ? jsx(Component, props, children) : null;
  };
}

export function EventLoopProvider({ children }) {
  const dispatch = useContext(DispatchContext)
  const [addEvents, connectErrors] = useEventLoop(
    dispatch,
    initialEvents,
    clientStorage,
  )
  return createElement(
    EventLoopContext.Provider,
    { value: [addEvents, connectErrors] },
    children
  );
}

export function StateProvider({ children }) {
  const [reflex___state____state, dispatch_reflex___state____state] = useReducer(applyDelta, initialState["reflex___state____state"])
const [reflex___state____state__reflex___state____frontend_event_exception_state, dispatch_reflex___state____state__reflex___state____frontend_event_exception_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____frontend_event_exception_state"])
const [reflex___state____state__reflex___state____on_load_internal_state, dispatch_reflex___state____state__reflex___state____on_load_internal_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____on_load_internal_state"])
const [reflex___state____state__reflex___state____update_vars_internal_state, dispatch_reflex___state____state__reflex___state____update_vars_internal_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____update_vars_internal_state"])
const [reflex___state____state__reflex_tree___state____state, dispatch_reflex___state____state__reflex_tree___state____state] = useReducer(applyDelta, initialState["reflex___state____state.reflex_tree___state____state"])
  const dispatchers = useMemo(() => {
    return {
      "reflex___state____state": dispatch_reflex___state____state,
"reflex___state____state.reflex___state____frontend_event_exception_state": dispatch_reflex___state____state__reflex___state____frontend_event_exception_state,
"reflex___state____state.reflex___state____on_load_internal_state": dispatch_reflex___state____state__reflex___state____on_load_internal_state,
"reflex___state____state.reflex___state____update_vars_internal_state": dispatch_reflex___state____state__reflex___state____update_vars_internal_state,
"reflex___state____state.reflex_tree___state____state": dispatch_reflex___state____state__reflex_tree___state____state,
    }
  }, [])

  return (
    createElement(StateContexts.reflex___state____state,{value: reflex___state____state},
createElement(StateContexts.reflex___state____state__reflex___state____frontend_event_exception_state,{value: reflex___state____state__reflex___state____frontend_event_exception_state},
createElement(StateContexts.reflex___state____state__reflex___state____on_load_internal_state,{value: reflex___state____state__reflex___state____on_load_internal_state},
createElement(StateContexts.reflex___state____state__reflex___state____update_vars_internal_state,{value: reflex___state____state__reflex___state____update_vars_internal_state},
createElement(StateContexts.reflex___state____state__reflex_tree___state____state,{value: reflex___state____state__reflex_tree___state____state},
    createElement(DispatchContext, {value: dispatchers}, children)
    )))))
  )
}