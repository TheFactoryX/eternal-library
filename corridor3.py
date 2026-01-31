"""
Corridor 3 - The Infinite Loop

In the depths of the Eternal Library,
a programmer debugs the universe.
"""

import anthropic
import os
import json
from datetime import datetime
from pathlib import Path

# Library configuration
MODEL = "glm-4.7"
TOME_ID = "tome_0004"
TOME_TITLE = "The Infinite Loop"
LANGUAGE = "en"

# Tome background
TOME_BACKGROUND = """
## The World

There is a program that contains everything.

Not a metaphor. A literal program—written in a language that predates all languages, running on hardware that might be the universe itself. Or the universe might be running on it. The distinction has ceased to matter.

Somewhere in this program, there is a bug. The program still runs—it has always run, it will always run—but something is wrong. Something has always been wrong.

## The Programmer

The narrator is a programmer. They do not remember when they started debugging. They do not remember what the program was supposed to do before the bug. They only know:

1. The bug exists
2. The bug must be found
3. The bug must be fixed

Each chapter is a log entry—part technical documentation, part philosophical meditation, part desperate prayer. The programmer documents their search through the codebase of reality.

## The Code

The program contains:
- Functions that call themselves (recursion into infinity)
- Variables that change when observed (quantum debugging)
- Comments written in languages that don't exist
- Error messages that are poems
- Stack traces that describe dreams
- Memory leaks that manifest as déjà vu

## Topics Explored

Through the debugging metaphor:
- Algorithms and their implications
- The nature of computation and consciousness
- Famous problems (P=NP, halting problem, entropy)
- The beauty and horror of infinite loops
- What it means to be a process running on unknown hardware

## Style

- Technical language mixed with existential dread
- Code snippets that are almost real
- Dry humor about impossible situations
- References to real computer science concepts
- Each entry ends with a new hypothesis or a deeper mystery
- The tone of someone who has been debugging for too long
"""

# Paths
STACKS_DIR = Path(__file__).parent / "stacks" / TOME_ID
READING_ROOM = Path(__file__).parent / "reading-room"


def get_client():
    """Summon the Librarian."""
    return anthropic.Anthropic(
        base_url=os.environ.get("ANTHROPIC_BASE_URL")
    )


def get_tome_metadata():
    """Read tome metadata."""
    tome_file = STACKS_DIR / "tome.json"
    if tome_file.exists():
        with open(tome_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "id": TOME_ID,
        "title": TOME_TITLE,
        "language": LANGUAGE,
        "pages": 0,
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
        "synopsis": "Debug logs from a programmer searching for a bug in the universe. The search never ends.",
        "background": TOME_BACKGROUND
    }


def save_tome_metadata(metadata):
    """Save tome metadata."""
    tome_file = STACKS_DIR / "tome.json"
    with open(tome_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def get_previous_pages(limit=5):
    """Get recent log entries for context."""
    metadata = get_tome_metadata()
    pages_content = []

    start = max(1, metadata["pages"] - limit + 1)
    for i in range(start, metadata["pages"] + 1):
        page_file = STACKS_DIR / f"page_{i:03d}.md"
        if page_file.exists():
            with open(page_file, "r", encoding="utf-8") as f:
                pages_content.append(f.read())

    return pages_content


def write_new_page():
    """Write a new debug log."""
    client = get_client()
    metadata = get_tome_metadata()

    new_page_num = metadata["pages"] + 1

    previous_pages = get_previous_pages(limit=5)
    background = metadata.get("background", TOME_BACKGROUND)

    if new_page_num == 1:
        prompt = f"""You are a programmer writing debug logs as you search for a bug in the program that is reality.

# Background

{background}

---

Write Log Entry #001.

This is your first documented attempt to locate the bug. Introduce your situation, your methodology, and your first observations about the codebase.

Requirements:
- Write in English
- 600-900 words
- Mix technical language with philosophical reflection
- Include pseudo-code snippets or error messages
- Reference real computer science concepts creatively
- End with a hypothesis or unsettling discovery"""
    else:
        context = "\n\n---\n\n".join(previous_pages)
        prompt = f"""You are a programmer writing debug logs as you search for a bug in the program that is reality.

# Background

{background}

---

# Previous Log Entries

{context}

---

Write Log Entry #{new_page_num:03d}.

Continue your investigation. Follow threads from previous entries, but discover something new. The bug remains elusive.

Requirements:
- Write in English
- 600-900 words
- Mix technical language with philosophical reflection
- Include pseudo-code snippets or error messages
- Reference real computer science concepts creatively
- Build on previous discoveries
- End with a new hypothesis or deeper mystery"""

    message = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = message.content[0].text

    page_file = STACKS_DIR / f"page_{new_page_num:03d}.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    page_content = f"""# Log Entry #{new_page_num:03d}

> Written at {timestamp}

---

{content}
"""

    with open(page_file, "w", encoding="utf-8") as f:
        f.write(page_content)

    metadata["pages"] = new_page_num
    metadata["updated_at"] = datetime.now().isoformat()
    save_tome_metadata(metadata)

    print(f"📖 Log #{new_page_num:03d} written in '{TOME_TITLE}'")
    return new_page_num


def update_library_index():
    """Update library index."""
    library_file = READING_ROOM / "library.json"

    if library_file.exists():
        with open(library_file, "r", encoding="utf-8") as f:
            library = json.load(f)
    else:
        library = {"tomes": [], "updated_at": None}

    metadata = get_tome_metadata()
    index_metadata = {k: v for k, v in metadata.items() if k != "background"}

    found = False
    for i, tome in enumerate(library["tomes"]):
        if tome["id"] == TOME_ID:
            library["tomes"][i] = index_metadata
            found = True
            break

    if not found:
        library["tomes"].append(index_metadata)

    library["updated_at"] = datetime.now().isoformat()

    with open(library_file, "w", encoding="utf-8") as f:
        json.dump(library, f, ensure_ascii=False, indent=2)

    print("📚 Library index updated")


def main():
    """The corridor's cycle."""
    STACKS_DIR.mkdir(parents=True, exist_ok=True)
    READING_ROOM.mkdir(parents=True, exist_ok=True)

    write_new_page()
    update_library_index()


if __name__ == "__main__":
    main()
