# Athena-Revision 🏛️ - 項目規格

## 概述

Athena-Revision 是一個 AI 輔助的學習温習工具，專為 Athena 設計。

## 核心功能

### 1. 內容提取（Cui）
- 📸 拍攝書本頁面
- 🤖 Goblin AI 提取內容
- 📝 存入 Markdown 檔案

### 2. 題目生成（同步進行）
- 🤖 Goblin 分析內容
- 📋 生成多類型題目
- 💾 存入題庫 JSON

### 3. 練習模式（Athen）
- 🎲 從題庫隨機抽題
- 📝 多種題型練習
- 📊 即時反饋

---

## 系統架構

```
┌─────────────────┐
│  content/       │  ← 書本內容 (MD)
│  questions/     │  ← 題庫 (JSON)
└────────┬────────┘
         ↓
┌─────────────────┐
│  GitHub Repo    │
│  ebuddycheung   │
│  /Athena-Revision│
└────────┬────────┘
         ↓
┌─────────────────┐
│  GitHub Pages   │  ← 静态网站
│  (index.html)  │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Athena 温習   │
│  fetch() 讀題庫 │
└─────────────────┘
```

---

## 題庫格式 (JSON)

```json
{
  "subject": "chinese",
  "chapter": "p5_unit1_poetry",
  "title": "第一課：詠柳",
  "questions": [
    {
      "id": "ch_p5_1_001",
      "type": "mcq",
      "difficulty": "easy",
      "question": "《詠柳》的作者是誰？",
      "options": ["李白", "賀知章", "杜甫", "王維"],
      "answer": "賀知章",
      "explanation": "《詠柳》的作者是唐代詩人賀知章。"
    },
    {
      "id": "ch_p5_1_002",
      "type": "truefalse",
      "question": "《詠柳》是一首描寫夏天的詩。",
      "answer": false,
      "explanation": "《詠柳》描寫的是春天的景色。"
    },
    {
      "id": "ch_p5_1_003",
      "type": "fillblank",
      "question": "「二月春風___。」",
      "answer": "似剪刀",
      "explanation": "詩句「二月春風似剪刀」。"
    },
    {
      "id": "ch_p5_1_004",
      "type": "shortanswer",
      "question": "詩歌用了什麼修辭？有何好處？",
      "sampleAnswer": "用了比喻，把春風比作剪刀，生動形象。",
      "explanation": "這是比喻修辭。"
    }
  ]
}
```

---

## 題型

| 題型 | ID | 說明 |
|------|-----|------|
| 選擇題 | `mcq` | 四選一 |
| 是非題 | `truefalse` | True/False |
| 填空題 | `fillblank` | 填入答案 |
| 短答題 | `shortanswer` | 開放式答題 |

---

## 難度等級

| 等級 | 說明 |
|------|------|
| `easy` | 基礎記憶題 |
| `medium` | 理解應用題 |
| `hard` | 分析思考題 |

---

## 數據結構

```
Athena-Revision/
├── index.html              # 主介面
├── styles.css              # 樣式
├── app.js                  # 前端邏輯
├── content/                # 書本內容
│   ├── chinese/            # 中文科
│   │   └── p5_*.md
│   └── english/            # 英文科
│       └── p5_*.md
├── questions/              # 題庫
│   ├── chinese_*.json      # 中文題庫
│   └── english_*.json      # 英文題庫
├── SPEC.md                 # 規格文檔
└── README.md
```

---

## 工作流程

### 添加新內容（Cui 影書 → Goblin）

1. Cui 拍照發給 Goblin
2. Goblin 提取內容存入 `content/chinese/*.md`
3. Goblin 生成題目存入 `questions/chinese_*.json`
4. Push 到 GitHub
5. Athena 可以立即使用

### Athena 温習流程

1. 選擇科目（中文/英文/數學）
2. 選擇課文
3. 選擇題型
4. fetch() 從 GitHub 載入題庫
5. 隨機排序，取最多10題
6. 開始練習
7. 提交後顯示答案和解釋

---

## 已有的內容

### 中文科
- ✅ 第一課：詠柳（古詩）

### 英文科
- ✅ Unit 1: Our Environment

### 數學科
- ⏳ 即將推出

---

## 技術棧

- **前端**: HTML5 + CSS3 + Vanilla JS
- **存儲**: GitHub Repository
- **題庫**: JSON (GitHub Raw CDN)
- **AI**: Goblin (Claude-powered)

---

## 特色

- ✅ 繁體中文介面
- ✅ 響應式設計（手機/平板）
- ✅ 隨機題目（不會重複）
- ✅ 即時反饋和解釋
- ✅ 題庫與內容分離
- ✅ 易於擴展新內容

---

*Powered by Goblin 👺*
*Last Updated: 2026-03-26*
