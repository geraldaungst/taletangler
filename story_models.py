#!/usr/bin/env python3
"""
story_models.py

Description: The models and data structures used by TaleTangler
"""
class Story():
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.scenes = dict()


class Scene():
    def __init__(self, description, choices):
        self.description = description
        self.choices = choices


class Choice():
    def __init__(self, prompt, scene_tag):
        self.prompt = prompt
        self.next_scene = scene_tag
