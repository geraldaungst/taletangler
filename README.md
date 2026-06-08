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

```bash
python taletangler.py path/to/your_story.txt
```

Two sample stories are included in the `stories/` folder to get you started.

---

## Writing a Story

Story files are plain text (`.txt`) with a simple structure.

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

Each choice needs exactly one `->` separating the prompt from the destination.
The destination must match another scene's tag.

### Endings

```
THE END
```

A line containing `THE END` marks an ending scene. Every story needs at least one.
A scene should either have choices or be an ending scene, but not both.

---

## Current Limitations

- No story validation yet — destination scene tags are not verified at load time
- Scenes that do not follow the formatting rules may create unexpected behavior; some errors will be caught, but others may not
- Terminal interface only
- No save or restore

---

## Planned Features

- **Story validation** — check for unreachable scenes, missing destinations,
  duplicate scene tags, and scenes with no exits before play begins
- **Improved error handling and reporting** — clearer messages for authors
  when a story file has formatting problems
- **Authoring guide** — a plain-language guide for student writers explaining
  the story file format with examples and common mistakes
- **Teacher guide** — classroom integration notes, workshop ideas, and tips
  for using TaleTangler as a writing tool
- **Web interface** — play stories in a browser instead of the terminal,
  making TaleTangler accessible to students without command line experience

---

## Feedback and Contributions

This project is in early development. If you try it out, feedback is welcome
via [GitHub Issues](../../issues). Bug reports, story format questions, and
feature suggestions are all fair game.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
