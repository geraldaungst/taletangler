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

    def __repr__(self):
        story_strings = [self.title, self.author]
        story_strings.extend(["\n"] + self.instructions + ["\n"])
        for scene in self.scenes:
            story_strings.append(f"{self.scenes[scene]}")
        return "\n".join(story_strings)

    def display_scene(self, cur_scene):
        pass

    def get_reader_choice(self, cur_scene):
        pass

    def handle_choice(self, cur_scene, reader_choice):
        pass


class Scene:
    def __init__(self, description, choices):
        self.description = description
        self.choices = choices

    def __repr__(self):
        scene_strings = ["\n".join(self.description)]
        for choice_num, choice in enumerate(self.choices, start=1):
            scene_strings.append(f"{choice_num}: {choice}")
        return "\n".join(scene_strings)

class Choice:
    def __init__(self, prompt, scene_tag):
        self.prompt = prompt
        self.next_scene = scene_tag

    def __repr__(self):
        return self.prompt + " -> " + self.next_scene
