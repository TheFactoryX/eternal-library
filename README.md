# 📖 永恒图书馆

> *"图书馆是无限的，周期性的。"*
> — 博尔赫斯

---

在这里，书永远写不完。

每 15 分钟，图书管理员醒来。
在黑暗中，他们写下新的一页。
然后沉睡。然后醒来。然后继续。

---

## 书卷

### 《迷楼记》
一个人在不断变化的建筑中迷失。
每一章是一个新的房间。
永远找不到出口。

### *The Lighthouse Keeper's Letters*
灯塔守望者写给未知收件人的信。
每一章是一封信。
永远不会有回信。

---

## 阅览室

[eternal-library.vercel.app](https://eternal-library.vercel.app)

书页每 15 分钟生长一次。
网站自动更新。
永不停止。

---

## 走廊

| 走廊 | 书卷 | 语言 |
|------|------|------|
| corridor0.py | 迷楼记 | 中文 |
| corridor1.py | The Lighthouse Keeper's Letters | English |

---

## 架构

```
eternal-library/
├── corridor0.py          # 走廊 0
├── corridor1.py          # 走廊 1
├── stacks/               # 书库
│   ├── tome_0001/        # 《迷楼记》
│   │   ├── page_001.md
│   │   ├── page_002.md
│   │   └── tome.json
│   └── tome_0002/        # The Lighthouse Keeper's Letters
├── reading-room/         # 阅览室
│   ├── index.html
│   └── library.json
└── .github/workflows/
    └── corridor-switch.yml
```

---

## 轮回

GitHub Actions 每 15 分钟运行一次。

两条走廊同时工作。
两本书同时生长。
图书馆永远不会关闭。

---

**Strange people. Strange things.**

📧 hi@sdpkjc.com
