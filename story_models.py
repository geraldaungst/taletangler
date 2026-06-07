#!/usr/bin/env python3
"""
story_models.py

Description: The models and data structures used by TaleTangler
"""
class Story:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.instructions = []
        self.scenes = dict()

    def display_scene(self, cur_scene):
        pass

    def get_reader_choice(self):
        pass

    def handle_choice(self, cur_scene):
        pass


class Scene:
    def __init__(self, description, choices):
        self.description = description
        self.choices = choices


class Choice:
    def __init__(self, prompt, scene_tag):
        self.prompt = prompt
        self.next_scene = scene_tag
