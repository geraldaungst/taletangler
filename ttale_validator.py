#!/usr/bin/env python3
"""
ttale_validator.py

Description: A standalone script to validate a TaleTangler story file and report any errors found.

Usage: 
"""
import argparse
from errors import TTError, ErrText, story_exists
from story_parser import StoryParser


def validate_story(story_file):
    pass


def main():
    # Open and process the story file
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("story_file", type=story_exists)
    arg_parser.add_argument("-w", "-v", "--writer", "--verbose", action="store_true")
    # TODO: Consider adding --debug mode for giving debugging output to developer
    # arg_parser.add_argument("-d", "--debug", action="store_true")
    args = arg_parser.parse_args()
    if args.debug:
        # Debug mode also includes all Verbose options, so -v is ignored if -d is also active
        parser_mode = "Debug"
    elif args.verbose:
        parser_mode = "Writer"
    else:
        parser_mode = "Validate"
    story_parser = StoryParser(parser_mode)
    story, cur_scene = story_parser.process_story(args.story_file)


if __name__ == "__main__":
    main()
