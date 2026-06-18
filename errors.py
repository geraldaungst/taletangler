#!/usr/bin/env python3
"""
errors.py

Description: Error handling for TaleTangler
"""
from enum import Enum
import argparse
from pathlib import Path
from dataclasses import dataclass
from collections import Counter

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


def report_file_errors(error_list: list[TTError], verbose_mode: bool) -> None:
    print("Critical errors found in the story file:")
    print("========================================")
    print("Errors below will prevent the story from running. They are grouped by scene.")
    errors = sorted(error_list, key=lambda e: e.scene)
    if verbose_mode:
        scene_group = ""
        for error in errors:
            if error.scene != scene_group:
                scene_group = error.scene
                print(f"\nErrors in scene {scene_group}:")
            print(f"    Line {error.line}: {error.text}")
    else:
        error_counter = Counter(error.type for error in errors)
        print(f"Total errors found: {len(errors)}")
        scene_counter = Counter(error.scene for error in errors)
        print(f"Number of scenes with errors: {len(scene_counter)}")
        print("Number of errors by type:")
        for error_type, count in error_counter.items():
            print(f"    {error_type}: {count} errors")
        print("Run with --writer to see individual error details.")

def report_story_notes(note_list: list[TTError], verbose_mode: bool) -> None:
    print("Story file notes:")
    print("=================")
    print("Notes below are not critical errors, but will cause the story to not run as expected.")
    notes = sorted(note_list, key=lambda e: e.scene)
    if verbose_mode:
        scene_group = ""
        for note in notes:
            if note.scene != scene_group:
                scene_group = note.scene
                print(f"\nNotes for scene {scene_group}:")
            print(f"    Line {note.line}", end="")
            if note.duplicate_choice_boundary is not None:
                print(
                    f", (extra choices begin at line {note.duplicate_choice_boundary})",
                    end="",
                )
            print(f": {note.text} ")
    else:
        note_counter = Counter(note.type for note in notes)
        print(f"Total notes: {len(notes)}")
        print("Number of errors by type:")
        for note_type, count in note_counter.items():
            print(f"{note_type}: {count} notes")
        print("Run with --writer to see individual note details.")
