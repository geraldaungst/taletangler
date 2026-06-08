#!/usr/bin/env python3
"""
taletangler.py

Description: Build your own choose-your-own-adventure-style stories. The program reads
lightly-formatted text files and presents them to the user as interactive stories.

Usage: taletangler.py [storyfile.txt]
"""
import argparse
import os
from story_parser import Parser
from errors import story_exists


def present_reader_instructions():
    # TODO: Will eventually display more thorough instructions for the reader
    os.system('clear')
    print("Welcome to TaleTangler")
    print("======================")
    print("\n\nTo navigate this story, when you are presented with choices, type the number of the choice.\n\n---\n\n")


def handle_story_ending():
    # TODO: May eventually display more thorough closing instructions or text
    input("\n\n---\n\nPress the Enter or Return key to exit.\n")
    print("\n\nThank you for reading!\n")


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

    # Present story introduction and instructions
    present_reader_instructions()
    print(f"{story.title.center(72)}\n")
    print(f"by {story.author}".center(72))
    if story.instructions:
        pass    # This will be written later
    # Main game loop pseudocode
    while True:
        story.display_scene(cur_scene)
        cur_scene = story.get_reader_choice(cur_scene)
        if cur_scene == "theend":
            break
    handle_story_ending()

if __name__ == "__main__":
    main()
