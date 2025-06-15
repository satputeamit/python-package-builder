import os
import subprocess
import tempfile
from typing_extensions import TypedDict
import common
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage,HumanMessage


# @tool
# def generate_extension_cross_platform(module_name: str = "cpp_module", platform: str="linux") -> str:
#     """
#     Builds a Python extension file (.pyd on Windows, .so on Linux) from the converted C++ code.
#     Uses MSVC `cl` on Windows and Docker on Linux.
#     """
#     # import platform
 
#     import tempfile, os, subprocess, sysconfig

#     with tempfile.TemporaryDirectory() as tmpdir:
#         cpp_file = os.path.join(tmpdir, f"{module_name}.cpp")
#         with open(cpp_file, "w") as f:
#             f.write(common.code)

#         ext = sysconfig.get_config_var("EXT_SUFFIX") or (".pyd" if platform.system() == "Windows" else ".so")
#         output_file = os.path.join(tmpdir, f"{module_name}{ext}")

#         # if platform.system() == "Windows":
#         if (platform.strip()).lower()=="windows":
#             # Build with MSVC cl
#             include = sysconfig.get_paths()["include"]
#             lib = sysconfig.get_config_var("LIBDIR")
#             cmd = [
#                 "cl",
#                 "/LD", cpp_file,
#                 f"/I{include}",
#                 f"/link",
#                 f"/OUT:{output_file}",
#                 f"/LIBPATH:{lib}",
#                 "python310.lib"
#             ]
#         else:
#              # Use Docker
#             # Copy the file to current dir so it maps to /build inside Docker
#             docker_build_path = f"D:/Projects/pkg-gen/build"
#             docker_cpp_file = f"{module_name}.cpp"
#             docker_so_file = f"{module_name}.so"

#             docker_cmd = [
#                 "docker", "run", "--rm",
#                 "-v", f"{docker_build_path}:/build",
#                 "so-builder",             
#                 f"g++ -O3 -Wall -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes) /build/{docker_cpp_file} -o /build/{docker_so_file}"
#             ]
#             result = subprocess.run(docker_cmd, capture_output=True, text=True)
#             if result.returncode != 0:
#                 return f"❌ Docker build failed:\n{result.stderr}"
#             return f"✅ .so file built in Docker: {module_name}.so"

#         result = subprocess.run(cmd, capture_output=True, text=True)
#         if result.returncode != 0:
#             return f"❌ MSVC build failed:\n{result.stderr}"

#         final_file = f"{module_name}{ext}"
#         final_path = os.path.abspath(final_file)
#         print(final_path)
#         with open(output_file, "rb") as src, open(final_path, "wb") as dst:
#             dst.write(src.read())

#         return f"✅ Extension built successfully and saved to: {final_path}"



def _generate_extension_cross_platform(module_name: str = "cpp_module", platform: str = "linux") -> str:
    """
    Builds a Python extension file (.pyd on Windows, .so on Linux) from the converted C++ code.
    Uses MSVC `cl` on Windows and Docker on Linux.
    """
    import os,sys, subprocess, sysconfig
    # module_name = data["module_name"]
    # platform = data["platform"]
    common.logging.info("🧪 [DEBUG] Running generate_extension_cross_platform...")
    # Define output directory (must be absolute path for Docker mount)
    docker_build_path = os.path.abspath("D:/Projects/pkg-gen/build")
    os.makedirs(docker_build_path, exist_ok=True)

    docker_cpp_file = f"{module_name}.cpp"
    docker_so_file = f"{module_name}.so"

    cpp_file_path = os.path.join(docker_build_path, docker_cpp_file)
    output_so_path = os.path.join(docker_build_path, docker_so_file)

    # Write the C++ code to a file
    with open(cpp_file_path, "w") as f:
        f.write(common.code)

    if platform.strip().lower() == "windows":
        # Build with MSVC cl
        venv_base = sys.base_prefix  # This will be your .venv path
        include_py = sysconfig.get_paths()["include"]
        include_pybind11 = os.path.join(venv_base, "Lib", "site-packages", "pybind11", "include")
        lib_dir = os.path.join(venv_base, "libs")

        ext = sysconfig.get_config_var("EXT_SUFFIX") or ".pyd"
        output_file = f"{module_name}{ext}"
        vcvars_path = "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvarsall.bat"
        if not os.path.exists(vcvars_path):
            raise FileNotFoundError(f"vcvars64.bat not found at: {vcvars_path}")

        build_cmd = (
            f'"{vcvars_path}" x64 && '  # Set up the environment
            f'cl /LD '
            f'/I D:\\Projects\\langGraph\\.venv\\Include '
            f'/I D:\\Projects\\langGraph\\.venv\\Lib\\site-packages\\pybind11\\include '
            f'D:\\Projects\\pkg-gen\\build\\{module_name}.cpp '
            f'/link /LIBPATH:D:\\Projects\\langGraph\\.venv\\libs '
            f'python310.lib '
            f'/OUT:D:\\Projects\\pkg-gen\\build\\{module_name}.pyd'
        )

        print("Running:", build_cmd)
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Build failed!")
            print(result.stderr)
            return False
        print(f"✅ Built: {output_file}")       

        return f"✅ .pyd file built at: {output_file}"

    else:
        # Build in Docker and save .so to the host-mapped directory        s
        docker_build_path = os.path.abspath("D:/Projects/pkg-gen")
        docker_build_path = docker_build_path+"/build"
        docker_cpp_file = f"{module_name}.cpp"
        docker_so_file = f"{module_name}.so"
        common.logging.info(docker_build_path)
        common.logging.info(docker_cpp_file)
        # Save C++ file to shared directory
        cpp_path = os.path.join(docker_build_path, docker_cpp_file)
        with open(cpp_path, "w") as f:
            f.write(common.code)

        # docker_cmd = [
        #     "docker", "run", "--rm",
        #     "-v", f"{docker_build_path}:/build",
        #     "so-builder",
        #     "/bin/bash", "-c",
        #     f"g++ -O3 -Wall -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes) "
        #     f"/build/{docker_cpp_file} -o /build/{docker_so_file}"
        # ]
        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{docker_build_path}:/build",
            "so-builder",
            "g++ -O3 -Wall -shared -std=c++17 -fPIC "
            "-I/usr/include/python3.11 "
            "-I/usr/local/lib/python3.11/site-packages/pybind11/include "
            f"/build/{docker_cpp_file} -o /build/{docker_so_file}"
        ]
        common.logging.info(" ".join(docker_cmd))
        result = subprocess.run(docker_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return f"❌ Docker build failed:\n{result.stderr}"
        
        cpp_file = os.path.join(docker_build_path, docker_cpp_file)
        if os.path.exists(cpp_file):
            os.remove(cpp_file)

        output_file_path = os.path.join(docker_build_path, docker_so_file)
        if not os.path.exists(output_file_path):
            return f"⚠️ Build completed but .so file not found at expected path: {output_file_path}"

        return f"✅ .so file built successfully: {output_file_path}"



@tool
def generate_extension_cross_platform(module_name: str = "cpp_module", platform: str = "linux") -> str:
    """
    Builds a Python extension file (.pyd on Windows, .so on Linux) from the converted C++ code.
    Uses MSVC `cl` on Windows and Docker on Linux.
    """
    return _generate_extension_cross_platform(module_name, platform) 