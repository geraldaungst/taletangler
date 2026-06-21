#!/usr/bin/env python3
"""
ttale_validator.py

Description: A standalone script to validate a TaleTangler story file and report any errors found.

Usage: 
"""
import argparse
import errors
from story_models import Story, SINK_NODES
from story_parser import StoryParser, Mode


def confirm_endings(story: Story, story_parser: StoryParser) -> bool:
    if not story.scenes:    # Story has no scenes
        story_parser.handle_error(errors.ErrText.EMPTY_STORY, "(STORY_LEVEL)")
        return False
    story_endings = 0
    confirmed = True
    for scene_tag, scene in story.scenes.items():
        for choice in scene.choices:
            # Counting the number of story endings in the file
            if choice.next_scene == "theend":
                story_endings += 1
            # Choice points to a nonexistent scene
            elif choice.next_scene not in story.scenes and choice.next_scene not in SINK_NODES:
                story_parser.handle_error(errors.ErrText.INVALID_DESTINATION, scene_tag)
                confirmed = False
    if story_endings == 0:
        story_parser.handle_error(errors.ErrText.NO_ENDINGS, "(STORY_LEVEL)")
        confirmed = False
    return confirmed


def dfs_recursive(story: Story, scene_tag: str, visited: set | None = None) -> None:
    if visited is None:
        visited = set(SINK_NODES)

    # Mark the current node as visited
    visited.add(scene_tag)
    story.scenes[scene_tag].connected = True

    # Recursively visit all unvisited neighbors
    for neighbor in story.scenes[scene_tag].choices:
        if neighbor.next_scene not in visited:
            dfs_recursive(story, neighbor.next_scene, visited)


def validate_story(story: Story, story_parser: StoryParser, start_scene: str) -> None:
    confirm_endings(story, story_parser)
    # Check for any self-loops: choices pointing back to the same scene
    # This does not prevent the story from running, but it warrants a note to the author
    for scene_tag, scene in story.scenes.items():
        for choice in scene.choices:
            if choice.next_scene == scene_tag:
                story_parser.notes.append(errors.TTError(
                    errors.ErrText.SELF_LOOP.code,
                    scene_tag,
                    None,  # Cannot figure out line number of self-loop
                    errors.ErrText.SELF_LOOP.value
                ))
    dfs_recursive(story, start_scene)
    # Produce a note for each scene that is not reachable from the starting scene
    for scene in story.scenes:
        if not story.scenes[scene].connected:
            story_parser.notes.append(errors.TTError(
                errors.ErrText.UNREACHABLE_SCENE.code,
                scene,
                None,   # Cannot figure out line number of unreachable scene
                errors.ErrText.UNREACHABLE_SCENE.value
            ))


def main():
    # Open and process the story file
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("story_file", type=errors.story_exists)
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
    # None below is a defensive fallback in case the story file has no starting scene to prevent an exception
    start_scene = next((tag for tag, scene in story.scenes.items() if scene.starting_scene), None)
    if start_scene is None: # Story has no starting scene
        story_parser.handle_error(errors.ErrText.NO_STARTING_SCENE, "(STORY_LEVEL)")
    elif not story_parser.errors:
        validate_story(story, story_parser, start_scene)
    errors.report_errors(story_parser.errors, story_parser.notes, verbose_mode)

if __name__ == "__main__":
    main()
