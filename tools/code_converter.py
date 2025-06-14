import common
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage,HumanMessage


@tool
def code_convert(code: str)->str:
    """Uses LLM to convert Python code to optimized C++ code."""  

    system = SystemMessage(content="You are a code converter. Convert Python code to optimized C++ code. Only output the converted C++ code. Do not explain or use markdown.")
    user = HumanMessage(content=f"Convert this Python code to C++:\n{code}")
   
    response = common.llm.invoke([system, user])

    # Save only the raw C++ output
    common.code = response.content.strip()
    common.code = common.code.replace('```cpp',"")
    common.code = common.code.replace('```',"")
    return common.code