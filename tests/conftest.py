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

import os
import sys
from pathlib import Path

# Add metashade-mtlx to the path so we can import from it
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / 'metashade-mtlx'))

# Add MaterialX Python bindings from local build
materialx_python_path = repo_root / 'builds' / 'MaterialX' / 'installed' / 'python'
if materialx_python_path.exists():
    sys.path.insert(0, str(materialx_python_path))

# Set up test context with this directory
from util import testing

test_dir = Path(__file__).parent
testing.GlslTestContext.setup_class(test_dir)
