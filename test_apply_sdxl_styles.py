# Copyright (c) , Manfred Moitzi
# License: MIT License
import pytest
import re

from .apply_sdxl_style import (
    NODE_CLASS_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS,
    NODE_DEFINITIONS,
)


def test_all_classes_created():
    assert len(NODE_CLASS_MAPPINGS) == len(NODE_DEFINITIONS)
    assert len(NODE_DISPLAY_NAME_MAPPINGS) == len(NODE_DEFINITIONS)


def test_valid_class_names():
    for name, cls in NODE_CLASS_MAPPINGS.items():
        assert name == cls.__name__
        assert re.fullmatch("[a-zA-Z_][a-zA-Z0-9_]*", name) is not None


def test_classes_have_templates():
    for cls in NODE_CLASS_MAPPINGS.values():
        assert len(cls.TEMPLATES) > 1


if __name__ == "__main__":
    pytest.main([__file__])
