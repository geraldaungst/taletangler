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
    line: int | None
    text: str
    duplicate_choice_boundary: int | None = None


class ErrText(Enum):
    NO_ACTIVE_SCENE = "No active scene for description. Text cannot be added."
    NO_SCENE_TAG = "Scene is missing a scene tag. Placeholder was added instead."
    UNEXPECTED_FRONTMATTER = "Unexpected text before the 'Scene:' tag line. Text was ignored."
    APPEARS_LIKE_CHOICE = "Line appears to be a choice, but is not in the 'Choices:' section."
    MALFORMED_CHOICE = "Choice text not formatted correctly. Must begin with '-' and contain one '->'."
    # NO_CHOICES error was deprecated by the choice to add the DEAD_END note below
    # NO_CHOICES = "No choices were found for one or more scenes."
    DUPLICATE_CHOICES_SECTION = "Scene contains two 'Choices:' sections. All choices from the second section were included in the first."
    INLINE_CHOICE_ADDED = "Unexpected text after 'Choices:' appears to be a choice: added to choices list."
    INLINE_CHOICE_INVALID = "Unexpected text after 'Choices:' ignored: does not appear to be a choice."
    DUPLICATE_SCENE_TAG = "Duplicate scene tag found. File processing cannot continue until all tags are unique."
    INVALID_DESTINATION = "Invalid destination tag. Choice must lead to an existing scene."
    NO_ENDINGS = "No ending scene found. Story cannot end."
    SELF_LOOP = "Choice leads to the same scene."
    UNREACHABLE_SCENE = "No path of choices leads to this scene. Readers will never see it."
    DEAD_END = "Scene has no choices and no 'THE END'. The validator added an implied ending automatically."
    ENDING_WITH_CHOICES = "Scene contains 'THE END' and choices. Ending will be ignored so choices are offered to the reader."
    EMPTY_STORY = "Story file has no scenes. There is nothing to present to the reader."
    NO_STARTING_SCENE = "No starting scene found. Story cannot begin."

    @property
    def code(self):
        return self.name.lower()


class FileFormatError(ValueError):
    """Raised when a story file does not match the expected format."""


def story_exists(arg):
    story_file = Path(arg).expanduser().resolve()
    if not story_file.exists():
        raise argparse.ArgumentTypeError("Story file does not exist.")
    elif story_file.suffix.lower() not in (".txt", ".ttale"):
        raise argparse.ArgumentTypeError("Incorrect story file type. Must be plain text.")
    return story_file

def display_errors(error_list: list[TTError], error_type: str, verbose_mode: bool) -> None:
    if error_type == "error":
        header = (
            "\n========================================\n"
            "Critical errors found in the story file:\n"
            "========================================\n"
            "Errors below will prevent the story from running."
        )
        prefix = "Errors in scene"
    elif error_type == "note":
        header = (
            "\n=================\n"
            "Story file notes:\n"
            "=================\n"
            "Notes below are not critical errors, but will cause the story to not run as expected."
        )
        prefix = "Notes for scene"
    else:
        print(f"Unknown error type '{error_type}'. Validation failed.")
        return
    
    print(header)
    errors = sorted(error_list, key=lambda e: e.scene)
    if verbose_mode:
        scene_group = ""
        for error in errors:
            if error.scene != scene_group:
                scene_group = error.scene
                print(f"\n{prefix} {scene_group}:")
            if error.line:
                print(f"    Line {error.line}", end="")
            if error.duplicate_choice_boundary is not None:
                print(
                    f", (extra choices begin with choice {error.duplicate_choice_boundary})",
                    end="",
                )
            print(f": {error.text} ")
    else:
        error_counter = Counter(error.type for error in errors)
        print(f"Total {error_type}s: {len(errors)}")
        print(f"Number of {error_type}s by type:")
        for error_code, count in error_counter.items():
            print(f"{error_code}: {count} {error_type}s")
        print("Run with --writer to see individual details.")


def report_errors(error_list: list[TTError], note_list: list[TTError], verbose_mode: bool) -> None:
    if not error_list and not note_list:
        print("No errors or problems found in the story file.")
        return
    if error_list:
        display_errors(error_list, "error", verbose_mode)
        if note_list and not verbose_mode:
            print("Additional non-critical notes also found.")
            print("Fix critical errors first, or use --writer to see all details.")
            return
    if note_list:
        display_errors(note_list, "note", verbose_mode)
