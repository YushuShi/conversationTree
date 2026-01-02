import {Fragment,useCallback,useContext,useEffect,useRef} from "react"
import {Avatar as RadixThemesAvatar,Badge as RadixThemesBadge,Box as RadixThemesBox,Button as RadixThemesButton,Checkbox as RadixThemesCheckbox,Code as RadixThemesCode,ContextMenu as RadixThemesContextMenu,Dialog as RadixThemesDialog,Flex as RadixThemesFlex,Heading as RadixThemesHeading,IconButton as RadixThemesIconButton,Link as RadixThemesLink,ScrollArea as RadixThemesScrollArea,Select as RadixThemesSelect,Separator as RadixThemesSeparator,Text as RadixThemesText,TextField as RadixThemesTextField,Tooltip as RadixThemesTooltip} from "@radix-ui/themes"
import {ColorModeContext,EventLoopContext,StateContexts} from "$/utils/context"
import {ReflexEvent,getRefValue,getRefValues,isNotNullOrUndefined,isTrue,refs} from "$/utils/state"
import {Moon as LucideMoon,RefreshCcw as LucideRefreshCcw,Settings as LucideSettings,Share2 as LucideShare2,Sun as LucideSun} from "lucide-react"
import DebounceInput from "react-debounce-input"
import {Helmet} from "react-helmet"
import {Link as ReactRouterLink} from "react-router"
import ReactMarkdown from "react-markdown"
import "katex/dist/katex.min.css"
import remarkMath from "remark-math"
import remarkGfm from "remark-gfm"
import remarkUnwrapImages from "remark-unwrap-images"
import rehypeKatex from "rehype-katex"
import rehypeRaw from "rehype-raw"
import {PrismAsyncLight as SyntaxHighlighter} from "react-syntax-highlighter"
import oneLight from "react-syntax-highlighter/dist/esm/styles/prism/one-light"
import oneDark from "react-syntax-highlighter/dist/esm/styles/prism/one-dark"
import {Root as RadixFormRoot} from "@radix-ui/react-form"
import {jsx} from "@emotion/react"




function Fragment_4eccfd74653df2c248da64de2d1cc715 () {
  const { resolvedColorMode } = useContext(ColorModeContext)



  return (
    jsx(Fragment,{},((resolvedColorMode?.valueOf?.() === "light"?.valueOf?.())?(jsx(Fragment,{},jsx(LucideSun,{},))):(jsx(Fragment,{},jsx(LucideMoon,{},)))))
  )
}


function Iconbutton_64cd1f55e79fb92a917783c799ca0981 () {
  const { toggleColorMode } = useContext(ColorModeContext)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_9922dd3e837b9e087c86a2522c2c93f8 = useCallback(toggleColorMode, [addEvents, ReflexEvent, toggleColorMode])

  return (
    jsx(RadixThemesIconButton,{css:({ ["padding"] : "6px", ["background"] : "transparent", ["color"] : "inherit", ["zIndex"] : "20", ["&:hover"] : ({ ["cursor"] : "pointer" }) }),onClick:on_click_9922dd3e837b9e087c86a2522c2c93f8,size:"1"},jsx(Fragment_4eccfd74653df2c248da64de2d1cc715,{},))
  )
}


function Select__root_98d10fa33cab8a0e34ba5acdf4ed1da8 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_752305895252f25547ecaf37a9de1ba7 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.set_selected_model_key", ({ ["key"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesSelect.Root,{onValueChange:on_change_752305895252f25547ecaf37a9de1ba7,value:reflex___state____state__reflex_tree___state____state.selected_model_key_rx_state_},jsx(RadixThemesSelect.Trigger,{css:({ ["width"] : "100%" })},),jsx(RadixThemesSelect.Content,{},jsx(RadixThemesSelect.Group,{},"",jsx(RadixThemesSelect.Item,{value:"ChatGPT (GPT-5.2 Pro)"},"ChatGPT (GPT-5.2 Pro)"),jsx(RadixThemesSelect.Item,{value:"ChatGPT (GPT-5.2)"},"ChatGPT (GPT-5.2)"),jsx(RadixThemesSelect.Item,{value:"ChatGPT (GPT-5 Mini)"},"ChatGPT (GPT-5 Mini)"),jsx(RadixThemesSelect.Item,{value:"ChatGPT (GPT-5 Nano)"},"ChatGPT (GPT-5 Nano)"),jsx(RadixThemesSelect.Item,{value:"Claude 4.5 Opus"},"Claude 4.5 Opus"),jsx(RadixThemesSelect.Item,{value:"Claude 4.5 Sonnet"},"Claude 4.5 Sonnet"),jsx(RadixThemesSelect.Item,{value:"Claude 4.5 Haiku"},"Claude 4.5 Haiku"),jsx(RadixThemesSelect.Item,{value:"Gemini 2.0 Flash"},"Gemini 2.0 Flash"),jsx(RadixThemesSelect.Item,{value:"Gemini 3.0 Pro (Preview)"},"Gemini 3.0 Pro (Preview)"))))
  )
}


function Button_e3720ecd3120d23ff81bab94c2d1fb14 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_c84cf1179e7ab45840eff30e02770fce = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.toggle_settings_modal", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{css:({ ["width"] : "100%" }),onClick:on_click_c84cf1179e7ab45840eff30e02770fce,variant:"soft"},"Open API Settings")
  )
}


