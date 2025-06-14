import common
from langchain_core.tools import tool


@tool
def save_code(filename: str) -> str:
    """Saves the converted C++ code to a file."""
  
    print("converted_code::", common.code)
    if not filename.endswith(".cpp"):
        filename += ".cpp"
    try:
        with open("./build/"+filename, "w") as f:
            f.write(common.code)
        return f"Code saved to {filename}"
    except Exception as e:
        return f"Failed to save file: {str(e)}"