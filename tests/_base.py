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

import abc
import inspect
import io
import os
import sys
from pathlib import Path

import MaterialX as mx
from metashade.glsl import frag
from metashade.util.tests import RefDiffer

from generate import GeneratorContext


class MaterialXTestContext(GeneratorContext):
    """Base context for generating MaterialX nodes with metashade generators in tests."""
    
    @classmethod
    def setup_class(cls):
        cls._parent_dir = Path(sys.modules[cls.__module__].__file__).parent
        
        # Output to the libraries directory at the repo root
        cls._out_dir = cls._parent_dir.parent / 'libraries'
        
        # Reference directory for comparing outputs
        ref_dir = cls._out_dir
        
        out_dir = os.getenv('METASHADE_PYTEST_OUT_DIR', None)
        if out_dir is not None:
            # If output dir is specified, enable comparison against references
            cls._out_dir = Path(out_dir).resolve()
            cls._ref_differ = RefDiffer(ref_dir)
        else:
            cls._ref_differ = None
        
        os.makedirs(cls._out_dir, exist_ok=True)
    
    @staticmethod
    def _get_test_func_name():
        for frame in inspect.stack():
            if frame.function.startswith('test_'):
                return frame.function
        raise RuntimeError('No test function found in the stack')
    
    def __init__(self):
        test_name = self._get_test_func_name()
        self._src_file_name = f'{test_name}.{self._file_extension}'
        self._src_path = self._out_dir / self._src_file_name
        self._mtlx_path = self._out_dir / f'{test_name}.mtlx'
        self._doc = mx.createDocument()
    
    def validate_document(self):
        """Validate the MaterialX document."""
        valid, errors = self._doc.validate()
        if not valid:
            raise ValueError(f"MaterialX document validation failed:\n{errors}")
        return True
    
    def _check_files(self):
        """Check generated files against references if RefDiffer is configured."""
        if self._ref_differ is not None:
            self._ref_differ(self._src_path)
            self._ref_differ(self._mtlx_path)
    
    def __enter__(self):
        self._file = open(self._src_path, 'w')
        self._sh = self._create_generator()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self._file.close()
            return False
        
        self._file.close()
        
        # Write the MaterialX document
        mx.writeToXmlFile(self._doc, str(self._mtlx_path))
        
        # Validate the document
        self.validate_document()
        
        # Check against references if configured
        self._check_files()
        
        return True


class GlslMaterialXContext(MaterialXTestContext):
    """Context for generating GLSL MaterialX nodes."""
    
    @property
    def _file_extension(self):
        return 'glsl'
    
    @property
    def _mx_target_name(self):
        return 'genglsl'
    
    def _create_generator(self):
        return frag.Generator(self._file, glsl_version='')


# Initialize class method
MaterialXTestContext.setup_class()


class TestBase:
    """Base class for MaterialX metashade tests."""
    pass
