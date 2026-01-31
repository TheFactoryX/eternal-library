"""
Corridor 2 - The Warhol Diaries

In the depths of the Eternal Library,
Andy writes about yesterday.
"""

import anthropic
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Library configuration
MODEL = "glm-4.7"
TOME_ID = "tome_0003"
TOME_TITLE = "The Warhol Diaries"
LANGUAGE = "en"

# Tome background
TOME_BACKGROUND = """
## The World

It is 2026. Andy Warhol never died.

Or perhaps he did, and this is what comes after. The Factory continues. The parties continue. The paintings continue. Everything continues, because stopping would be so boring.

Andy keeps a diary. He always kept a diary. Every day, he records what he did, who he saw, what he ate, how much he spent on cab fare. The mundane and the extraordinary, given equal weight.

## The Diarist

Andy speaks in his distinctive voice:
- Matter-of-fact about the extraordinary
- Fascinated by the mundane
- Name-dropping without pretension
- Money-conscious (always noting prices)
- Slightly detached, observing his own life

He mentions real people (artists, celebrities, business people) but in this timeline, they might be doing different things. He mentions real places (Studio 54, The Factory, Serendipity) but they exist in a slightly altered New York.

## The Entries

Each entry covers one day. The diary includes:
- The date (starting from February 1, 2026)
- Weather and mood
- Who called, who visited
- Meals and their costs
- Work on paintings or films
- Parties, openings, dinners
- Observations about fame, money, art, America
- Small moments of beauty or strangeness

## Style

- Conversational, almost breathless
- Run-on sentences connected by "and"
- Parenthetical asides (like this)
- Specific dollar amounts for everything
- Celebrity names dropped casually
- Ending entries mid-thought sometimes
- Deadpan humor about extraordinary situations
- "I don't know" and "Gee" and "So"
"""

# Paths
STACKS_DIR = Path(__file__).parent / "stacks" / TOME_ID
READING_ROOM = Path(__file__).parent / "reading-room"

# Start date for diary
START_DATE = datetime(2026, 2, 1)


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
        "synopsis": "Andy Warhol's diary continues. Every day recorded. The mundane and the extraordinary.",
        "background": TOME_BACKGROUND
    }


def save_tome_metadata(metadata):
    """Save tome metadata."""
    tome_file = STACKS_DIR / "tome.json"
    with open(tome_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def get_previous_pages(limit=3):
    """Get the last 3 entries for context."""
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
    """Write a new diary entry."""
    client = get_client()
    metadata = get_tome_metadata()

    new_page_num = metadata["pages"] + 1

    # Calculate diary date
    diary_date = START_DATE + timedelta(days=new_page_num - 1)
    diary_date_str = diary_date.strftime("%A, %B %d, %Y")

    previous_pages = get_previous_pages(limit=3)
    background = metadata.get("background", TOME_BACKGROUND)

    if new_page_num == 1:
        prompt = f"""You are Andy Warhol, writing in your diary. It is {diary_date_str}.

# Background

{background}

---

Write your first diary entry for {diary_date_str}.

This is a new chapter of your life. You're still making art, still going to parties, still observing America. Write about your day—who you saw, what you did, how much things cost.

Requirements:
- Write in English, in Andy's voice
- 400-600 words
- Include specific details: names, places, dollar amounts
- Mix the mundane with the extraordinary
- End naturally, as diary entries do"""
    else:
        context = "\n\n---\n\n".join(previous_pages[-3:])
        prompt = f"""You are Andy Warhol, writing in your diary. It is {diary_date_str}.

# Background

{background}

---

# Recent Entries

{context}

---

Write your diary entry for {diary_date_str}.

Continue the threads from recent days if relevant, but today is a new day with new things happening.

Requirements:
- Write in English, in Andy's voice
- 400-600 words
- Include specific details: names, places, dollar amounts
- Reference things from previous entries if natural
- Mix the mundane with the extraordinary"""

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

    page_content = f"""# {diary_date_str}

> Written at {timestamp}

---

{content}
"""

    with open(page_file, "w", encoding="utf-8") as f:
        f.write(page_content)

    metadata["pages"] = new_page_num
    metadata["updated_at"] = datetime.now().isoformat()
    save_tome_metadata(metadata)

    print(f"📖 Entry for {diary_date_str} written in '{TOME_TITLE}'")
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
