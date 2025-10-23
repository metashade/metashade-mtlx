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
from metashade.glsl import frag

class GeneratorContext:
    def __init__(self, doc, out_dir):
        self._doc = doc
        self._src_file_name = f'metashade.{self._file_extension}'
        self._src_path = out_dir / self._src_file_name

    def __enter__(self):
        self._file = open(self._src_path, 'w')
        self._sh = self._create_generator()
        return self._sh
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self._file.close()
            return False
        
        self._file.close()
        return True
    
    @abc.abstractmethod
    def _create_generator(self):
        pass

    def add_node(self, func_name : str, mx_doc_string : str):
        nodedef_name = f'ND_{func_name}'

        # Define the metashade node definition
        nodedef = self._doc.addNodeDef(
            name = nodedef_name,
            node = 'metashade',
            type = 'color3'     # TODO: derive from the function definition
        )
        nodedef.setDocString(mx_doc_string)

        # Define the node implementation for the Metashade node
        impl = self._doc.addImplementation(
            f'IM_{func_name}_{self._mx_generator_name}'
        )
        impl.setNodeDef(nodedef)
        impl.setTarget(self._mx_target_name)
        impl.setFile(self._src_file_name)
        impl.setFunction(func_name)
        impl.setDocString(
            f'{self._mx_target_name} implementation of {nodedef_name}'
        )

        # The output is automatically created when specifying the output type
        # in addNodeDef. Get the existing output to verify it exists
        output = nodedef.getOutput("out")
        if output:
            output.setDocString("The output")

class GlslGeneratorContext(GeneratorContext):
    _file_extension = 'glsl'
    _mx_target_name = 'genglsl'

    def _create_generator(self):
        return frag.Generator(self._file, '450')

def generate_purple(ctx : GeneratorContext) -> None:
    sh = ctx.sh
    func_name = 'mx_metashade_purple'

    with sh.function(func_name, result = sh.Out(sh.Float3)):
        # Generate purple color: vec3(0.5, 0.0, 1.0)
        result = sh.Float3(0.5, 0.0, 1.0)

    ctx.add_node(
        func_name = func_name,
        mx_doc_string = 'Metashade-generated dummy node '
                        'that returns a purple color'
    )

def generate(out_dir_path):
    print(f"MaterialX version: {mx.__version__}")

    # Delete the output directory in order to delete any stale files
    if os.path.exists(out_dir_path):
        shutil.rmtree(out_dir_path)
    os.makedirs(out_dir_path)

    # Create MaterialX document for node definitions
    doc = mx.createDocument()

    with GlslGeneratorContext(doc = doc, out_dir = out_dir_path) as ctx:
        generate_purple(ctx = ctx)

    # Write the MaterialX document to file
    mtlx_file_path = out_dir_path / "metashade.mtlx"
    mx.writeToXmlFile(doc, str(mtlx_file_path))
    
    print(f"Generated files:")
    print(f"  - {out_dir_path / 'metashade.glsl'}")
    print(f"  - {mtlx_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Generate MaterialX nodes and source code for them."
    )
     
    parser.add_argument("--out-dir", help = "Path to the output directory")
    args = parser.parse_args()

    generate(
        out_dir_path = Path(args.out_dir)
    )