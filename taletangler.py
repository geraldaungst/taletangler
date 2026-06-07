#!/usr/bin/env python3
"""
taletangler.py

Description: Build your own choose-your-own-adventure-style stories. The program reads
lightly-formatted text files and presents them to the user as interactive stories.

Usage: taletangler.py [storyfile.txt]
"""
import argparse
from story_parser import Parser
from errors import story_exists


def present_reader_instructions():
    # TODO: Will eventually display instructions for the reader
    pass


def handle_story_ending():
    # TODO: Will eventually display any closing instructions or text
    pass


def main():
    # Open and process the story file
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("story_file", type=story_exists)
    arg_parser.add_argument("-d", "--debug", action="store_true")
    args = arg_parser.parse_args()
    if args.debug:
        parser_mode = "Verbose"
    else:
        parser_mode = "Normal"
    story_parser = Parser(parser_mode)
    story, cur_scene = story_parser.process_story(args.story_file)
    print(story)

"""All code below is future functionality. Currently in pseudocode.

    # Present story introduction and instructions
    present_reader_instructions()
    print(story.title)
    if story.instructions:
        pass    # This will be written later
    # Main game loop pseudocode
    while True:
        story.display_scene(cur_scene)
        reader_choice = story.get_reader_choice(cur_scene)
        cur_scene = story.handle_choice(cur_scene, reader_choice)
        if cur_scene == "theend":
            break
    handle_story_ending()
"""

if __name__ == "__main__":
    main()
