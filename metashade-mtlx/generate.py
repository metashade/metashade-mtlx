# Copyright 2025 Pavlo Penenko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
from pathlib import Path
import shutil

import MaterialX as mx

def get_purple_glsl_function():
    """
    Returns the GLSL code for the dummy purple function implemented in MaterialX.
    
    Returns:
        str: GLSL function code that outputs a purple color via parameter
    """
    return '''void mx_metashade_purple(out vec3 result)
{
    result = vec3(0.5, 0.0, 1.0); // Purple color
}'''

def generate(out_dir_path):
    print(f"MaterialX version: {mx.__version__}")

    # Delete the output directory in order to delete any stale files
    if os.path.exists(out_dir_path):
        shutil.rmtree(out_dir_path)
    os.makedirs(out_dir_path)
    
    # Generate the GLSL shader file
    with open(out_dir_path / "metashade.glsl", "w") as f:
        f.write(get_purple_glsl_function())
    
    # Create MaterialX document for node definitions
    doc = mx.createDocument()
    
    # Define the metashade node definition
    nodedef = doc.addNodeDef(name = "ND_metashade_purple", node = "metashade", type = "color3")
    nodedef.setDocString("Metashade-generated dummy node that returns a purple color")
    
    # The output is automatically created when specifying the output type in addNodeDef
    # Get the existing output to verify it exists
    output = nodedef.getOutput("out")
    if output:
        output.setDocString("Purple color output")
    
    # Define the GLSL implementation for the metashade node
    impl = doc.addImplementation("IM_metashade_purple_genglsl")
    impl.setNodeDef(nodedef)
    impl.setTarget("genglsl")
    impl.setFile("metashade.glsl")
    impl.setFunction("mx_metashade_purple")
    impl.setDocString("GLSL implementation of metashade node")
    
    # Write the MaterialX document to file
    mtlx_file_path = out_dir_path / "metashade.mtlx"
    mx.writeToXmlFile(doc, str(mtlx_file_path))
    
    print(f"Generated files:")
    print(f"  - {out_dir_path / 'metashade.glsl'}")
    print(f"  - {mtlx_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Generate MaterialX nodes and shader source code for them."
    )
     
    parser.add_argument("--out-dir", help = "Path to the output directory")
    args = parser.parse_args()

    generate(
        out_dir_path = Path(args.out_dir)
    )