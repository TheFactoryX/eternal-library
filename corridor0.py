"""
走廊 0 - 中文书卷

在永恒图书馆的深处，
图书管理员在黑暗中书写。
"""

import anthropic
import os
import json
from datetime import datetime
from pathlib import Path

# 图书馆配置
MODEL = "glm-4.7"
TOME_ID = "tome_0001"
TOME_TITLE = "迷楼记"
LANGUAGE = "zh"

# 书卷背景设定（永久存储在 tome.json 中）
TOME_BACKGROUND = """
## 世界观

这是一座不可能存在的建筑。

它没有名字，没有建造者，没有历史。它只是存在着——或许一直存在着。

建筑内部的空间不遵循欧几里得几何。走过一扇门，你可能进入一个比外面更大的房间。爬上一段楼梯，你可能到达比起点更低的地方。时间在这里也变得可疑：你在某个房间待了一整天，出来后发现才过了几分钟——或者相反。

## 主人公

叙述者是一个没有名字的人。他/她不记得自己是如何进入这座建筑的，也不记得外面的世界是什么样子。这些记忆像是被建筑本身吞噬了。

叙述者唯一确定的是：必须继续走下去。不是为了找到出口（出口可能并不存在），而是因为停下来会发生某种可怕的事情。这种恐惧没有来源，但绝对真实。

## 空间类型

建筑中的空间各不相同：
- 房间：有的空无一物，有的堆满了奇怪的物品
- 走廊：有的笔直延伸到视线尽头，有的不断转弯
- 楼梯：向上或向下，有时通向意想不到的地方
- 庭院：开放的空间，但抬头看不到天空，只有更多的建筑
- 地下室：潮湿、黑暗，藏着更古老的秘密
- 图书室：装满了无法阅读的书籍
- 其他：任何可以想象的空间，以及无法想象的空间

## 遭遇

有时叙述者会发现其他存在的痕迹：
- 脚印、指痕、划痕
- 留下的物品：钥匙、照片、字条
- 声音：远处的脚步、低语、音乐
- 影子：但从未直接见到另一个人

## 文风

- 第一人称叙述
- 诗意但克制
- 细节丰富，感官描写
- 不安但不恐怖
- 每一章结尾留下悬念或谜题
"""

# 路径
STACKS_DIR = Path(__file__).parent / "stacks" / TOME_ID
READING_ROOM = Path(__file__).parent / "reading-room"


def get_client():
    """召唤图书管理员。"""
    return anthropic.Anthropic(
        base_url=os.environ.get("ANTHROPIC_BASE_URL")
    )


def get_tome_metadata():
    """读取书卷元数据。"""
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
        "synopsis": "一个人在不断变化的建筑中迷失。每一章是一个新的房间。永远找不到出口。",
        "background": TOME_BACKGROUND
    }


def save_tome_metadata(metadata):
    """保存书卷元数据。"""
    tome_file = STACKS_DIR / "tome.json"
    with open(tome_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def get_previous_pages(limit=5):
    """获取最近的5个书页，作为上下文。"""
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
    """书写新的一页。"""
    client = get_client()
    metadata = get_tome_metadata()

    # 新页码
    new_page_num = metadata["pages"] + 1

    # 获取前5章
    previous_pages = get_previous_pages(limit=5)

    # 构建提示——始终包含完整背景
    background = metadata.get("background", TOME_BACKGROUND)

    if new_page_num == 1:
        prompt = f"""你是一位神秘的作家，正在书写一本永远不会结束的书：《{TOME_TITLE}》。

# 书卷背景设定

{background}

---

现在，请书写第一章。

这是叙述者进入建筑后的第一个空间。描写他/她的困惑、观察、以及继续前行的决定。

要求：
- 用中文书写
- 800-1200字
- 只写正文，不要写章节标题
- 严格遵循背景设定中的文风要求
- 结尾留下悬念，暗示更多空间等待探索"""
    else:
        context = "\n\n---\n\n".join(previous_pages)
        prompt = f"""你是一位神秘的作家，正在书写一本永远不会结束的书：《{TOME_TITLE}》。

# 书卷背景设定

{background}

---

# 前文回顾（最近 {len(previous_pages)} 章）

{context}

---

现在，请继续书写第 {new_page_num} 章。

要求：
- 用中文书写
- 800-1200字
- 只写正文，不要写章节标题
- 延续前文的故事线索，但进入一个新的空间
- 可以呼应之前章节中的细节、物品或谜题
- 严格遵循背景设定中的文风要求
- 结尾留下悬念或新的谜题"""

    # 召唤图书管理员
    message = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = message.content[0].text

    # 保存书页
    page_file = STACKS_DIR / f"page_{new_page_num:03d}.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    page_content = f"""# 第 {new_page_num} 章

> 书写于 {timestamp}

---

{content}
"""

    with open(page_file, "w", encoding="utf-8") as f:
        f.write(page_content)

    # 更新元数据
    metadata["pages"] = new_page_num
    metadata["updated_at"] = datetime.now().isoformat()
    save_tome_metadata(metadata)

    print(f"📖 书页 {new_page_num:03d} 已写入《{TOME_TITLE}》")
    return new_page_num


def update_library_index():
    """更新图书馆索引。"""
    library_file = READING_ROOM / "library.json"

    # 读取现有索引
    if library_file.exists():
        with open(library_file, "r", encoding="utf-8") as f:
            library = json.load(f)
    else:
        library = {"tomes": [], "updated_at": None}

    # 更新当前书卷信息（不包含完整背景，只保留摘要）
    metadata = get_tome_metadata()
    index_metadata = {k: v for k, v in metadata.items() if k != "background"}

    # 查找或添加
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

    print("📚 图书馆索引已更新")


def main():
    """走廊的轮回。"""
    # 确保目录存在
    STACKS_DIR.mkdir(parents=True, exist_ok=True)
    READING_ROOM.mkdir(parents=True, exist_ok=True)

    # 书写新页
    write_new_page()

    # 更新索引
    update_library_index()


if __name__ == "__main__":
    main()
