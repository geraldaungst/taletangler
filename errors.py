#!/usr/bin/env python3
"""
errors.py

Description: Error handling for TaleTangler
"""
from enum import Enum
import argparse
from pathlib import Path
from dataclasses import dataclass

@dataclass
class TTError:
    type: str
    scene: str
    line: int
    text: str
    duplicate_choice_boundary: int | None = None



class ErrText(Enum):
    NO_ACTIVE_SCENE = "No active scene for description. Text cannot be added."
    NO_SCENE_TAG = "Scene is missing a scene tag. Placeholder was added instead."
    UNEXPECTED_FRONTMATTER = "Unexpected text before the 'Scene:' tag line. Text was ignored."
    APPEARS_LIKE_CHOICE = "Line appears to be a choice, but is not in the 'Choices:' section."
    MALFORMED_CHOICE = "Choice text not formatted correctly. Must begin with '-' and contain one '->'."
    NO_CHOICES = "No choices were found for one or more scenes."
    DUPLICATE_CHOICES_SECTION = "Scene contains two 'Choices:' sections. All choices from the second section were included in the first."
    INLINE_CHOICE_ADDED = "Unexpected text after 'Choices:' appears to be a choice: added to choices list."
    INLINE_CHOICE_INVALID = "Unexpected text after 'Choices:' ignored: does not appear to be a choice."

    @property
    def code(self):
        return self.name.lower()

class FileFormatError(ValueError):
    """Raised when a story file does not match the expected format."""

def story_exists(arg):
    story_file = Path(arg).expanduser().resolve()
    if not story_file.exists():
        raise argparse.ArgumentTypeError("Story file does not exist.")
    elif story_file.suffix.lower() != ".txt":
        raise argparse.ArgumentTypeError("Incorrect story file type. Must be plain text.")
    return story_file
