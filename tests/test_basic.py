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

import pytest
import _base


class TestBasic:
    """Tests for the purple color generator function."""
    
    def test_dummy_purple(self):
        """Generate a simple purple color function."""
        ctx = _base.GlslMaterialXContext()
        
        with ctx as test_ctx:
            sh = test_ctx._sh
            func_name = 'dummy_purple'
            
            # Define the purple function
            with sh.function(func_name)(result=sh.Out(sh.RgbF)):
                sh.result = sh.RgbF((0.5, 0.0, 1.0))
            
            # Add as MaterialX node
            test_ctx.add_node(
                func_name=func_name,
                mx_doc_string='Metashade-generated dummy node that returns a purple color'
            )
