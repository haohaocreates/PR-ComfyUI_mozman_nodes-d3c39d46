# Copyright (c) 2023, Manfred Moitzi
# License: MIT License
from __future__ import annotations
import pathlib
import dataclasses
import json


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
TEMPLATE_FILES: dict[str, dict[str, Template]] = dict()


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
    return templates


class ApplyStyle:
    FILE: str = "styles.json"

    @classmethod
    def INPUT_TYPES(self):
        cwd = pathlib.Path(__file__).parent
        templates = load_style_templates(cwd / self.FILE)
        templates[BYPASS] = BYPASS_TEMPLATE
        TEMPLATE_FILES[self.FILE] = templates
        style_names = sorted(templates.keys())
        style_names.remove(BYPASS)
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
        templates = TEMPLATE_FILES.get(self.FILE, {})
        template = templates.get(style, BYPASS_TEMPLATE)
        output_positive, output_negative = template.apply(
            positive_prompt, negative_prompt, apply_negative_style
        )
        if log_prompt:
            print("-" * 79)
            print(f"Style: {style} from '{self.FILE}' file")
            print(f"Input Positive: {positive_prompt}")
            print(f"Input Negative: {negative_prompt}")
            print(f"Output Positive: {output_positive}")
            print(f"Output Negative: {output_negative}")
            print("-" * 79)

        return output_positive, output_negative


class ApplySDXLStyleSAI(ApplyStyle):
    FILE = "sdxl_styles_sai.json"


class ApplySDXLStyleTWRI(ApplyStyle):
    FILE = "sdxl_styles_twri.json"


class ApplySDXLStyleMRE(ApplyStyle):
    FILE = "sdxl_styles_mre.json"


class ApplyFooocusStyle(ApplyStyle):
    FILE = "fooocus.json"


class ApplyClipDropStyle(ApplyStyle):
    FILE = "clipdrop_styles.json"


class ApplyArtStyleExpansion(ApplyStyle):
    FILE = "art_styles_expansion.json"


NODE_CLASS_MAPPINGS = {
    "ApplySDXLStyleSAI": ApplySDXLStyleSAI,
    "ApplySDXLStyleTWRI": ApplySDXLStyleTWRI,
    "ApplySDXLStyleMRE": ApplySDXLStyleMRE,
    "ApplyClipDropStyle": ApplyClipDropStyle,
    "ApplyFooocusStyle": ApplyFooocusStyle,
    "ApplyArtStyleExpansion": ApplyArtStyleExpansion,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ApplySDXLStyleSAI": "Apply SDXL Style SAI",
    "ApplySDXLStyleTWRI": "Apply SDXL Style TWRI",
    "ApplySDXLStyleMRE": "Apply SDXL Style MRE",
    "ApplyClipDropStyle": "Apply ClipDrop Style",
    "ApplyFooocusStyle": "Apply Fooocus Style",
    "ApplyArtStyleExpansion": "Apply Art Style Expansion",
}
