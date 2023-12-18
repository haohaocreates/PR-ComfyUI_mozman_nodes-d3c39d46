# Copyright (c) 2023, Manfred Moitzi
# License: MIT License
from __future__ import annotations
from . import apply_sdxl_style

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

NODE_CLASS_MAPPINGS: dict[str, type] = {}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {}

apply_sdxl_style.setup_nodes(NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS)