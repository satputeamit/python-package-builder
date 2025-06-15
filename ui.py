import gradio as gr
import common
# Global cache of code
converted_cpp_code = ""

def convert_python_to_cpp(python_code):
    from tools.code_converter import code_convert  # or access your function directly  
    cpp = code_convert(python_code)
    common.code = cpp
    return cpp

def add_pybind_code(cpp_code):
    from tools.make_pybuild import add_pybind  
    pybind_code = add_pybind(cpp_code)
    common.code = pybind_code
    return pybind_code

def generate_extension(cpp_code, platform, module_name="cpp_module"):
    from tools.make_package import _generate_extension_cross_platform  
    common.code = cpp_code
    return _generate_extension_cross_platform(module_name=module_name,platform=platform)

with gr.Blocks(title="Python to C++ + Pybind11 Converter") as demo:
    gr.Markdown("# 🐍 ➡️ C++ Converter with Pybind Builder")

    with gr.Row():
        python_input = gr.Textbox(label="Enter Python Code", lines=10)
        convert_btn = gr.Button("Convert to C++")
        cpp_output = gr.Textbox(label="Converted C++ Code", lines=10)

    convert_btn.click(fn=convert_python_to_cpp, inputs=python_input, outputs=cpp_output)

    with gr.Row():
        pybind_btn = gr.Button("Add pybind11 Support")
        pybind_cpp_output = gr.Textbox(label="C++ Code with pybind11", lines=10)

    pybind_btn.click(fn=add_pybind_code, inputs=cpp_output, outputs=pybind_cpp_output)

    with gr.Row():
        platform_choice = gr.Radio(["Windows", "Linux"], label="Select Platform", value="Windows")
        module_name = gr.Textbox(label="Module Name", value="cpp_module")
        build_btn = gr.Button("Build Extension")
        result_msg = gr.Textbox(label="Build Output", lines=5)

    build_btn.click(fn=generate_extension, inputs=[pybind_cpp_output, platform_choice, module_name], outputs=result_msg)

demo.launch()