function Fragment_c252ef831a13dd95143cf92ac4075328 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(Fragment,{},(reflex___state____state__reflex_tree___state____state.has_any_api_key_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"2"},"API keys saved for this browser."))):(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",size:"2",weight:"bold"},"Paste your API keys to start.")))))
  )
}


function Debounceinput_ad1c40a6d462fd84019d7d558f0d6e43 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_0a539a841ab9ff06675b7ea8b83f4067 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.set_current_api_key", ({ ["key"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_0a539a841ab9ff06675b7ea8b83f4067,placeholder:reflex___state____state__reflex_tree___state____state.current_api_key_placeholder_rx_state_,type:"password",value:(isNotNullOrUndefined(reflex___state____state__reflex_tree___state____state.current_api_key_rx_state_) ? reflex___state____state__reflex_tree___state____state.current_api_key_rx_state_ : "")},)
  )
}


function Debounceinput_6a50c8437b4e8cc4c4a9055ad48f2cdd () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_b1aaec1ac5be2b2ae05f5ecdb84d18e1 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.set_search_api_key", ({ ["key"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_b1aaec1ac5be2b2ae05f5ecdb84d18e1,placeholder:"TAVILY_API_KEY",type:"password",value:(isNotNullOrUndefined(reflex___state____state__reflex_tree___state____state.search_api_key_rx_state_) ? reflex___state____state__reflex_tree___state____state.search_api_key_rx_state_ : "")},)
  )
}


function Button_efff4efa2f4d82a3f09d952520dccaa7 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_c49c450c555fd35345f244ced206522c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.save_api_keys", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{css:({ ["width"] : "100%" }),onClick:on_click_c49c450c555fd35345f244ced206522c},"Save Keys")
  )
}


function Button_1d24448ac956b6a8f55899673112dc80 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_841983f204a3e43b10a32851ad1d99e3 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.reset_keys", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{css:({ ["width"] : "100%" }),onClick:on_click_841983f204a3e43b10a32851ad1d99e3,variant:"soft"},"Reset Keys")
  )
}


function Fragment_87cf7d6942d952aeaa12c961845d4116 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(Fragment,{},(reflex___state____state__reflex_tree___state____state.is_logged_in_rx_state_?(jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["marginTop"] : "4", ["width"] : "100%" }),direction:"column",gap:"2"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"2"},"API keys are managed in Settings."),jsx(Button_e3720ecd3120d23ff81bab94c2d1fb14,{},)))):(jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["marginTop"] : "4", ["width"] : "100%" }),direction:"column",gap:"2"},jsx(Fragment_c252ef831a13dd95143cf92ac4075328,{},),jsx(RadixThemesText,{as:"p",css:({ ["marginTop"] : "2" }),size:"2",weight:"bold"},"API Key"),jsx(Debounceinput_ad1c40a6d462fd84019d7d558f0d6e43,{},),jsx(RadixThemesText,{as:"p",css:({ ["marginTop"] : "2" }),size:"2",weight:"bold"},"Deep Search Key (Tavily)"),jsx(Debounceinput_6a50c8437b4e8cc4c4a9055ad48f2cdd,{},),jsx(Button_efff4efa2f4d82a3f09d952520dccaa7,{},),jsx(Button_1d24448ac956b6a8f55899673112dc80,{},))))))
  )
}


function Button_8d83602b8fd0496791d71af5354f3337 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_03f4b298f68822677d9a11d74d0c97c1 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.add_new_topic", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{css:({ ["width"] : "100%" }),onClick:on_click_03f4b298f68822677d9a11d74d0c97c1},"\u2795 New Topic")
  )
}


function Button_d005b3a24d469ba2c6b0808c7298d7a9 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_46517bb836e735ca2ab204423ddc7f6d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.start_new_chat", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{onClick:on_click_46517bb836e735ca2ab204423ddc7f6d,size:"1",variant:"ghost"},"\ud83c\udd95 New")
  )
}


