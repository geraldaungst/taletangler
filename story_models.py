#!/usr/bin/env python3
"""
story_models.py

Description: The models and data structures used by TaleTangler
"""
class Story:
    def __init__(self, title: str, author: str):
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

    def display_scene(self, cur_scene: str):
        print("---")
        for line in self.scenes[cur_scene].description:
            print(line)
        for option, choice in enumerate(self.scenes[cur_scene].choices, start=1):
            if choice.next_scene == "theend":
                print(f"{choice.prompt}")
            else:
                print(f"{option}: {choice.prompt}")
        print("\n")

    def get_reader_choice(self, cur_scene: str):
        choice = 0
        if self.scenes[cur_scene].choices[0].next_scene == "theend":
            return "theend"
        while True:
            try:
                choice = int(input("What do you do? "))
            except ValueError:
                print("Please enter the number of your choice.")
                continue
            if choice < 1 or choice > len(self.scenes[cur_scene].choices):
                print("That is not one of the choices.")
                continue
            break
        # Reader-facing numbers start at 1; list index starts at 0
        choice = choice - 1
        return self.scenes[cur_scene].choices[choice].next_scene


class Choice:
    def __init__(self, prompt: str, scene_tag: str):
        self.prompt = prompt
        self.next_scene = scene_tag

    def __repr__(self):
        return self.prompt + " -> " + self.next_scene


class Scene:
    def __init__(self, description: list[str], choices: list[Choice]):
        self.description = description
        self.choices = choices

    def __repr__(self):
        scene_strings = ["**SCENE START**", "\n".join(self.description)]
        for choice_num, choice in enumerate(self.choices, start=1):
            scene_strings.append(f"{choice_num}: {choice}")
        return "\n".join(scene_strings)
