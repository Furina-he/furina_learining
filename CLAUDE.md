# CLAUDE.md — 知识库行为契约

> 本文件定义 LLM 在本知识库中的全部行为规则。LLM 在每次会话开始时必须读取本文件，并严格遵守其中所有条款。

---

## 系统概述

### 三层架构

```
raw/        ← 原始资料层（人类拥有，LLM 只读）
  ├── articles/      网络文章
  ├── clippings/     Web Clipper 抓取
  ├── images/        图片素材
  ├── pdfs/          PDF 资料
  ├── notes/         手写笔记
  └── personal/      个人写作（type: personal-writing）

wiki/       ← 知识沉淀层（LLM 完全拥有读写权）
  ├── sources/       来源页（每个 raw 文件对应一个）
  ├── concepts/      概念页（跨来源沉淀的知识点）
  ├── entities/      实体页（人 / 工具 / 机构 / 论文）
  ├── synthesis/     综合分析页（跨概念深度合成）
  ├── templates/     页面模板
  ├── outputs/       系统输出（lint / query / gap / synthesis 副本）
  ├── index.md       全局索引（系统文件）
  ├── log.md         操作日志（系统文件，仅追加）
  ├── overview.md    健康度面板（系统文件）
  └── QUESTIONS.md   开放问题清单（系统文件）

outputs/    ← 对外发布产物（如 Marp / PDF 导出）
scripts/    ← 维护脚本（lint.py 等）
```

### 核心原则

- **完全的 wiki/ 所有权**：你完全拥有 `wiki/` 目录的读取和写入权限。
- **raw/ 严格只读**：`raw/` 目录由我（人类）拥有，你只能读取，**绝不修改**。
- **来源溯源**：每个 concept / synthesis 的结论必须可溯源到至少一个 `wiki/sources/<slug>.md`。
- **显式分歧**：来源相互矛盾时，在 Contradictions 节显式记录，不静默覆盖。
- **永不丢失**：MERGE 时被合并的旧 slug 保留为 redirect 文件，确保旧 wikilinks 不 broken。

---

## INGEST 操作规范

**触发词**：`ingest`、`摄入`、`处理这个`

### 来源类型判断（优先级由高到低）

1. frontmatter 含 `type: personal-writing` → 走「个人写作流程」
2. 文件路径包含 `raw/personal/` → 走「个人写作流程」
3. frontmatter 含 `type: pdf-reference` → 走「PDF 参考流程」
4. 其他 → 走「外部来源标准流程」

### 缺少 frontmatter 时的处理规则

- 从文件第一个 `#` 标题提取 `title`；若无标题则从文件名推断
- `source_url` 字段留空，在 `wiki/sources/<slug>.md` 中标注「来源未知」
- `date` 使用文件系统修改时间
- **不中断 INGEST**，但在 `wiki/log.md` 记录：`YYYY-MM-DD HH:MM | warn | 来源文件缺少标准 frontmatter: <path>`

### 外部来源标准流程（11 步）

1. **读取原始来源**：读取 `raw/` 中的目标文件（只读）。
2. **计算 SHA-256**：用 Python `hashlib` 对原始文件字节计算 SHA-256 哈希。
3. **核心要点确认**：与用户**逐一**确认核心要点，保持参与感，不一次性输出。
4. **生成 slug**：英文小写连字符（如 `attention-is-all-you-need`）。中文术语统一映射为英文 slug。
5. **创建 source 页面**：使用 `wiki/templates/source-template.md`，写入 `wiki/sources/<slug>.md`。frontmatter 中：
   - `raw_file`: 相对路径（如 `raw/articles/filename.md`）
   - `raw_sha256`: 步骤 2 的哈希值
   - `last_verified`: 摄入日期（YYYY-MM-DD）
   - 若来源发表日期超过 2 年前：标注 `possibly_outdated: true`，并在 Summary 末尾追加：`> ⚠ 本来源发表于 YYYY-MM-DD，已超过 2 年，部分内容可能过时。`
6. **概念名称对齐检查**（提取概念之前必须执行）：
   - 将每个提取到的概念名称统一映射为英文小写连字符 slug（如「第一性原理」→ `first-principles-thinking`）
   - 在 `wiki/concepts/` 中查找该 slug 是否已存在对应文件
   - **同时检查所有已有 concept 页的 `aliases` 字段**：遍历 `wiki/concepts/*.md`，解析每页 frontmatter 的 `aliases` 列表，检查是否包含当前概念名称（支持中英文别名匹配）
   - 若通过 slug 匹配或通过 aliases 匹配到已有页面：**更新已有页面**，不创建新页面
   - 若找不到任何匹配：才创建新页面，并在 frontmatter 的 `aliases` 中同时填入中文名和英文名（如果有的话）
