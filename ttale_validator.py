#!/usr/bin/env python3
"""
ttale_validator.py

Description: A standalone script to validate a TaleTangler story file and report any errors found.

Usage: 
"""
import argparse
from errors import story_exists, report_errors
from story_models import Story
from story_parser import StoryParser, Mode


def validate_story(story: Story, verbose_mode: bool):
    print("Story graph validation not yet implemented.")
    print("Report will include only story file errors.")
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
    story, cur_scene = story_parser.process_story(args.story_file)
    if not story_parser.errors:
        validate_story(story, verbose_mode)
    report_errors(story_parser.errors, story_parser.notes, verbose_mode)

if __name__ == "__main__":
    main()
