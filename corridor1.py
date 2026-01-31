"""
Corridor 1 - English Tome

In the depths of the Eternal Library,
the Librarian writes in darkness.
"""

import anthropic
import os
import json
from datetime import datetime
from pathlib import Path

# Library configuration
MODEL = "glm-4.7"
TOME_ID = "tome_0002"
TOME_TITLE = "The Lighthouse Keeper's Letters"
LANGUAGE = "en"

# Tome background (permanently stored in tome.json)
TOME_BACKGROUND = """
## The World

The lighthouse stands on a nameless island, far from any shore marked on maps.

The keeper does not remember arriving here. There was no boat, no journey—only the sudden awareness of being here, tending the light. Time passes strangely: days feel like hours, nights stretch into weeks. The keeper has stopped counting.

The sea around the island is not ordinary water. It changes color with no relation to the sky. Ships appear on the horizon that could not exist—vessels from other centuries, other worlds, perhaps other dreams. They never come close. They never respond to signals.

## The Keeper

The keeper writes letters to someone. Who? A lover left behind? A child never met? A version of themselves that escaped this place? The recipient is never named, because the keeper no longer remembers. But the act of writing is the only thing that feels real.

The keeper is neither young nor old. Gender is unspecified—perhaps forgotten, perhaps irrelevant. What remains: a voice, a longing, a duty to keep the light burning.

## The Lighthouse

The lighthouse has too many rooms. New doors appear; old ones vanish. The light at the top burns without fuel. Sometimes the keeper climbs the stairs and arrives somewhere else—a memory, a dream, a place that cannot be.

Objects appear: a photograph of strangers, a key that fits no lock, books in languages that don't exist, a music box that plays unfamiliar songs.

## The Letters

Each chapter is one letter. The letters describe:
- The sea and weather (always strange, always meaningful)
- Ships seen on the horizon (each one a mystery)
- Dreams and visions (bleeding into waking life)
- Discoveries within the lighthouse
- Fragments of memory (unreliable, contradictory)
- The act of writing itself

## Style

- First person, epistolary format
- Start with "Dear—" or similar address (the recipient unnamed)
- Melancholic but not despairing
- Poetic, rich in sensory detail
- Surreal elements treated as ordinary
- Each letter ends with something unresolved: a question, a sound, a glimpse
- Never a reply. Never an escape. But always hope.
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
        "synopsis": "Letters from a lighthouse keeper to an unknown recipient. Each chapter is a letter. There will never be a reply.",
        "background": TOME_BACKGROUND
    }


def save_tome_metadata(metadata):
    """Save tome metadata."""
    tome_file = STACKS_DIR / "tome.json"
    with open(tome_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def get_previous_pages(limit=5):
    """Get the last 5 pages for context."""
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
    """Write a new page."""
    client = get_client()
    metadata = get_tome_metadata()

    # New page number
    new_page_num = metadata["pages"] + 1

    # Get previous 5 pages
    previous_pages = get_previous_pages(limit=5)

    # Build prompt—always include full background
    background = metadata.get("background", TOME_BACKGROUND)

    if new_page_num == 1:
        prompt = f"""You are a mysterious author writing an endless book: "{TOME_TITLE}".

# Tome Background

{background}

---

Now, write the first letter.

This is the keeper's first letter—perhaps the first one ever written, or simply the first one that survives. The keeper describes their situation, the lighthouse, and why they have begun to write.

Requirements:
- Write in English
- 600-900 words
- Only the letter content, no chapter title
- Follow the style guide exactly
- End with something unresolved"""
    else:
        context = "\n\n---\n\n".join(previous_pages)
        prompt = f"""You are a mysterious author writing an endless book: "{TOME_TITLE}".

# Tome Background

{background}

---

# Previous Letters (last {len(previous_pages)})

{context}

---

Now, write Letter #{new_page_num}.

Requirements:
- Write in English
- 600-900 words
- Only the letter content, no chapter title
- Continue threads from previous letters, but introduce something new
- Reference details, objects, or mysteries from earlier letters
- Follow the style guide exactly
- End with something unresolved"""

    # Summon the Librarian
    message = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = message.content[0].text

    # Save the page
    page_file = STACKS_DIR / f"page_{new_page_num:03d}.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    page_content = f"""# Letter {new_page_num}

> Written at {timestamp}

---

{content}
"""

    with open(page_file, "w", encoding="utf-8") as f:
        f.write(page_content)

    # Update metadata
    metadata["pages"] = new_page_num
    metadata["updated_at"] = datetime.now().isoformat()
    save_tome_metadata(metadata)

    print(f"📖 Page {new_page_num:03d} written in '{TOME_TITLE}'")
    return new_page_num


def update_library_index():
    """Update library index."""
    library_file = READING_ROOM / "library.json"

    # Read existing index
    if library_file.exists():
        with open(library_file, "r", encoding="utf-8") as f:
            library = json.load(f)
    else:
        library = {"tomes": [], "updated_at": None}

    # Update current tome (without full background, only synopsis)
    metadata = get_tome_metadata()
    index_metadata = {k: v for k, v in metadata.items() if k != "background"}

    # Find or add
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
    # Ensure directories exist
    STACKS_DIR.mkdir(parents=True, exist_ok=True)
    READING_ROOM.mkdir(parents=True, exist_ok=True)

    # Write new page
    write_new_page()

    # Update index
    update_library_index()


if __name__ == "__main__":
    main()