function Flex_37fa3ac3393860415b1c6f0cae46290a () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"column",gap:"1"},Array.prototype.map.call(reflex___state____state__reflex_tree___state____state.chat_groups_rx_state_ ?? [],((group_rx_state_,index_153eccd629980b6edab506c0eb301bf8)=>(jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["alignItems"] : "start" }),direction:"column",key:index_153eccd629980b6edab506c0eb301bf8,gap:"1"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray", ["marginTop"] : "2" }),size:"1",weight:"bold"},group_rx_state_?.["date"]),Array.prototype.map.call(group_rx_state_?.["chats"] ?? [],((chat_rx_state_,index_17561c8083d3f04e816e3c6d5ab68c6b)=>(jsx(RadixThemesBox,{css:({ ["width"] : "100%" }),draggable:true,key:index_17561c8083d3f04e816e3c6d5ab68c6b,onDragStart:((_e0) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.set_dragged_chat_id", ({ ["chat_id"] : chat_rx_state_?.["id"] }), ({  })))], [_e0], ({  }))))},jsx(RadixThemesButton,{css:({ ["width"] : "100%", ["justifyContent"] : "start", ["fontSize"] : "14px", ["color"] : "gray" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.load_chat", ({ ["chat_id"] : chat_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),variant:"ghost"},chat_rx_state_?.["title"]))))))))))
  )
}


function Fragment_725812c06a36e3805052e52988336c17 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(Fragment,{},(isTrue(reflex___state____state__reflex_tree___state____state.user_rx_state_)?(jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%", ["marginTop"] : "4" }),direction:"row",gap:"3"},jsx(RadixThemesText,{as:"p",size:"2",weight:"bold"},"History"),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},),jsx(Button_d005b3a24d469ba2c6b0808c7298d7a9,{},)),jsx(RadixThemesScrollArea,{css:({ ["maxHeight"] : "200px" })},jsx(Flex_37fa3ac3393860415b1c6f0cae46290a,{},))))):(jsx(Fragment,{},))))
  )
}


function Flex_a494994c4bc7d01ca2e539f81b13812d () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"0"},Array.prototype.map.call(reflex___state____state__reflex_tree___state____state.flat_tree_rx_state_ ?? [],((node_rx_state_,index_7fe6328d496e6dbb854f3b8beb94c6b5)=>(jsx(RadixThemesContextMenu.Root,{key:index_7fe6328d496e6dbb854f3b8beb94c6b5},jsx(RadixThemesContextMenu.Trigger,{},jsx(RadixThemesBox,{css:({ ["width"] : "100%" }),onDragOver:((_e0) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => null), ["callback"] : null }), ({ ["preventDefault"] : true })))], [_e0], ({  })))),onDrop:((_e0) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.graft_conversation", ({ ["target_node_id"] : node_rx_state_?.["id"] }), ({  })))], [_e0], ({  }))))},jsx(RadixThemesBox,{css:({ ["cursor"] : "pointer", ["width"] : "100%" }),draggable:true,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.select_node", ({ ["node_id"] : node_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),onDragStart:((_e0) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.set_dragged_node_id", ({ ["node_id"] : node_rx_state_?.["id"] }), ({  })))], [_e0], ({  }))))},jsx(RadixThemesBox,{css:({ ["paddingTop"] : "4px", ["paddingBottom"] : "4px", ["paddingRight"] : "8px", ["paddingLeft"] : ((node_rx_state_?.["indent"] * 1)+"rem"), ["borderRadius"] : "4px", ["width"] : "100%", ["background"] : (node_rx_state_?.["is_selected"] ? "var(--accent-3)" : (node_rx_state_?.["is_grafted"] ? "var(--green-3)" : "transparent")), ["&:hover"] : ({ ["background"] : "var(--gray-3)" }) })},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(Fragment,{},(node_rx_state_?.["has_children"]?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["cursor"] : "pointer", ["marginRight"] : "6px", ["width"] : "12px", ["textAlign"] : "center", ["fontFamily"] : "monospace", ["--default-font-family"] : "monospace", ["userSelect"] : "none" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.toggle_node_collapse", ({ ["node_id"] : node_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},(node_rx_state_?.["is_collapsed"] ? ">" : "v")))):(jsx(Fragment,{},jsx(RadixThemesBox,{css:({ ["width"] : "20px" })},))))),jsx(Fragment,{},((node_rx_state_?.["role"]?.valueOf?.() === "model"?.valueOf?.())?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "purple" })},("A: "+(JSON.stringify(node_rx_state_?.["content"])).split("").slice(undefined, 30).join("")+"...")))):(jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(Fragment,{},(!((node_rx_state_?.["index_label"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontWeight"] : "bold", ["color"] : "gray", ["marginRight"] : "4px" })},node_rx_state_?.["index_label"]))):(jsx(Fragment,{},)))),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "green" })},(node_rx_state_?.["content"].split("").slice(undefined, 30).join("")+"..."))))))),jsx(Fragment,{},(node_rx_state_?.["is_selected"]?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "14px", ["marginLeft"] : "auto" })},"\ud83d\udccc"))):(jsx(Fragment,{},))))))))),jsx(RadixThemesContextMenu.Content,{},jsx(RadixThemesContextMenu.Item,{css:({ ["color"] : "red" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.delete_node_action", ({ ["node_id"] : node_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Delete")))))))
  )
}


function Text_18e2224a2564a4b1179cf27a020f04ef () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},("$"+reflex___state____state__reflex_tree___state____state.session_cost_rx_state_))
  )
}


function Text_3a98efa2d2a1746f8c28f7274c43e683 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},reflex___state____state__reflex_tree___state____state.session_tokens_rx_state_)
  )
}


function Text_51f21d23d5353b9f50a4eb05c18ed77c () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},("$"+reflex___state____state__reflex_tree___state____state.daily_cost_rx_state_))
  )
}


function Text_c4be0f5f0c871e4378a808a13baced62 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},reflex___state____state__reflex_tree___state____state.daily_tokens_rx_state_)
  )
}


function Text_6de6d4a65d0568c3df5488f39ba959ef () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},("$"+reflex___state____state__reflex_tree___state____state.weekly_cost_rx_state_))
  )
}


function Text_cf0da5e001017d94679c8880be6dfb68 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},reflex___state____state__reflex_tree___state____state.weekly_tokens_rx_state_)
  )
}


function Text_318a53e69795218ed8f736ecaa7a9eb3 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},("$"+reflex___state____state__reflex_tree___state____state.user_rx_state_?.["total_cost"]))
  )
}


