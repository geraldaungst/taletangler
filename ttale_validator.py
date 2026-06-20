#!/usr/bin/env python3
"""
ttale_validator.py

Description: A standalone script to validate a TaleTangler story file and report any errors found.

Usage: 
"""
import argparse
from errors import story_exists, report_errors, ErrText
from story_models import Story
from story_parser import StoryParser, Mode


def confirm_endings(story: Story, story_parser: StoryParser) -> None:
    story_endings = 0
    for scene_tag, scene in story.scenes.items():
        for choice in scene.choices:
            # Counting the number of story endings in the file
            if choice.next_scene == "theend":
                story_endings += 1
            # Choice points to a nonexistent scene
            elif choice.next_scene not in story.scenes and choice.next_scene != "no-destination":
                story_parser.handle_error(ErrText.INVALID_DESTINATION, scene_tag)
    if story_endings == 0:
        story_parser.handle_error(ErrText.NO_ENDINGS, "(STORY_LEVEL)")


def validate_story(story: Story, story_parser: StoryParser, start_scene: str) -> bool:
    confirm_endings(story, story_parser)
    return True     # Will eventually return False if any problems are found


def main():
    # Open and process the story file
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("story_file", type=story_exists)
    arg_parser.add_argument("-w", "-v", "--writer", "--verbose", action="store_true")
    # TODO: Consider adding --debug mode for giving debugging output to developer
    # arg_parser.add_argument("-d", "--debug", action="store_true")
    args = arg_parser.parse_args()
    verbose_mode = False
    if args.writer:
        parser_mode = Mode.WRITER
        verbose_mode = True
    else:
        parser_mode = Mode.VALIDATE
    story_parser = StoryParser(parser_mode)
    story = story_parser.process_story(args.story_file)
    start_scene = next(tag for tag, scene in story.scenes.items() if scene.starting_scene)
    if not story_parser.errors:
        validate_story(story, story_parser, start_scene)
    report_errors(story_parser.errors, story_parser.notes, verbose_mode)

if __name__ == "__main__":
    main()
