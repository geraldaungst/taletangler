#!/usr/bin/env python3
"""
story_parser.py

Description: Text file parser for TaleTangler

Usage: python3 ttale_validator.py <story_file.ttale> [-v --verbose -w --writer]

Note that --verbose and --writer are synonyms
"""
import re
import errors
from story_models import Story, Scene, Choice
from enum import Enum, auto

SCENE_SEPARATORS = ["---", "===", "***"]

class State(Enum):
    FRONTMATTER = auto()
    SCENE = auto()
    TAG = auto()
    DESCRIPTION = auto()
    CHOICES = auto()


class Mode(Enum):
    NORMAL = auto()
    VERBOSE = auto()
    VALIDATE = auto()
    WRITER = auto()


def looks_like_choice(line: str) -> bool:
    test_line = line.strip()
    return bool(test_line and test_line.startswith("-") and "->" in test_line)


class StoryParser:
    def __init__(self, mode: Mode):
        self.state = State.FRONTMATTER
        self.mode = mode
        self.notes = []
        self.errors = []
        self.active_scene = None
        self.active_choices_section = False
        self.cur_line = 0
        self.untagged_scene_count = 0
    
    def handle_error(self, this_error: errors.ErrText, scene: str | None = None) -> None:
        if self.mode == Mode.NORMAL:
            raise errors.FileFormatError(this_error.code)
        elif self.mode == Mode.VERBOSE:
            print(this_error.value)
            raise errors.FileFormatError(this_error.code)
        elif self.mode in (Mode.VALIDATE, Mode.WRITER):
            self.errors.append(
                errors.TTError(
                    this_error.code,
                    scene if scene is not None else self.active_scene,
                    self.cur_line,
                    this_error.value,
                )
            )
        else:  # There is a problem--unrecognized parser mode.
            raise ValueError(f"Unrecognized parser mode: {self.mode}")

    @staticmethod
    def normalize(text: str) -> str:
        normalized_text = re.sub(r'[^a-z0-9:]', '', text.lower())
        return normalized_text

    def parse_frontmatter(self, story: Story, line: str) -> None:
        # In this state, all text other than "title:" and "author:" lines is ignored
        # TODO: Future versions may add other frontmatter that gets captured instead of being ignored.
        #   Possibilities include:
        #   - Subtitle
        #   - Tagline
        #   - Copyright
        #   - Date written
        #   - Version
        #   - Preface
        #   - Instructions
        #   - Teacher, Course, Assignment details
        norm_line = self.normalize(line)
        if norm_line[:6] == "title:":
            story.title = line[6:].strip()
        elif norm_line[:7] == "author:":
            story.author = line[7:].strip()
        elif norm_line[:6] == "scene:":
            self.state = State.TAG
        elif line.strip()[:3] in SCENE_SEPARATORS:
            self.state = State.SCENE

    def parse_scene(self, line: str) -> None:
        # In this state, blank lines are discarded until a "scene:" tag is reached
        # Other text in this state is flagged for the author
        norm_line = self.normalize(line) # normalized line
        if norm_line[:6] == "scene:":
            self.state = State.TAG
        elif len(norm_line) > 0:
            # For now, multiple unexpected lines will result in multiple identical notes
            # Each line will be collected as a separate note for completeness, but reporting can be condensed
            self.notes.append(errors.TTError(
                errors.ErrText.UNEXPECTED_FRONTMATTER.code,
                self.active_scene,
                self.cur_line,
                errors.ErrText.UNEXPECTED_FRONTMATTER.value
            ))

    def parse_tagline(self, line: str) -> tuple[str, Scene]:
        # This state is a single line that handles the scene: tag and updates the parser's active scene
        norm_line = self.normalize(line) # normalized line
        scene_tag = norm_line[6:]
        scene = Scene([], [])  # Create a new scene object with empty description and choices
        if not scene_tag:
            self.untagged_scene_count += 1
            scene_tag = f"untagged-{self.untagged_scene_count:02d}"
            self.handle_error(errors.ErrText.NO_SCENE_TAG, scene_tag)
        self.state = State.DESCRIPTION  # This state is always a single line

        return scene_tag, scene


    def parse_description(self, story: Story, line: str) -> None:
        # In this state, all text is collected verbatim. The assumption is this part is written as the
        # author intended
        norm_line = self.normalize(line) # normalized line
        # The slice below ensures that a line with unexpected text after "choices:" is not ignored
        if norm_line in ["choices:", "theend"]:
            self.state = State.CHOICES
        elif norm_line == "scene:":
            self.state = State.TAG
        elif line.strip()[:3] in SCENE_SEPARATORS:
            self.state = State.SCENE
        elif self.active_scene:   # Only process descriptions if there is an active scene to attach them to.
            if norm_line[:8] == "choices:":
                if looks_like_choice(line[8:].strip()):
                    self.state = State.CHOICES
                    return  # Prevents adding this line to the description
                else:
                    self.notes.append(errors.TTError(
                        errors.ErrText.INLINE_CHOICE_INVALID.code,
                        self.active_scene,
                        self.cur_line,
                        errors.ErrText.INLINE_CHOICE_INVALID.value
                    ))
            elif looks_like_choice(line):
                self.notes.append(
                    errors.TTError(
                        errors.ErrText.APPEARS_LIKE_CHOICE.code,
                        self.active_scene,
                        self.cur_line,
                        errors.ErrText.APPEARS_LIKE_CHOICE.value,
                    )
                )
            story.scenes[self.active_scene].description.append(line.strip())
        else:
            self.handle_error(errors.ErrText.NO_ACTIVE_SCENE)


    def parse_choices(self, line: str, choice_count: int) -> tuple[str, str] | None:
        line = line.strip() # normalized line
        if line == "":  # Skip blank lines
            return None
        if self.normalize(line)[:8] == "choices:":  # Skip to next line
            if self.active_choices_section: # there is already a choices section in this scene
                self.notes.append(errors.TTError(
                    errors.ErrText.DUPLICATE_CHOICES_SECTION.code,
                    self.active_scene,
                    self.cur_line,
                    errors.ErrText.DUPLICATE_CHOICES_SECTION.value,
                    choice_count + 1    # The extra choices begin with the next choice line
                ))
                return None
            self.active_choices_section = True
            if line[8:]:    # Unexpected text after "choices:" will be processed as a choice
                self.handle_error(errors.ErrText.INLINE_CHOICE_ADDED)
                # The remaining text on this line will fall through to the rest of the parser
                line = line[8:].strip()
            else:   # "choices:" was by itself on the line and can be skipped
                return None
        if line[:3] in SCENE_SEPARATORS:
            self.active_choices_section = False
            self.state = State.SCENE
            return None
        if self.normalize(line)[:6] == "scene:":
            self.active_choices_section = False
            self.state = State.TAG
            return None
        if self.normalize(line) == "theend":
            self.active_choices_section = False
            return line, "theend"
        if not looks_like_choice(line):
            self.handle_error(errors.ErrText.MALFORMED_CHOICE)
            return None
        prompt, next_scene, *extra = line.split("->")
        next_scene = self.normalize(next_scene)
        if extra or not next_scene:     # Choice line must have exactly one "->"
            self.handle_error(errors.ErrText.MALFORMED_CHOICE)
            # Instead of assuming which scene tag is intended when more than one exists, assign "no-destination" instead
            next_scene = "no-destination"
        prompt = prompt.strip("-").strip()
        return prompt, next_scene


    def process_story(self, story_file: str) -> Story:
        self.state = State.FRONTMATTER
        story = Story("Untitled", "Anonymous")  # Create with default title and author
        has_starting_scene = False
        choice_count = 0
        with open(story_file) as sf:
            for line in sf:
                self.cur_line += 1
                if self.state == State.FRONTMATTER:
                    self.parse_frontmatter(story, line)
                if self.state == State.SCENE:
                    self.parse_scene(line)
                if self.state == State.DESCRIPTION:
                    self.parse_description(story, line)
                if self.state == State.CHOICES:
                    result = self.parse_choices(line, choice_count)
                    if result:    # If result is not None, it is a valid choice line
                        choice_count += 1
                        prompt, next_scene = result
                        story.scenes[self.active_scene].choices.append(Choice(prompt, next_scene, line_in_file=self.cur_line))
                    # If result is None, state was changed to one of these
                    #   State.TAG: parser will move to the statement below
                    #   State.SCENE: continue to the next line of text
                if self.state == State.TAG:
                    scene_tag, scene = self.parse_tagline(line)
                    scene.line_in_file = self.cur_line
                    if scene_tag in story.scenes:
                        self.handle_error(errors.ErrText.DUPLICATE_SCENE_TAG, scene_tag)
                        continue  # Any duplicate tags should be skipped
                    self.active_scene = scene_tag
                    story.scenes[self.active_scene] = scene # Adds a new key, value pair to the .scenes dict in story
                    if not has_starting_scene:   # First scene in the file is the starting scene
                        story.scenes[scene_tag].starting_scene = True
                        has_starting_scene = True
                    choice_count = 0    # Sets choice count for new scene to zero for later states
        return story

    def post_process(self, story: Story) -> None:
        for scene_tag, scene in story.scenes.items():
            # If there are no choices, add a default choice to the end of the scene
            if not scene.choices:
                self.notes.append(errors.TTError(
                    errors.ErrText.DEAD_END.code,
                    scene_tag,
                    scene.line_in_file,
                    errors.ErrText.DEAD_END.value
                ))
                scene.choices.append(Choice("(IMPLIED_ENDING)", "theend", line_in_file=scene.line_in_file))
            # Otherwise check for the presence of "theend" in choices along with other valid choices
            elif {"theend"} < {choice.next_scene for choice in scene.choices}:
                # Note that this scene has both "theend" and other valid choices
                # Ending will be removed from the graph to allow choices to proceed
                self.notes.append(errors.TTError(
                    errors.ErrText.ENDING_WITH_CHOICES.code,
                    scene_tag,
                    scene.line_in_file,
                    errors.ErrText.ENDING_WITH_CHOICES.value
                ))
                scene.choices = [choice for choice in scene.choices if choice.next_scene != "theend"]