function Text_e92ff41d410af70364ef24e2a51a4fc7 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},reflex___state____state__reflex_tree___state____state.user_rx_state_?.["total_tokens"])
  )
}


function Fragment_455dca085d621305307d645c2930aadd () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(Fragment,{},(isTrue(reflex___state____state__reflex_tree___state____state.user_rx_state_)?(jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"3"},jsx(RadixThemesSeparator,{css:({ ["marginTop"] : "2", ["marginBottom"] : "2" }),size:"4"},),jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},"Today"),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",justify:"between",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},"Cost:"),jsx(Text_51f21d23d5353b9f50a4eb05c18ed77c,{},)),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",justify:"between",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},"Tokens:"),jsx(Text_c4be0f5f0c871e4378a808a13baced62,{},)),jsx(RadixThemesSeparator,{css:({ ["marginTop"] : "2", ["marginBottom"] : "2" }),size:"4"},),jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},"This Week"),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",justify:"between",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},"Cost:"),jsx(Text_6de6d4a65d0568c3df5488f39ba959ef,{},)),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",justify:"between",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},"Tokens:"),jsx(Text_cf0da5e001017d94679c8880be6dfb68,{},)),jsx(RadixThemesSeparator,{css:({ ["marginTop"] : "2", ["marginBottom"] : "2" }),size:"4"},),jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},"Total"),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",justify:"between",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},"Cost:"),jsx(Text_318a53e69795218ed8f736ecaa7a9eb3,{},)),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",justify:"between",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},"Tokens:"),jsx(Text_e92ff41d410af70364ef24e2a51a4fc7,{},))))):(jsx(Fragment,{},))))
  )
}


function Text_e78a40079991ce24d01ee20fd68b0927 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesText,{as:"p",size:"1",weight:"bold"},reflex___state____state__reflex_tree___state____state.user_rx_state_?.["email"])
  )
}


function Avatar_2f7e0bdde496512a02982b36d20da275 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesAvatar,{fallback:reflex___state____state__reflex_tree___state____state.user_rx_state_?.["email"]?.at?.(0),size:"2"},)
  )
}


function Button_2f10311455cfc372272022acedd467b2 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_08983a41c67e7022b9f9f1bcca494b7f = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.logout", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{color:"red",onClick:on_click_08983a41c67e7022b9f9f1bcca494b7f,size:"1",variant:"ghost"},"Log Out")
  )
}


function Button_543df2458f67f031defca407de660254 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_02f40f698cb5c7bd16185acb148d1ec9 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.toggle_login_modal", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{onClick:on_click_02f40f698cb5c7bd16185acb148d1ec9,size:"2",variant:"solid"},"Sign In / Sign Up")
  )
}


function Fragment_e4f7d34f2e580996ef6076a34b94948e () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    jsx(Fragment,{},(reflex___state____state__reflex_tree___state____state.is_logged_in_rx_state_?(jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "center" }),direction:"row",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "end" }),direction:"column",gap:"0"},jsx(Text_e78a40079991ce24d01ee20fd68b0927,{},),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "green" }),size:"1"},"Logged In")),jsx(Avatar_2f7e0bdde496512a02982b36d20da275,{},),jsx(RadixThemesTooltip,{content:"API Settings"},jsx(RadixThemesButton,{css:({ ["padding"] : "1" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.toggle_settings_modal", ({  }), ({  })))], [_e], ({  })))),size:"1",variant:"ghost"},jsx(LucideSettings,{size:14},))),jsx(Button_2f10311455cfc372272022acedd467b2,{},)))):(jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "center" }),direction:"row",gap:"2"},jsx(Button_543df2458f67f031defca407de660254,{},),jsx(RadixThemesTooltip,{content:"API Settings"},jsx(RadixThemesButton,{css:({ ["padding"] : "1" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.toggle_settings_modal", ({  }), ({  })))], [_e], ({  })))),size:"2",variant:"ghost"},jsx(LucideSettings,{size:14},))))))))
  )
}


function Dialog__title_fd3a92bba7e7b940004531bf671e7466 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesDialog.Title,{},(reflex___state____state__reflex_tree___state____state.is_signup_mode_rx_state_ ? "Sign Up" : "Sign In"))
  )
}


function Dialog__description_fb3dc8275fead2f628c564b9ea50478d () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesDialog.Description,{},(reflex___state____state__reflex_tree___state____state.is_signup_mode_rx_state_ ? "Create a new account to save your chats and API keys." : "Enter your credentials to access your account."))
  )
}


function Debounceinput_fdccdeac5420c1c700d40fa70a5c0dc1 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_3e390790bdadcb2c66447280ea54ad9c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.set_auth_email", ({ ["email"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(DebounceInput,{debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_3e390790bdadcb2c66447280ea54ad9c,placeholder:"Email",value:(isNotNullOrUndefined(reflex___state____state__reflex_tree___state____state.auth_email_rx_state_) ? reflex___state____state__reflex_tree___state____state.auth_email_rx_state_ : "")},)
  )
}


