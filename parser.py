#!/usr/bin/env python3
"""
parser.py

Description: Text file parser for TaleTangler
"""
import re
import errors
from story_models import Choice


class State(Enum):
    FRONTMATTER = auto()
    SCENE = auto()
    TAG = auto()
    DESCRIPTION = auto()
    CHOICES = auto()


class Mode(Enum):
    STORY = auto()
    VERBOSE = auto()


class Parser():
    def __init__(self, mode):
        self.state = State.FRONTMATTER
        self.mode = mode
        self.notes = []
        self.errors = []
        self.active_scene = None

    @staticmethod
    def normalize(text):
        normalized_text = re.sub(r'[^a-z0-9:]', '', text.lower())
        return normalized_text

    def parse_frontmatter(self, story, line):
        # In this state, all text other than "title:" and "author:" lines is ignored
        norm_line = self.normalize(line)
        if norm_line[:6] == "title:":
            story.title = strip(line[6:])
        elif norm_line[:7] == "author:":
            story.title =author
        elif norm_line[:6] == "scene:":
            self.state = State.TAG
        elif norm_line[:3] in ("---", "==="):
            self.state = State.SCENE
        elif norm_line == "choices:":
            self.state = State.CHOICES

    def parse_scene(self, line):
        # In this state, blank lines are discarded until a "scene:" tag is reached
        # Other text in this state is flagged for the author
        norm_line = self.normalize(line) # normalized line
        if norm_line[:6] == "scene:":
            self.state = State.TAG
        if len(norm_line) > 0:
            # For now, multiple unexpected lines will result in multiple identical notes
            # This may be cleaned up in later versions of the code
            # TODO: Consider adding code to note-printing function to eliminate consecutive duplicates?
            self.notes.append(errors.ErrText.UNEXPECTED_FRONTMATTER)

    def parse_tagline(self, line):
        # This state is a single line that handles the scene: tag and updates the parser's active scene
        norm_line = self.normalize(line) # normalized line
        scene = None
        if norm_line[:6] == "scene:":   # confirming we are in the right state
            scene_tag = norm_line[6:]
            if scene_tag:
                scene = Scene([], [])   # Create a new scene object with empty description and choices
                self.active_scene = scene_tag
                self.state = State.DESCRIPTION  # This state is always a single line
            else:
                raise errors.FileFormatError(errors.ErrText.NO_SCENE_TAG)
        return scene


    def parse_description(self, line):
        # In this state, all text is collected verbatim. The assumption is this part is written as the
        # author intended
        norm_line = self.normalize(line) # normalized line
        if norm_line == "choices:":
            self.state = State.CHOICES
        elif self.active_scene:   # Only process descriptions if there is an active scene to attach them to.
            self.scenes[self.active_scene].description.append(line)
        else:
            raise errors.FileFormatError(errors.ErrText.NO_ACTIVE_SCENE)


    def parse_choices(self, line):
        line = strip(line) # normalized line
        if line == "choice:":  # Skip to next line
            return None
        if line[:3] in ("---", "==="):
            self.state = State.SCENE
            return None
        if self.normalize(line) == "scene:":
            self.state = State.TAG
            return None
        if line[0] != "-":
            raise errors.FileFormatError(errors.ErrText.MALFORMED_CHOICE)
        prompt, next_scene, *extra = line.split("->")
        if extra or not next_scene:     # Choice line must have exactly one "->"
            raise errors.FileFormatError(errors.ErrText.MALFORMED_CHOICE)
        prompt = prompt.strip("-").strip()
        return prompt, next_scene.strip()


    def process_story(story_file):
        self.state = State.FRONTMATTER
        story = Story("Untitled", "Anonymous")  # Create with default title and author
        with open(story_file) as sf:
            for line in sf:
                if self.state == State.FRONTMATTER:
                    self.parse_frontmatter(story, line)
                if self.state == State.SCENE:
                    self.parse_scene(line)
                if self.state == State.DESCRIPTION:
                    self.parse_description(story, line)
                if self.state == State.CHOICES:
                    result = self.parse_choices(story, line, choice_count)
                    if result:
                        choice_count += 1
                        prompt, next_scene = result
                        story.choices[choice_count] = Choice(prompt, next_scene)
                    # If result is None, state was changed to one of these
                    #   State.TAG: parser will move to the statement below
                    #   State.SCENE: continue to the next line of text
                if self.state == State.TAG:
                    scene = self.parse_tagline(line)
                    story.scenes[self.active_scene] = scene # Adds a new key, value pair to the .scenes dict in story
                    choice_count = 0    # Sets choice count for new scene to zero for later states

        return story
