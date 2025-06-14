import common
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage,HumanMessage

@tool
def add_pybind(code: str)->str:
    """Uses LLM to add pybind header and required code in C++ code."""  

    system = SystemMessage(content="You are a code converter. Add pybind header and other required code to C++ code and also use defined function name as module name properly, will use to to create .pyd or .so file. Only output the converted C++ code. Do not explain or use markdown.")
    user = HumanMessage(content=f"Convert this C++ code  which will use for building .pyd file or .so file:\n{code}")
   
    response = common.llm.invoke([system, user])

    # Save only the raw C++ output
    common.code =response.content.strip()
    common.code =  common.code.replace('```cpp',"")
    common.code =  common.code.replace('```',"")
    return  common.code