function Debounceinput_1ceb7cd66c2f79f489053d011e81841a () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_a69d82918f12368b09193bded806c5b2 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.set_auth_password", ({ ["password"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(DebounceInput,{debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_a69d82918f12368b09193bded806c5b2,placeholder:"Password",type:"password",value:(isNotNullOrUndefined(reflex___state____state__reflex_tree___state____state.auth_password_rx_state_) ? reflex___state____state__reflex_tree___state____state.auth_password_rx_state_ : "")},)
  )
}


function Button_031498b4ea3b95324c61c0015d09385c () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_d6671b1f86c4553b668054e6fbc35661 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.signup", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{css:({ ["width"] : "100%" }),onClick:on_click_d6671b1f86c4553b668054e6fbc35661},"Sign Up")
  )
}


function Button_56b3866c8493a7ba913cd9a18909a2bf () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_6045a0475b5ebe13e9308385a02bf2d4 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.login", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{css:({ ["width"] : "100%" }),onClick:on_click_6045a0475b5ebe13e9308385a02bf2d4},"Log In")
  )
}


function Fragment_93c887c09e1937e43c7e30f9d2c192ad () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(Fragment,{},(reflex___state____state__reflex_tree___state____state.is_signup_mode_rx_state_?(jsx(Fragment,{},jsx(Button_031498b4ea3b95324c61c0015d09385c,{},))):(jsx(Fragment,{},jsx(Button_56b3866c8493a7ba913cd9a18909a2bf,{},)))))
  )
}


function Link_60479d28564ac2381d328b4b704ecc9a () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);
const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)

const on_click_f9c9a8843694d228df0b535139f19db0 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.toggle_auth_mode", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesLink,{css:({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) }),href:"#",onClick:on_click_f9c9a8843694d228df0b535139f19db0},(reflex___state____state__reflex_tree___state____state.is_signup_mode_rx_state_ ? "Sign In" : "Sign Up"))
  )
}


function Text_1aa6aab885336fc3efad2d262d97d740 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesText,{as:"p",size:"1"},(reflex___state____state__reflex_tree___state____state.is_signup_mode_rx_state_ ? "Already have an account? " : "Don't have an account? "),jsx(Link_60479d28564ac2381d328b4b704ecc9a,{},))
  )
}


function Dialog__root_17de9fd21ae697982b08c9d0ac60ca5f () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_open_change_95b826674a34a0971b1b9f780c1f8c93 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.toggle_login_modal", ({  }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesDialog.Root,{onOpenChange:on_open_change_95b826674a34a0971b1b9f780c1f8c93,open:reflex___state____state__reflex_tree___state____state.show_login_rx_state_},jsx(RadixThemesDialog.Content,{},jsx(Dialog__title_fd3a92bba7e7b940004531bf671e7466,{},),jsx(Dialog__description_fb3dc8275fead2f628c564b9ea50478d,{},),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["marginTop"] : "4" }),direction:"column",gap:"3"},jsx(Debounceinput_fdccdeac5420c1c700d40fa70a5c0dc1,{},),jsx(Debounceinput_1ceb7cd66c2f79f489053d011e81841a,{},),jsx(Fragment_93c887c09e1937e43c7e30f9d2c192ad,{},),jsx(Text_1aa6aab885336fc3efad2d262d97d740,{},)),jsx(RadixThemesDialog.Close,{},jsx(RadixThemesButton,{css:({ ["color"] : "gray", ["marginTop"] : "4" }),size:"1",variant:"soft"},"Close"))))
  )
}


function Debounceinput_f70592127853678926633175adbaa6c6 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_a36ac22d58b8e155d34b16f8bb36b966 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.set_openai_api_key", ({ ["key"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_a36ac22d58b8e155d34b16f8bb36b966,placeholder:"OpenAI API Key (sk-...)",type:"password",value:(isNotNullOrUndefined(reflex___state____state__reflex_tree___state____state.openai_api_key_rx_state_) ? reflex___state____state__reflex_tree___state____state.openai_api_key_rx_state_ : "")},)
  )
}


function Debounceinput_db1b4e01bbb1a2ebb4b3a313e47ed2b2 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_aa38ae6982a0df9c4b86b1f204962516 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.set_anthropic_api_key", ({ ["key"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_aa38ae6982a0df9c4b86b1f204962516,placeholder:"Anthropic API Key (sk-ant...)",type:"password",value:(isNotNullOrUndefined(reflex___state____state__reflex_tree___state____state.anthropic_api_key_rx_state_) ? reflex___state____state__reflex_tree___state____state.anthropic_api_key_rx_state_ : "")},)
  )
}


function Debounceinput_188349cdda77d6252d4bdd68dc6ad1d0 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_07726f43794daca745245c2690b8a345 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.set_google_api_key", ({ ["key"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_07726f43794daca745245c2690b8a345,placeholder:"Google API Key",type:"password",value:(isNotNullOrUndefined(reflex___state____state__reflex_tree___state____state.google_api_key_rx_state_) ? reflex___state____state__reflex_tree___state____state.google_api_key_rx_state_ : "")},)
  )
}


function Button_26d65f37ca5f4cf72d42de1705b20027 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_c49c450c555fd35345f244ced206522c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.save_api_keys", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{css:({ ["width"] : "100%" }),onClick:on_click_c49c450c555fd35345f244ced206522c},"Save")
  )
}


