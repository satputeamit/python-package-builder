import os
import subprocess
import tempfile
import common
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage,HumanMessage

@tool
def run_and_debug_cpp_code(_: str = "") -> str:
    """
    Compiles and runs the converted C++ code. If it fails, tries to auto-correct.
    Retries until successful, then returns the output.
    """
   

    with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False, mode="w") as cpp_file:
        cpp_file.write(common.code)
        cpp_filename = cpp_file.name

    binary_filename = cpp_filename.replace(".cpp", "")
    attempts = 0

    while attempts < 3:
        compile_result = subprocess.run(
            ["g++", "-o", binary_filename, cpp_filename],
            capture_output=True, text=True
        )

        if compile_result.returncode == 0:
            run_result = subprocess.run([binary_filename], capture_output=True, text=True)
            return f"✅ Output:\n{run_result.stdout}"
        else:
            error_msg = compile_result.stderr

            fixer =common.llm
            messages = [
                SystemMessage(content="You are a C++ code fixer. Fix any compilation errors and return ONLY corrected code."),
                HumanMessage(content=f"C++ code:\n```cpp\n{converted_code}\n```\n\nCompiler error:\n{error_msg}")
            ]
            fixed_response = fixer.invoke(messages)
            converted_code = fixed_response.content.strip()

            with open(cpp_filename, "w") as f:
                f.write(converted_code)

            attempts += 1

    return f"❌ Failed to compile after {attempts} attempts."
