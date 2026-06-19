# TaleTangler
A choose-your-own-adventure story engine for young writers.

TaleTangler reads lightly-formatted plain text story files and presents them as interactive branching narratives in the terminal. It is designed so that anyone — including elementary students — can write a complete branching story without touching Python code.

---

## Requirements
- Python 3.x
- Mac, Linux, or Windows

No additional packages required.

---

## Usage

Play a story:
```bash
python taletangler.py path/to/your_story.ttale
```

Validate a story file before sharing it:
```bash
python ttale_validator.py path/to/your_story.ttale
```

Add `-w` or `--writer` for a full report with per-error detail and line numbers — useful when fixing problems:
```bash
python ttale_validator.py path/to/your_story.ttale --writer
```

Three sample stories are included in the `stories/` folder: `example.ttale`, `lighthouse.ttale`, and the longer `recess_at_last.ttale`.

---

## Story Files

Story files use the `.ttale` extension by convention, though the engine and validator also accept `.txt` files. Both formats are plain text — `.ttale` is just a signal that a file is ready to play.

---

## Writing a Story

Story files are plain text with a simple structure.

### Frontmatter
Optional. Anything before the first scene is ignored except:
```
title: Your Story Title
author: Your Name
```

### Scenes
Each scene has a tag, description text, and choices.

```
scene: Start
You stand at the edge of a dark forest. The trees are tall and old.
Choices:
- Go into the forest -> Deep Woods
- Turn back -> Village Square
---
```

- The scene tag is the scene's unique identifier. Case and punctuation are ignored when matching.
- The first scene in the file is always the starting scene.
- Scene separators (`---`, `===`, `***`) are optional but recommended.

### Choices
```
Choices:
- Choice text the reader sees -> Destination Scene Tag
```

Each choice needs exactly one `->` separating the prompt from the destination. The destination must match another scene's tag.

### Endings
```
THE END
```

A line containing `THE END` marks an ending scene. Every story needs at least one. A scene should either have choices or be an ending scene, but not both.

---

## Current Limitations
- Graph validation is not yet implemented — the validator checks for file formatting problems but does not yet verify that all destinations exist, detect unreachable scenes, or confirm that the story has at least one ending
- Terminal interface only

---

## Planned Features
- **Graph validation** — check for unreachable scenes, missing destinations, and scenes with no exits; confirm at least one ending exists
- **Save and restore** — resume a story in progress; saves are keyed by story identity (title and author) and stored in a platform-appropriate location using platformdirs
- **Authoring guide** — a plain-language guide for student writers explaining the story file format with examples and common mistakes
- **Teacher guide** — classroom integration notes, workshop ideas, and tips for using TaleTangler as a writing tool
- **Web interface** — play stories in a browser instead of the terminal, making TaleTangler accessible to students without command line experience

---

## Feedback and Contributions
This project is in early development. If you try it out, feedback is welcome via [GitHub Issues](../../issues). Bug reports, story format questions, and feature suggestions are all fair game.

---

## License
MIT License — see [LICENSE](LICENSE) for details.
