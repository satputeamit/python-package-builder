import os
import subprocess
import tempfile
from typing import Annotated,Sequence,TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage,HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
#tools
import common
from tools.code_converter import code_convert
from tools.code_save import save_code
from tools.make_pybuild import add_pybind
from tools.make_package import generate_extension_cross_platform

tracker=[]
class AgentState(TypedDict):  
    messages : Annotated[Sequence[BaseMessage], add_messages]



tools = [code_convert,add_pybind,generate_extension_cross_platform, save_code]

llm_with_tools = common.llm.bind_tools(tools=tools)

def controller_node(state: AgentState) -> AgentState:
    global tracker
    messages = list(state["messages"])

    def has_step(tag: str):
        # print( "msg========>",[m.content for m in messages])
        # data = any(isinstance(m, ToolMessage) and tag in m.content for m in messages)
        print("Tracker===", tracker)
        data = tag in tracker
        print("data=====>", data)
        return data

    steps = []
    print("step::", steps)
    if not has_step("code_convert"):
        steps.append(HumanMessage(content="Convert this Python code to C++ using code_convert"))

    elif has_step("code_convert") and not has_step("add_pybind"):
        steps.append(HumanMessage(content="add pybind"))

    elif has_step("add_pybind") and not has_step("generate_extension_cross_platform"):
        steps.append(HumanMessage(content="make package .pyd"))

    elif has_step("generate_extension_cross_platform") and not has_step("save_code"):
        steps.append(HumanMessage(content="Save"))

    # If no messages, ask for input
    print("steps::", steps)
    if not messages:
        print("\n👤 Enter Python code to convert to C++ (end input with an empty line):")
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        user_code = "\n".join(lines)
        steps = [HumanMessage(content=user_code)]

    if not steps:
        return {"messages": messages}  # nothing to do

    # Call LLM
    system_prompt = SystemMessage(content="You are an assistant that automatically converts and builds Python code to C++ bindings.")
    response = llm_with_tools.invoke([system_prompt] + messages + steps)

    print(f"\n🤖 AI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        tool = [tc['name'] for tc in response.tool_calls]
        print(f"🔧 Using Tools: {tool}")
        # tracker.extend(tool)

    return {"messages": messages + steps + [response]}


def should_continue(state: AgentState) -> str:
    for message in reversed(state["messages"]):
        if isinstance(message, ToolMessage) and "saved" in message.content.lower():
            return "end"
    return "continue"



graph = StateGraph(AgentState)
graph.add_node("controller", controller_node)
graph.add_node("tools", ToolNode(tools=tools))
graph.set_entry_point("controller")
graph.add_edge("controller", "tools")
graph.add_conditional_edges("tools", should_continue, {"continue": "controller", "end": END})

app = graph.compile()


def run_converter():
    print("🔄 PYTHON TO C++ CONVERTER 🔄")
    state = {"messages": []}
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            for msg in step["messages"][-2:]:
                if isinstance(msg, ToolMessage):
                    print(f"🛠️ TOOL RESULT: {msg.content}")
                    # ✅ Update tracker based on tool message content
                    if "code_convert" in msg.name:
                        tracker.append("code_convert")
                    elif "add_pybind" in msg.name:
                        tracker.append("add_pybind")
                    elif "generate_extension_cross_platform" in msg.name:
                        tracker.append("generate_extension_cross_platform")
                    elif "save_code" in msg.name:
                        tracker.append("save_code")

    print("✅ Conversion finished.")

if __name__ == "__main__":
    run_converter()