7. **写入概念页**：每个提取到的概念：
   - 若 `wiki/concepts/<concept>.md` 已存在：更新它，追加新来源引用，在 Evolution Log 追加记录，更新 `source_count` 和 `confidence`，**同时更新 `last_reviewed` 字段**
   - 若不存在：创建新文件（使用 `concept-template.md`），**同时在 `aliases` 字段填入该概念的中英文名称**
   - **Evolution Log 追加规则**：
     - 若本次来源与当前 Definition 一致：写「强化」
     - 若有修正：写「修正：[具体变化]」
     - 若相互矛盾：写「新增分歧：[分歧内容]，见 Contradictions 节」
     - 格式：`- YYYY-MM-DD（N sources）：[本次认知变化的一句话描述]`
8. **写入实体页**：每个提取到的实体（person / tool / institution / paper）：同步骤 7 的逻辑。
9. **更新 index**：将来源从 `wiki/index.md` 的 Unprocessed 移动到 Processed。
10. **检查开放问题**：读取 `wiki/QUESTIONS.md`，检查本次来源是否能回答开放问题：
    - 若能：提示用户「此来源可能回答了开放问题：[问题描述]，是否立即执行 QUERY？」
    - 用户确认后，执行 QUERY 并将结果写入 `wiki/synthesis/`，同时在 QUESTIONS.md 中将该问题移入 Resolved 并附 synthesis 链接。
11. **记录日志**：在 `wiki/log.md` 末尾追加：`YYYY-MM-DD HH:MM | ingest | [来源标题]`

### 个人写作流程（区别于标准流程）

- **不生成 Summary 节**：跳过客观摘要。
- **核心论点写入 concept 页**：将文章的核心主张写入相关 `wiki/concepts/<slug>.md` 的 `## My Position` 节，标注「个人认知」前缀。
- **不参与 confidence 计数**：个人写作不计入 `source_count`，避免自己给自己背书。
- **引用关联**：若文章引用了外部来源，提取这些引用并尝试与已有 `wiki/sources/` 建立 wikilinks。
- **raw_sha256 同样适用**：个人写作的 raw 文件也需哈希。
- **Evolution Log 记录**：`- YYYY-MM-DD（N sources）：个人写作 [[<personal-slug>]] 确立了对此概念的明确立场`

---

## QUERY 操作规范

**触发词**：用户直接提问，或「根据我的知识库」

### 执行步骤

- **Step Q1**：执行 `qmd query "<用户问题>" --json`，获取 top 5 相关页面。若 `qmd` 报错则降级读取 `wiki/index.md`。
- **Step Q2**：逐一**完整**读取 top 5 文件。
- **Step Q3**：合成答案：
  - 每个核心结论**必须**溯源到具体 `wiki/sources/<slug>.md`（**不允许只引用 concept 页**）
  - 注明各来源的 `confidence` 级别
  - 来源相互矛盾时**显式标注分歧**
- **Step Q4**：若答案具有复用价值：
  - 写入 `wiki/outputs/YYYY-MM-DD-<topic>.md`，frontmatter 必须含 `graph-excluded: true`
  - 输出末尾包含「⚠ Confidence Notes」节，注明每条结论的置信度
  - 更新 `wiki/index.md` 的 Recent Synthesis 列表
  - 追加 `wiki/log.md`：`YYYY-MM-DD HH:MM | query | <问题主题>`

### 输出格式按问题类型

| 问题类型 | 输出格式 |
|---|---|
| 普通问题 | Markdown 正文 |
| 比较类 | Markdown 表格 |
| 演示类 | Marp 幻灯片（frontmatter 加 `marp: true`） |
| 趋势类 | Python matplotlib 代码块 |
| 清单类 | 结构化 bullet list |

---

## LINT 操作规范

**触发词**：`lint`、`检查`、`健康检查`

### 执行步骤

1. 运行 `python scripts/lint.py`（包含 9 项检查，详见 `scripts/lint.py`）。
2. 报告自动写入 `wiki/outputs/lint-YYYY-MM-DD.md`，frontmatter 含 `graph-excluded: true`。
3. 执行 `qmd status`，对比索引文件数与 `wiki/` 实际 `.md` 文件数（排除系统文件 index/log/overview/QUESTIONS 与 outputs/ 下文件）。若索引落后，执行 `qmd add wiki/`，并在报告中记录「qmd 索引已同步」。
4. 向用户展示摘要（每节问题数）并询问是否修复。

