# Copyright (c) 2023, Manfred Moitzi
# License: MIT License
from __future__ import annotations
import pathlib
import dataclasses
import json

__all__ = ["setup_nodes"]

BYPASS = "bypass"
BYPASS_PROMPT = "{prompt}"


@dataclasses.dataclass
class Template:
    name: str
    positive_prompt: str = ""
    negative_prompt: str = ""

    def apply(
        self, positive: str, negative: str, apply_negative: bool = True
    ) -> tuple[str, str]:
        if apply_negative:
            negative += " " + self.negative_prompt
        return (
            self.positive_prompt.replace(BYPASS_PROMPT, positive),
            negative,
        )


BYPASS_TEMPLATE = Template(BYPASS, BYPASS_PROMPT)


def load_json_data(style_path: pathlib.Path) -> list:
    try:
        return json.loads(style_path.read_text(encoding="utf-8"))
    except (IOError, json.JSONDecodeError) as e:
        print(str(e))
        return []


def load_style_templates(style_path: pathlib.Path) -> dict[str, Template]:
    json_data = load_json_data(style_path)
    templates: dict[str, Template] = {}
    for record in json_data:
        if not isinstance(record, dict):
            continue
        template = Template(
            name=record.get("name", ""),
            positive_prompt=record.get("prompt", BYPASS_PROMPT),
            negative_prompt=record.get("negative_prompt", ""),
        )
        templates[template.name] = template
    templates[BYPASS] = BYPASS_TEMPLATE
    return templates


class ApplyStyle:
    TEMPLATES: dict[str, Template] = {}

    @classmethod
    def INPUT_TYPES(self):
        style_names = sorted(self.TEMPLATES.keys())
        try:
            style_names.remove(BYPASS)
        except ValueError:
            pass
        style_names.insert(0, BYPASS)

        return {
            "required": {
                "positive_prompt": ("STRING", {"multiline": True}),
                "negative_prompt": ("STRING", {"multiline": True}),
                "style": ((style_names),),
                "apply_negative_style": (
                    "BOOLEAN",
                    {"default": True, "label_on": "yes", "label_off": "no"},
                ),
                "log_prompt": (
                    "BOOLEAN",
                    {"default": False, "label_on": "yes", "label_off": "no"},
                ),
            }
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "positive_prompt",
        "negative_prompt",
    )
    FUNCTION = "apply_sdxl_style"
    CATEGORY = "mozman"

    def apply_sdxl_style(
        self,
        positive_prompt: str,
        negative_prompt: str,
        style: str,
        apply_negative_style: bool,
        log_prompt: bool,
    ):
        template = self.TEMPLATES.get(style, BYPASS_TEMPLATE)
        output_positive, output_negative = template.apply(
            positive_prompt, negative_prompt, apply_negative_style
        )
        if log_prompt:
            line = "-" * 79
            print(line)
            print(f"Style: '{style}' from class <{self.__class__.__name__}>")
            print(f"Input Positive: {positive_prompt}")
            print(f"Input Negative: {negative_prompt}")
            print(f"Output Positive: {output_positive}")
            print(f"Output Negative: {output_negative}")
            print(line)

        return output_positive, output_negative


NODE_DEFINITIONS = [
    ("sdxl_styles_sai.json", "Apply SDXL Style SAI"),
    ("sdxl_styles_twri.json", "Apply SDXL Style TWRI"),
    ("sdxl_styles_mre.json", "Apply SDXL Style MRE"),
    ("clipdrop_styles.json", "Apply ClipDrop Style"),
    ("fooocus.json", "Apply Fooocus Style"),
    ("art_styles_expansion.json", "Apply Art Style Expansion"),
    ("technical_documentation.json", "Apply Technical Documentation Style"),
]


def setup_nodes(
    class_mapping: dict[str, type], display_name_mapping: dict[str, str]
) -> None:
    cwd = pathlib.Path(__file__).parent
    for file_name, display_name in NODE_DEFINITIONS:
        templates = load_style_templates(cwd / "styles" / file_name)
        class_name = display_name.replace(" ", "")

        # create classes dynamically:
        class_mapping[class_name] = type(
            class_name, (ApplyStyle,), {"TEMPLATES": templates}
        )
        display_name_mapping[class_name] = display_name
