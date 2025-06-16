# 🔄 Python package builder with LangGraph + pybind11

This project is a fully automated Python-to-C++ code converter using [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), and `pybind11`. It takes your Python code, converts it to C++, adds pybind11 bindings, builds it into a `.pyd` or `.so` extension, and saves it — all powered by an LLM and a sequence of smart tools.

---

## ✨ Features

- ✅ Converts Python code to C++ using LLM tooling  
- ✅ Adds `pybind11` bindings automatically  
- ✅ Builds platform-specific `.pyd` (Windows) or `.so` (Linux) modules  
- ✅ Saves the final shared library for Python use  
- ✅ Modular, step-by-step orchestration using LangGraph  
- ✅ Tool integration and dynamic flow control  

---

## 🧠 How It Works

The system is driven by a graph of actions defined using LangGraph:

1. **Input Python code**
2. **Convert to C++**
3. **Add pybind11 bindings**
4. **Generate cross-platform extension**
5. **Save the output**

Each step is triggered conditionally based on tracked tool completion, allowing the LLM to manage the flow.

---

## 🛠️ Tech Stack

- **LangGraph**: Controls the conversion pipeline  
- **LangChain**: LLM orchestration  
- **ChatGroq**: LLM backend  
- **pybind11**: C++/Python binding  
- **ChromaDB + HuggingFace Embeddings**: (optional, pluggable)  
- **Python & subprocess**: For compilation and file handling  

---

## 📁 Project Structure

```
.
├── main.py                     # Entry point (this file)
├── tools/
│   ├── code_converter.py       # Python-to-C++ converter tool
│   ├── make_pybuild.py         # Tool to add pybind11 binding
│   ├── make_package.py         # Tool to build cross-platform shared library
│   └── code_save.py            # Tool to save the compiled output
├── common.py                   # Shared utility / LLM config
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- `g++` (for C++ compilation)
- `pybind11`
- `langchain`, `langgraph`, `langchain-groq`, `chroma`, etc.
- for windows required visual-studio build tool "cl.exe"

Install dependencies:

```bash
pip install -r req.txt
```

> Note: You need to set up a working Groq API key for LLM inference.

### Run the Converter

For command prompt/terminal based: Manual
```bash
python app.py
```
For command prompt/terminal based: Automated
```bash
python autoapp.py
```
For UI:
```bash
python ui.py
```

You will be prompted to input Python code. The system will automatically process it through the LangGraph flow.

---

## 🧪 Example

```python
# You input:
def add(a, b):
    return a + b
```

The system will:
1. Convert it to C++
2. Wrap it with `pybind11`
3. Compile a `.pyd`/`.so` file
4. Save it for Python use

---

## 📦 Output

- `.cpp` source file
- `bindings.cpp` (with pybind11)
- Compiled `.pyd` or `.so` file ready to import in Python

---

## 🧰 Tracker System

The system maintains a tracker of completed tool calls:
- `code_convert`
- `add_pybind`
- `generate_extension_cross_platform`
- `save_code`

This avoids redundant calls and enables stateful control.
