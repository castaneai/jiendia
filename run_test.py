#!/usr/bin/env python
import sys, os.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/src'))

import pytest
pytest.main('-x')