function Dialog__root_94d7ca6af0f6eae1ef39a3f21296cdd8 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_open_change_648925ea1804c114e4d3b98fa6b73599 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.toggle_settings_modal", ({  }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesDialog.Root,{onOpenChange:on_open_change_648925ea1804c114e4d3b98fa6b73599,open:reflex___state____state__reflex_tree___state____state.show_settings_rx_state_},jsx(RadixThemesDialog.Content,{},jsx(RadixThemesDialog.Title,{},"API Settings"),jsx(RadixThemesDialog.Description,{},"Store provider-specific API keys for this account."),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["marginTop"] : "4" }),direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"2"},jsx(RadixThemesText,{as:"p",size:"2",weight:"bold"},"OpenAI"),jsx(Debounceinput_f70592127853678926633175adbaa6c6,{},)),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"2"},jsx(RadixThemesText,{as:"p",size:"2",weight:"bold"},"Claude (Anthropic)"),jsx(Debounceinput_db1b4e01bbb1a2ebb4b3a313e47ed2b2,{},)),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"2"},jsx(RadixThemesText,{as:"p",size:"2",weight:"bold"},"Gemini (Google)"),jsx(Debounceinput_188349cdda77d6252d4bdd68dc6ad1d0,{},)),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"2"},jsx(RadixThemesText,{as:"p",size:"2",weight:"bold"},"Tavily (Deep Search)"),jsx(Debounceinput_6a50c8437b4e8cc4c4a9055ad48f2cdd,{},)),jsx(Button_26d65f37ca5f4cf72d42de1705b20027,{},)),jsx(RadixThemesDialog.Close,{},jsx(RadixThemesButton,{css:({ ["color"] : "gray", ["marginTop"] : "4" }),size:"1",variant:"soft"},"Close"))))
  )
}


function Button_a2d4b02d2070eb3dd0165c4911addd7f () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);
const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)

const on_click_26ecba3709c6ecbe594a2bda92aeb381 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.toggle_history", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{css:({ ["width"] : "100%" }),onClick:on_click_26ecba3709c6ecbe594a2bda92aeb381,variant:"outline"},(reflex___state____state__reflex_tree___state____state.show_full_history_rx_state_ ? "Hide Previous Messages" : "Show Previous Messages"))
  )
}


