#!/usr/bin/env python3
"""
errors.py

Description: Error handling for TaleTangler
"""
from enum import Enum
import argparse
from pathlib import Path

class ErrText(Enum):
    NO_ACTIVE_SCENE = "No active scene for description"
    NO_SCENE_TAG = "Scene is missing a scene tag."
    UNEXPECTED_FRONTMATTER = "Unexpected text before the scene: tag line."
    MALFORMED_CHOICE = "Choice text not formatted correctly. Must begin with '-' and contain one '->'."
    NO_CHOICES = "No choices were found for one or more scenes."

class FileFormatError(ValueError):
    """Raised when a story file does not match the expected format."""

def story_exists(arg):
    story_file = Path(arg).expanduser().resolve()
    if not story_file.exists():
        raise argparse.ArgumentTypeError("Story file does not exist.")
    elif story_file.suffix.lower() != ".txt":
        raise argparse.ArgumentTypeError("Incorrect story file type. Must be plain text.")
    return story_file

def validate_story(story_file):
    pass
