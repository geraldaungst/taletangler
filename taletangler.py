#!/usr/bin/env python3
"""
taletangler.py

Description: Build your own choose-your-own-adventure-style stories. The program reads
lightly-formatted text files and presents them to the user as interactive stories.

Usage: taletangler.py [storyfile.txt]
"""
from pathlib import Path
import re
import argparse
from enum import Enum, auto
from parser import State, Mode, Parser, process_story
from story_models import Story, Scene, Choice
from errors import FileFormatError, story_exists, validate_story

def main():
    # Open and process the story file
    parser = argparse.ArgumentParser()
    parser.add_argument("story_file", type=story_exists)
    story_file = parser.parse_args()
    story, cur_scene = process_story(story_file)


    # Present story introduction and instructions
    present_reader_instructions()
    print(story_title)
    if story_instructions
    # Main game loop pseudocode
    while True:
        display_scene(story, cur_scene)
        reader_choice = get_reader_choice(story, cur_scene)
        cur_scene = handle_choice(story, cur_scene, reader_choice)
        if cur_scene == "theend":
            break
    handle_story_ending()

if __name__ == "__main__":
    main()