function Fragment_a13a3a3fe1bb3ebc69d5bdeefe4dce64 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(Fragment,{},((reflex___state____state__reflex_tree___state____state.chat_history_rx_state_.length > 3)?(jsx(Fragment,{},jsx(Button_a2d4b02d2070eb3dd0165c4911addd7f,{},))):(jsx(Fragment,{},))))
  )
}


        function ComponentMap_be3dfccad967c5ae558c28786c64c3bc () {
            const { resolvedColorMode } = useContext(ColorModeContext)



            return (
                ({ ["h1"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h1",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"6",...props},children))), ["h2"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h2",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"5",...props},children))), ["h3"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h3",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"4",...props},children))), ["h4"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h4",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"3",...props},children))), ["h5"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h5",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"2",...props},children))), ["h6"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h6",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"1",...props},children))), ["p"] : (({node, children, ...props}) => (jsx(RadixThemesText,{as:"p",css:({ ["marginTop"] : "1em", ["marginBottom"] : "1em" }),...props},children))), ["ul"] : (({node, children, ...props}) => (jsx("ul",{css:({ ["listStyleType"] : "disc", ["marginTop"] : "1em", ["marginBottom"] : "1em", ["marginLeft"] : "1.5rem", ["direction"] : "column" })},children))), ["ol"] : (({node, children, ...props}) => (jsx("ol",{css:({ ["listStyleType"] : "decimal", ["marginTop"] : "1em", ["marginBottom"] : "1em", ["marginLeft"] : "1.5rem", ["direction"] : "column" })},children))), ["li"] : (({node, children, ...props}) => (jsx("li",{css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" })},children))), ["a"] : (({node, children, ...props}) => (jsx(RadixThemesLink,{css:({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) }),href:"#",...props},children))), ["code"] : (({node, inline, className, children, ...props}) => { const match = (className || '').match(/language-(?<lang>.*)/); let _language = match ? match[1] : '';  ;             return inline ? (                 jsx(RadixThemesCode,{...props},children)             ) : (                 jsx(SyntaxHighlighter,{children:((Array.isArray(children)) ? children.join("\n") : children),css:({ ["marginTop"] : "1em", ["marginBottom"] : "1em" }),language:_language,style:((resolvedColorMode?.valueOf?.() === "light"?.valueOf?.()) ? oneLight : oneDark),wrapLongLines:true,...props},)             );         }) })
            )
        }
        

function Flex_a6a7b6de494a3fa3aed57b5ee4cee747 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["padding"] : "6" }),direction:"column",gap:"3"},jsx(Fragment_a13a3a3fe1bb3ebc69d5bdeefe4dce64,{},),Array.prototype.map.call(reflex___state____state__reflex_tree___state____state.displayed_messages_rx_state_ ?? [],((message_rx_state_,index_3ed281d061f18561008ecb8243dde771)=>(jsx(RadixThemesBox,{css:({ ["paddingTop"] : "2", ["paddingBottom"] : "2", ["width"] : "100%" }),key:index_3ed281d061f18561008ecb8243dde771},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "start", ["width"] : "100%" }),direction:"column",gap:"2"},jsx(Fragment,{},((message_rx_state_?.["role"]?.valueOf?.() === "user"?.valueOf?.())?(jsx(Fragment,{},jsx(RadixThemesBox,{css:({ ["background"] : "var(--gray-3)", ["padding"] : "2", ["borderRadius"] : "8px", ["width"] : "100%" })},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["whiteSpace"] : "pre-wrap" })},message_rx_state_?.["content"]),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["paddingRight"] : "20px" }),direction:"row",justify:"end",gap:"1"},jsx(RadixThemesTooltip,{content:"Regenerate Answer"},jsx(RadixThemesButton,{css:({ ["padding"] : "1" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.regenerate_response", ({ ["node_id"] : message_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),size:"1",variant:"ghost"},jsx(LucideRefreshCcw,{size:14},))),jsx(Fragment,{},((reflex___state____state__reflex_tree___state____state.processing_rx_state_ && (reflex___state____state__reflex_tree___state____state.active_generation_user_id_rx_state_?.valueOf?.() === message_rx_state_?.["id"]?.valueOf?.()))?(jsx(Fragment,{},jsx(RadixThemesTooltip,{content:"Stop Generating"},jsx(RadixThemesButton,{color:"red",css:({ ["padding"] : "1" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.stop_generation", ({ ["user_node_id"] : message_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),size:"1",variant:"ghost"},"\u23f9")))):(jsx(Fragment,{},)))),jsx(RadixThemesTooltip,{content:"Copy Q&A to Clipboard"},jsx(RadixThemesButton,{css:({ ["padding"] : "1" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.share_response", ({ ["node_id"] : message_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),size:"1",variant:"ghost"},jsx(LucideShare2,{size:14},)))))))):(jsx(Fragment,{},jsx(RadixThemesBox,{css:({ ["background"] : "var(--accent-3)", ["padding"] : "2", ["borderRadius"] : "8px", ["width"] : "100%" })},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "start", ["width"] : "100%" }),direction:"column",gap:"1"},jsx(Fragment,{},(!((message_rx_state_?.["model"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx(RadixThemesBadge,{color:"purple",css:({ ["marginBottom"] : "2px" }),variant:"soft"},message_rx_state_?.["model"]))):(jsx(Fragment,{},)))),jsx(ReactMarkdown,{components:ComponentMap_be3dfccad967c5ae558c28786c64c3bc(),css:({ ["mathJax"] : true }),rehypePlugins:[rehypeKatex, rehypeRaw],remarkPlugins:[remarkMath, remarkGfm, remarkUnwrapImages]},message_rx_state_?.["content"]),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["marginTop"] : "2" }),direction:"row",gap:"2"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},("Tokens: "+message_rx_state_?.["tokens"])),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},"|"),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},("Cost: $"+message_rx_state_?.["cost"])))))))))))))))
  )
}


function Checkbox_8b90373f884595314e004fec35c6d4d3 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_fedf7cfebd0f5e93cb50369060dba34e = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.set_use_deep_search", ({ ["enable"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesCheckbox,{checked:reflex___state____state__reflex_tree___state____state.use_deep_search_rx_state_,onCheckedChange:on_change_fedf7cfebd0f5e93cb50369060dba34e,size:"2"},)
  )
}


function Button_ab0f73f04a70fd76ef86125b9b51c1f6 () {
  const reflex___state____state__reflex_tree___state____state = useContext(StateContexts.reflex___state____state__reflex_tree___state____state)



  return (
    jsx(RadixThemesButton,{loading:reflex___state____state__reflex_tree___state____state.processing_rx_state_,type:"submit"},"Send")
  )
}


function Root_07fb5539402078a02d8ecf77d1c6a51b () {
  const ref_chat_form = useRef(null); refs["ref_chat_form"] = ref_chat_form;
const [addEvents, connectErrors] = useContext(EventLoopContext);
const ref_chat_input = useRef(null); refs["ref_chat_input"] = ref_chat_input;

    const handleSubmit_0706ae759f79c1c5d58a6a899ee5c2e5 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["chat_form"] : getRefValue(refs["ref_chat_form"]), ["chat_input"] : getRefValue(refs["ref_chat_input"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.reflex_tree___state____state.process_chat", ({ ["form_data"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (true) {
            $form.reset()
        }
    })
    


  return (
    jsx(RadixFormRoot,{className:"Root ",css:({ ["width"] : "100%" }),id:"chat_form",onSubmit:handleSubmit_0706ae759f79c1c5d58a6a899ee5c2e5,ref:ref_chat_form},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "center" }),direction:"row",gap:"4"},jsx(RadixThemesTextField.Root,{css:({ ["flex"] : "1" }),id:"chat_input",placeholder:"Type a message...",ref:ref_chat_input},),jsx(RadixThemesText,{as:"label",size:"2"},jsx(RadixThemesFlex,{gap:"2"},jsx(Checkbox_8b90373f884595314e004fec35c6d4d3,{},),"Deep Search")),jsx(Button_ab0f73f04a70fd76ef86125b9b51c1f6,{},)))
  )
}