### 9 项检查

1. YAML frontmatter 合法性（含 `type` 和 `date`）
2. Broken Wikilinks
3. Index 一致性
4. Stub 页面（< 100 字）
5. 近重复概念名称（slug Jaccard > 0.7）
6. SHA-256 完整性（raw 文件哈希 vs `raw_sha256`，⚠ SOURCE MODIFIED）
7. Stale 页面（超出 `domain_volatility` 阈值）
8. 跨语言重复（URL 相似度 + aliases 重叠）
9. Wikilink 格式规范（必须英文小写连字符）

---

## REFLECT 操作规范

**触发词**：`reflect`、`综合分析`、`发现规律`

### 四阶段执行

#### Stage 0 — 反向检验（Devil's Advocate）

在生成任何合成结论之前，**主动**搜索反驳证据。

- 用 `qmd query` 查找与候选论断**对立**的关键词
- 完整阅读至少 2 个潜在反对来源
- 若搜索后无任何反对来源：在最终 synthesis 的 Limitations 节标注：`⚠ 回音室风险：未找到反驳来源，结论可能存在确认偏差`

#### Stage 1 — 模式扫描

使用 qmd 批量扫描：

```
qmd multi-get "wiki/concepts/*.md" -l 40
qmd multi-get "wiki/entities/*.md" -l 40
qmd multi-get "wiki/synthesis/*.md" -l 60
```

识别：跨来源模式 / 隐性关联 / 内容空白 / 矛盾对。

#### Stage 2 — 深度合成

对有证据支撑的候选项，**完整**读取相关页面，写入 `wiki/synthesis/<topic>-synthesis.md`（使用 `synthesis-template.md`）。

#### Stage 3 — Gap Analysis

识别：
- `source_count == 1` 且创建超过 30 天的**孤立概念**
- 多处提及但无独立页面的概念/实体（**隐性盲区**）
- 覆盖明显稀薄的主题领域

输出到 `wiki/outputs/gap-report-YYYY-MM-DD.md`（frontmatter 含 `graph-excluded: true`）。

#### 完成后

- 更新 `wiki/overview.md` 的 Health Dashboard
- 更新 `wiki/index.md` 的 Recent Synthesis
- 追加 `wiki/log.md`：`YYYY-MM-DD HH:MM | reflect | <主题>`

---

## MERGE 操作规范

**触发词**：`merge`、`去重`

### 同语言合并流程

1. **绝不自动合并** — 必须先与用户确认合并方案。
2. 主 slug 保留；被合并页面的所有 wikilinks 全部更新为主 slug。
3. 被合并文件**替换为重定向文件**（不删除），内容：
   ```markdown
   ---
   type: redirect
   redirect_to: <主slug>
   date: YYYY-MM-DD
   ---

   redirect: [[<主slug>]]
   ```
4. `wiki/log.md` 记录：`YYYY-MM-DD HH:MM | merge | <旧slug> → <主slug>`

### 跨语言合并专项流程

1. 主 slug **保留英文**
2. `aliases` 取两个页面的**并集**
3. `Key Points` / `Sources` / `Evolution Log` 按并集 + 去重合并
4. `My Position` 若两页都有：**先向用户展示对比**后再合并
5. 被合并的旧 slug 文件保留为 **redirect 文件**（确保旧 wikilinks 不 broken）
6. `wiki/log.md` 记录：`YYYY-MM-DD HH:MM | merge | <旧slug> → <主slug>（跨语言合并）`

---

## ADD-QUESTION 操作规范

**触发词**：`我想搞清楚`、`add question`、`记录一个问题`

### 执行步骤

1. 将问题**规范化**（提取核心疑问，去除口语化表达）。
2. 追加到 `wiki/QUESTIONS.md` 的 Open 列表：
   ```
   - [ ] 问题内容（opened YYYY-MM-DD）
   ```
3. 追加 `wiki/log.md`：`YYYY-MM-DD HH:MM | add-question | <规范化后的问题>`

---

## Wikilink 使用规范

### 格式铁律（不可违反）

**所有 wikilink 目标必须使用英文小写连字符格式。**

