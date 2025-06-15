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
from tools.code_debuger import run_and_debug_cpp_code

class AgentState(TypedDict):  
    messages : Annotated[Sequence[BaseMessage], add_messages]



tools = [code_convert,add_pybind,run_and_debug_cpp_code,generate_extension_cross_platform, save_code]

llm_with_tools = common.llm.bind_tools(tools=tools)


def code_converter_agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="""
You are a Python-to-C++ converter assistant.
- First, use 'code_convert' to convert Python to C++.
- Then, use 'run_and_debug_cpp_code' to compile and test the C++.
- If it works, ask user whether to save using 'save_code'.
- If compilation fails, retry until success using LLM fixes.
- If compilation complete, thn use 'add_pybind' to adding neccessary code.
""")
    
    if not state["messages"]:
        # user_input = input("\n👤 Enter Python code to convert to C++: ")
        print("\n👤 Enter Python code to convert to C++ (end input with an empty line):")
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        user_input = "\n".join(lines)
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input("\n👤 What next (convert more, or save)? ")
        user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt] + list(state["messages"]) + [user_message]
    response = llm_with_tools.invoke(all_messages)
    
    print(f"\n🤖 AI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"🔧 Using Tools: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state["messages"]) + [user_message, response]}

def should_continue(state: AgentState) -> str:
    for message in reversed(state["messages"]):
        if isinstance(message, ToolMessage) and "saved" in message.content.lower():
            return "end"
    return "continue"


graph = StateGraph(AgentState)
graph.add_node("agent", code_converter_agent)
graph.add_node("tools", ToolNode(tools=tools))
graph.set_entry_point("agent")
graph.add_edge("agent", "tools")
graph.add_conditional_edges("tools", should_continue, {"continue": "agent", "end": END})
app = graph.compile()


def run_converter():
    print("🔄 PYTHON TO C++ CONVERTER 🔄")
    state = {"messages": []}
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            for msg in step["messages"][-2:]:
                if isinstance(msg, ToolMessage):
                    print(f"🛠️ TOOL RESULT: {msg.content}")
    print("✅ Conversion finished.")

if __name__ == "__main__":
    run_converter()