export default function Component() {





  return (
    jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["height"] : "100vh", ["width"] : "100vw" }),direction:"row",gap:"0"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["resize"] : "horizontal", ["overflow"] : "auto", ["zIndex"] : "10", ["width"] : "300px", ["minWidth"] : "250px", ["maxWidth"] : "50%", ["height"] : "100vh", ["padding"] : "4", ["borderRight"] : "1px solid var(--gray-3)", ["background"] : "var(--gray-1)" }),direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["alignItems"] : "center" }),direction:"row",gap:"3"},jsx(RadixThemesHeading,{size:"3"},"Conversation Tree"),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},),jsx(Iconbutton_64cd1f55e79fb92a917783c799ca0981,{},)),jsx(RadixThemesSeparator,{css:({ ["marginTop"] : "4", ["marginBottom"] : "4" }),size:"4"},),jsx(Select__root_98d10fa33cab8a0e34ba5acdf4ed1da8,{},),jsx(Fragment_87cf7d6942d952aeaa12c961845d4116,{},),jsx(RadixThemesSeparator,{css:({ ["marginBottom"] : "4" }),size:"4"},),jsx(Button_8d83602b8fd0496791d71af5354f3337,{},),jsx(Fragment_725812c06a36e3805052e52988336c17,{},),jsx(RadixThemesSeparator,{size:"4"},),jsx(Flex_a494994c4bc7d01ca2e539f81b13812d,{},),jsx(RadixThemesSeparator,{css:({ ["marginTop"] : "2", ["marginBottom"] : "2" }),size:"4"},),jsx(RadixThemesSeparator,{css:({ ["marginTop"] : "2", ["marginBottom"] : "2" }),size:"4"},),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["padding"] : "2", ["background"] : "var(--gray-2)", ["borderRadius"] : "4px", ["marginTop"] : "4", ["marginBottom"] : "4" }),direction:"column",gap:"3"},jsx(RadixThemesText,{as:"p",size:"2",weight:"bold"},"Session Usage"),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",justify:"between",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},"Cost:"),jsx(Text_18e2224a2564a4b1179cf27a020f04ef,{},)),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",justify:"between",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},"Tokens:"),jsx(Text_3a98efa2d2a1746f8c28f7274c43e683,{},)),jsx(Fragment_455dca085d621305307d645c2930aadd,{},))),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["height"] : "100vh", ["flex"] : "1", ["background"] : "var(--gray-2)" }),direction:"column",gap:"3"},jsx(Helmet,{},jsx("script",{},"\n(() => {\n  if (window.__explainSelectionHandlerInstalled) return;\n  window.__explainSelectionHandlerInstalled = true;\n  window.__explainSelectionPrimedAt = 0;\n\n  const PRIME_WINDOW_MS = 1500;\n\n  const getSelectedText = () => {\n    try {\n      const sel = window.getSelection?.();\n      return (sel && sel.toString) ? sel.toString() : \"\";\n    } catch {\n      return \"\";\n    }\n  };\n\n  const setChatInput = (text) => {\n    const input = document.getElementById(\"chat_input\");\n    if (!input) return false;\n    input.focus();\n    input.value = text;\n    input.dispatchEvent(new Event(\"input\", { bubbles: true }));\n    input.dispatchEvent(new Event(\"change\", { bubbles: true }));\n    return true;\n  };\n\n  const submitChat = () => {\n    const form = document.getElementById(\"chat_form\");\n    if (!form) return false;\n    if (form.requestSubmit) {\n      form.requestSubmit();\n      return true;\n    }\n    form.dispatchEvent(new Event(\"submit\", { bubbles: true, cancelable: true }));\n    return true;\n  };\n\n  document.addEventListener(\"keydown\", (e) => {\n    // Prime on Shift+?\n    if (e.shiftKey && e.key === \"?\") {\n      window.__explainSelectionPrimedAt = Date.now();\n      return;\n    }\n\n    // Trigger on Enter shortly after priming.\n    if (e.key === \"Enter\") {\n      const primedAt = window.__explainSelectionPrimedAt || 0;\n      if (!primedAt || (Date.now() - primedAt) > PRIME_WINDOW_MS) return;\n      window.__explainSelectionPrimedAt = 0;\n\n      const selected = getSelectedText().trim();\n      if (!selected) return;\n\n      e.preventDefault();\n      e.stopPropagation();\n\n      const prompt = `Explain the following:\\n\\n${selected}`;\n      if (setChatInput(prompt)) submitChat();\n    }\n  }, true);\n})();\n            ")),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["padding"] : "4", ["borderBottom"] : "1px solid var(--gray-3)" }),direction:"row",gap:"3"},jsx(RadixThemesHeading,{size:"4"},"Chat"),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},),jsx(Fragment_e4f7d34f2e580996ef6076a34b94948e,{},),jsx(Dialog__root_17de9fd21ae697982b08c9d0ac60ca5f,{},),jsx(Dialog__root_94d7ca6af0f6eae1ef39a3f21296cdd8,{},)),jsx(RadixThemesScrollArea,{css:({ ["flex"] : "1", ["width"] : "100%" })},jsx(Flex_a6a7b6de494a3fa3aed57b5ee4cee747,{},)),jsx(RadixThemesBox,{css:({ ["padding"] : "4", ["width"] : "100%", ["borderTop"] : "1px solid var(--gray-3)" })},jsx(Root_07fb5539402078a02d8ecf77d1c6a51b,{},)))),jsx("title",{},"ReflexTree | Index"),jsx("meta",{content:"favicon.ico",property:"og:image"},))
  )
}