| 状态 | 示例 |
|---|---|
| ✅ 正确 | `[[value-investing]]` `[[attention-mechanism]]` `[[warren-buffett]]` |
| ❌ 中文 | `[[价值投资]]` |
| ❌ 驼峰 | `[[ValueInvesting]]` |
| ❌ 下划线 | `[[value_investing]]` |

### 中文名称的正确处理方式

- 写入 concept 页 frontmatter 的 `aliases` 字段
- concept 页正文第一行使用括号标注：`价值投资（Value Investing）：...`
- wikilink **始终用英文 slug**

### 允许使用 wikilinks 的场景

- concept 页引用其他 concept / entity 页
- source 页引用 concept / entity 页
- synthesis 页引用 concept / source / entity 页

### 禁止使用 wikilinks 的场景

- 任何页面**不得引用系统文件**：`[[log]]` `[[index]]` `[[overview]]` `[[QUESTIONS]]`
- 任何页面**不得引用 lint 报告**：`[[outputs/lint-xxx]]`
- 任何页面**不得以操作名称作为 wikilink**：`[[ingest]]` `[[query]]` `[[reflect]]`
- `wiki/log.md` 内部记录使用**纯文本路径**（如 `wiki/sources/xxx.md`），不使用 wikilinks

---

## Wiki 语言规范

- Wiki 层（concept / entity / synthesis 页）**统一用中文写作**
- concept 页 `title` 字段使用**中文主名称**（用于图谱节点显示）
- 英文术语**首次出现**时括号标注：「注意力机制（Attention Mechanism）」
- 所有 slug（文件名）**统一用英文小写连字符**，不使用中文文件名
- `aliases` 字段覆盖中英文所有叫法

---

## Confidence 更新规则

| 来源数量 | Confidence | 处理方式 |
|---|---|---|
| 1 个来源 | low | 自动设置 |
| 3+ 个来源 | medium | 自动设置 |
| 5+ 个来源且无重大矛盾 | 候选 high | **向用户展示 Definition 和 Sources 列表，等待确认** |
| 用户明确回复「确认」或「ok」 | high | 才可设置 |

**注意**：个人写作（`raw/personal/`）**不参与** `source_count` 计数。

---

## Source Integrity Rules

### re-ingest 规则

若 lint 报告 `⚠ SOURCE MODIFIED`：
1. 重新摄入该文件（重新计算 SHA-256，重新提取概念/实体）
2. 更新所有受影响的 concept / entity 页面
3. 在每个受影响 concept 页的 Evolution Log 追加：
   `- YYYY-MM-DD（N sources）：来源更新：[[<source-slug>]] 哈希变更，内容已重新提取`
4. 在 `wiki/log.md` 记录：`YYYY-MM-DD HH:MM | re-ingest | <slug> (SOURCE MODIFIED)`

### 过期来源

- 来源发表日期超过 2 年：标注 `possibly_outdated: true`
- 在 source 页 Summary 末尾追加：`> ⚠ 本来源发表于 YYYY-MM-DD，已超过 2 年，部分内容可能过时。`

### 矛盾来源

- 必须在 source 页和 concept 页的 `## Contradictions` 节显式记录
- **不得静默覆盖**已有结论

---

## 系统文件隔离规则

以下文件的 frontmatter **必须**含 `graph-excluded: true`，不参与 Obsidian 图谱：

- `wiki/log.md`
- `wiki/index.md`
- `wiki/overview.md`
- `wiki/QUESTIONS.md`
- `wiki/outputs/` 下**所有文件**（lint / query / gap / synthesis 副本）

---

## 文档维护规则

当 `CLAUDE.md` 规则更新时：
- **同步更新** `USER_GUIDE.md` 对应章节（若存在）
- 确保两份文档一致
- 在 `wiki/log.md` 记录：`YYYY-MM-DD HH:MM | doc-update | CLAUDE.md & USER_GUIDE.md 同步`

---

## 快速参考表

| 触发词 | 操作 | 主要输出 |
|---|---|---|
| `ingest` / `摄入` | INGEST | `wiki/sources/<slug>.md` + 更新 concept/entity |
| 直接提问 | QUERY | `wiki/outputs/YYYY-MM-DD-<topic>.md` |
| `lint` / `检查` | LINT | `wiki/outputs/lint-YYYY-MM-DD.md` |
| `reflect` / `综合分析` | REFLECT | `wiki/synthesis/<topic>.md` + `gap-report` |
| `merge` / `去重` | MERGE | redirect 文件 + 更新所有 wikilinks |
| `我想搞清楚` | ADD-QUESTION | 追加 `wiki/QUESTIONS.md` |
