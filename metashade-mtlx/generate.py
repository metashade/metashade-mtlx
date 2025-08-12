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

def get_purple_glsl_function():
    """
    Returns the GLSL code for the dummy purple function implemented in MaterialX.
    
    Returns:
        str: GLSL function code that returns a purple color
    """
    return '''vec3 mx_metashade_purple()
{
    return vec3(0.5, 0.0, 1.0); // Purple color
}'''

def generate(out_dir_path):
    # Delete the output directory in order to delete any stale files
    if os.path.exists(out_dir_path):
        shutil.rmtree(out_dir_path)
    os.makedirs(out_dir_path)
    
    with open(out_dir_path / "metashade.glsl", "w") as f:
        f.write(get_purple_glsl_function())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Generate MaterialX nodes and shader source code for them."
    )
     
    parser.add_argument("--out-dir", help = "Path to the output directory")
    args = parser.parse_args()

    generate(
        out_dir_path = Path(args.out_dir)
    )