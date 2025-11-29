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

import inspect
import os
from pathlib import Path

from metashade.util.testing import get_test_func_name
from metashade_mtlx.generate import GlslGeneratorContext

class GlslTestContext(GlslGeneratorContext):
    @classmethod
    def setup_class(cls, test_dir: Path):
        cls._parent_dir = test_dir
        cls._out_dir = test_dir.parent / 'libraries'
        os.makedirs(cls._out_dir, exist_ok=True)

    def __init__(self):
        test_name = get_test_func_name()
        super().__init__(test_name, self._out_dir)
