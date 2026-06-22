# Getting Started with TaleTangler

TaleTangler runs in the terminal and requires Python 3. Here's how to get it
running on your computer.

## Quick Start

1. Install Python 3 if you don't already have it.
2. Download the project from GitHub (green **Code** button → **Download ZIP**), then unzip it.
3. Open a terminal and navigate to the folder.
4Run a story:
   ```
   python taletangler.py stories/example.ttale
   ```

---

## Detailed Instructions

### Step 1 — Check whether Python is already installed

**Mac:**
Open the Terminal app (find it in Applications → Utilities, or search with
Spotlight). Type the following and press Return:
```
python3 --version
```
If you see a version number (e.g. `Python 3.12.0`), Python is already
installed. Skip to Step 2.

**Windows:**
Open Command Prompt (search for `cmd` in the Start menu). Type the following
and press Enter:
```
python --version
```
If you see a version number, Python is already installed. Skip to Step 2.

---

### Step 2 — Install Python (if needed)

Go to [python.org/downloads](https://www.python.org/downloads/) and download
the installer for your operating system.

**Mac:** Open the downloaded `.pkg` file and follow the installer prompts.

**Windows:** Open the downloaded `.exe` file. **Important:** on the first
screen of the installer, check the box that says **"Add Python to PATH"**
before clicking Install. This makes Python available from the command line.

When the installation is complete, repeat Step 1 to confirm Python is working.

---

### Step 3 — Download TaleTangler

1. Go to the [TaleTangler repository on GitHub](https://github.com/geraldaungst/taletangler).
2. Click the green **Code** button near the top right of the page.
3. Click **Download ZIP**.
4. Find the downloaded ZIP file (usually in your Downloads folder) and unzip it.
   - **Mac:** Double-click the ZIP file.
   - **Windows:** Right-click the ZIP file and choose **Extract All**.

You should now have a folder called `taletangler-main` (or similar).

---

### Step 4 — Open a terminal in the TaleTangler folder

**Mac:**
1. Open Terminal (Applications → Utilities → Terminal).
2. Type `cd ` (with a space after it), then drag the TaleTangler folder from
   Finder into the Terminal window. Press Return.

**Windows:**
1. Open the TaleTangler folder in File Explorer.
2. Click in the address bar at the top of the window, type `cmd`, and press
   Enter. A Command Prompt window will open already in the right folder.

---

### Step 5 — Run TaleTangler

Type the following and press Return (Mac) or Enter (Windows):

**Mac:**
```
python3 taletangler.py stories/example.ttale
```

**Windows:**
```
python taletangler.py stories/example.ttale
```

You should see the opening scene of the example story. Use the number keys to
make choices and work your way through the story.

To play a different story, replace `stories/example.ttale` with the path to
any `.ttale` file.

---

### Troubleshooting

**"python: command not found" or "python3: command not found"**
Python isn't installed, or the installer didn't add it to your PATH. Return to
Step 2. Windows users: make sure you checked "Add Python to PATH" during
installation.

**"No such file or directory"**
Your terminal isn't in the TaleTangler folder. Return to Step 4.

---

<!-- PLACEHOLDER: When platformdirs is added as a dependency, insert a
"Step 3a — Install required packages" section here, between Steps 3 and 4,
with instructions for running: pip install platformdirs -->
