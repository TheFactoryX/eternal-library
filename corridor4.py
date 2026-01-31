"""
Corridor 4 - The Wanderer's Atlas

In the depths of the Eternal Library,
postcards arrive from nowhere.
"""

import anthropic
import os
import json
from datetime import datetime
from pathlib import Path
import random

# Library configuration
MODEL = "glm-4.7"
TOME_ID = "tome_0005"
TOME_TITLE = "The Wanderer's Atlas"
LANGUAGE = "en"

# Tome background
TOME_BACKGROUND = """
## The World

There is a traveler who has been everywhere.

Not everywhere on Earth—everywhere. Places that exist. Places that don't. Places that used to exist. Places that might exist. Places that exist only when observed. The traveler sends postcards.

The postcards arrive at the library with no return address. Some are water-damaged. Some smell of spices or smoke or salt. Some are written in languages that shift as you read them. But they all describe a place, and they all are signed simply: "The Wanderer."

## The Wanderer

We know little about them:
- They have been traveling for longer than memory
- They cannot or will not return
- They find beauty in the strangest places
- They are lonely but content
- They write to someone, anyone, everyone

## The Places

Each postcard describes a location:
- Real places rendered strange (a Tokyo that exists only at 3am)
- Impossible geographies (the mountain that is also a whale)
- Historical places that never stopped existing
- Future places that already feel nostalgic
- Conceptual places (the border between two thoughts)

The descriptions blend:
- Geography and geology
- Local customs and cuisine
- Flora and fauna (real and imagined)
- The feeling of being there
- Small encounters with locals

## Style

- Postcard format: direct address to "Dear Friend"
- Vivid sensory details
- Matter-of-fact about impossibilities
- Specific place names (invented but convincing)
- Local words and phrases
- Wistful but not sad
- Each postcard ends with where they're heading next
- Always signs off: "Wish you were here. — The Wanderer"
"""

# Paths
STACKS_DIR = Path(__file__).parent / "stacks" / TOME_ID
READING_ROOM = Path(__file__).parent / "reading-room"

# Regions to inspire locations
REGIONS = [
    "East Asia", "Southeast Asia", "South Asia", "Central Asia",
    "Middle East", "North Africa", "Sub-Saharan Africa", "East Africa",
    "Northern Europe", "Southern Europe", "Eastern Europe", "Western Europe",
    "North America", "Central America", "South America", "Caribbean",
    "Oceania", "Pacific Islands", "Arctic", "Antarctic",
    "Underwater", "Underground", "In the clouds", "Between places"
]


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
        "synopsis": "Postcards from a traveler visiting impossible places. Each card describes somewhere that may or may not exist.",
        "background": TOME_BACKGROUND
    }


def save_tome_metadata(metadata):
    """Save tome metadata."""
    tome_file = STACKS_DIR / "tome.json"
    with open(tome_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def get_previous_pages(limit=5):
    """Get recent postcards for context."""
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
    """Write a new postcard."""
    client = get_client()
    metadata = get_tome_metadata()

    new_page_num = metadata["pages"] + 1

    # Pick a region for inspiration
    region = random.choice(REGIONS)

    previous_pages = get_previous_pages(limit=5)
    background = metadata.get("background", TOME_BACKGROUND)

    if new_page_num == 1:
        prompt = f"""You are The Wanderer, writing postcards from impossible places.

# Background

{background}

---

Write your first postcard. You are somewhere inspired by {region}, but stranger.

Invent a place name. Describe where you are with vivid sensory detail. Include something impossible but presented as ordinary. End with where you're heading next and sign off.

Requirements:
- Write in English
- 400-600 words
- Postcard format: "Dear Friend," ... "Wish you were here. — The Wanderer"
- Invent a specific, convincing place name
- Include local details (food, customs, language fragments)
- One or two impossible elements, treated as normal
- End with your next destination"""
    else:
        context = "\n\n---\n\n".join(previous_pages[-3:])

        # Get recent destinations to avoid
        recent_regions = []
        for page in previous_pages[-5:]:
            for r in REGIONS:
                if r.lower() in page.lower():
                    recent_regions.append(r)

        # Prefer unvisited regions
        available = [r for r in REGIONS if r not in recent_regions]
        if available:
            region = random.choice(available)

        prompt = f"""You are The Wanderer, writing postcards from impossible places.

# Background

{background}

---

# Recent Postcards

{context}

---

Write postcard #{new_page_num}. You are now somewhere inspired by {region}, but stranger.

You mentioned where you were heading in your last postcard—you may have arrived there, or been diverted somewhere else entirely.

Requirements:
- Write in English
- 400-600 words
- Postcard format: "Dear Friend," ... "Wish you were here. — The Wanderer"
- Invent a new specific place name
- Include local details (food, customs, language fragments)
- One or two impossible elements, treated as normal
- Maybe reference something from a previous postcard
- End with your next destination"""

    message = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = message.content[0].text

    page_file = STACKS_DIR / f"page_{new_page_num:03d}.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    page_content = f"""# Postcard #{new_page_num:03d}

> Received at {timestamp}

---

{content}
"""

    with open(page_file, "w", encoding="utf-8") as f:
        f.write(page_content)

    metadata["pages"] = new_page_num
    metadata["updated_at"] = datetime.now().isoformat()
    save_tome_metadata(metadata)

    print(f"📖 Postcard #{new_page_num:03d} received in '{TOME_TITLE}'")
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
