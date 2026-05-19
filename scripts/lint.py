#!/usr/bin/env python3
"""
Knowledge Base Lint Script

执行 9 项检查并将报告写入 wiki/outputs/lint-YYYY-MM-DD.md：
1. YAML frontmatter 合法性
2. Broken Wikilinks
3. Index 一致性
4. Stub 页面（<100 字）
5. 近重复概念名称（slug Jaccard > 0.7）
6. SHA-256 完整性
7. Stale 页面（超出 volatility 阈值）
8. 跨语言重复（URL 相似度 + aliases 重叠）
9. Wikilink 格式规范

用法：python scripts/lint.py
"""

import hashlib
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: 缺少 PyYAML。安装：pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
OUTPUTS = WIKI / "outputs"

VOLATILITY_DAYS = {"high": 90, "medium": 180, "low": 365}

SYSTEM_FILES = {"index.md", "log.md", "overview.md", "QUESTIONS.md"}
FORBIDDEN_WIKILINK_TARGETS = {
    "log", "index", "overview", "QUESTIONS",
    "ingest", "query", "reflect", "lint", "merge",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?(?:#[^\]]+)?\]\]")
SLUG_VALID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return {"__error__": str(e)}, text[m.end():]
    body = text[m.end():]
    return fm, body


def word_count(text: str) -> int:
    text_no_fm = FRONTMATTER_RE.sub("", text, count=1)
    cleaned = re.sub(r"```.*?```", "", text_no_fm, flags=re.DOTALL)
    cleaned = re.sub(r"`[^`]+`", "", cleaned)
    cleaned = re.sub(r"[#>\-*_\[\]()]", " ", cleaned)
    tokens = re.findall(r"\w+|[一-鿿]", cleaned)
    return len(tokens)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def jaccard(a: str, b: str) -> float:
    sa, sb = set(a.split("-")), set(b.split("-"))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def url_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    norm = lambda u: re.sub(r"^https?://(www\.)?", "", u.strip().rstrip("/")).lower()
    na, nb = norm(a), norm(b)
    if na == nb:
        return 1.0
    pa = set(re.split(r"[/?=&]", na))
    pb = set(re.split(r"[/?=&]", nb))
    if not pa or not pb:
        return 0.0
    return len(pa & pb) / len(pa | pb)


def collect_pages():
    pages = {}
    if not WIKI.exists():
        return pages
    for p in WIKI.rglob("*.md"):
        if "templates" in p.parts:
            continue
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        pages[rel] = {"path": p, "rel": rel, "text": text, "fm": fm or {}, "body": body, "slug": p.stem}
    return pages


def check_frontmatter(pages):
    issues = []
    for rel, page in pages.items():
        fm = page["fm"]
        if not fm:
            issues.append(f"- `{rel}`: 缺少 YAML frontmatter")
            continue
        if "__error__" in fm:
            issues.append(f"- `{rel}`: frontmatter YAML 解析失败 — {fm['__error__']}")
            continue
        if "type" not in fm:
            issues.append(f"- `{rel}`: frontmatter 缺少 `type` 字段")
        if "date" not in fm:
            issues.append(f"- `{rel}`: frontmatter 缺少 `date` 字段")
    return issues


def check_broken_wikilinks(pages):
    issues = []
    slugs = {Path(rel).stem for rel in pages}
    aliases_map = {}
    for rel, page in pages.items():
        for alias in page["fm"].get("aliases") or []:
            aliases_map[str(alias).strip()] = page["slug"]
    for rel, page in pages.items():
        for m in WIKILINK_RE.finditer(page["body"]):
            target = m.group(1).strip()
            target_slug = Path(target).stem
            if target_slug.startswith("<") or not target_slug:
                continue
            if target_slug in slugs:
                continue
            if target in aliases_map:
                continue
            issues.append(f"- `{rel}` → `[[{target}]]` 指向不存在的页面")
    return issues


def check_index_consistency(pages):
    issues = []
    index_rel = "wiki/index.md"
    if index_rel not in pages:
        return ["- `wiki/index.md` 不存在"]
    index_body = pages[index_rel]["body"]
    referenced = set()
    for m in WIKILINK_RE.finditer(index_body):
        referenced.add(Path(m.group(1).strip()).stem)
    existing_slugs = {Path(rel).stem for rel in pages}
    for ref in referenced:
        if ref.startswith("<") or not ref:
            continue
        if ref not in existing_slugs:
            issues.append(f"- `wiki/index.md` 引用了不存在的页面：`{ref}`")
    return issues


def check_stubs(pages):
    issues = []
    for rel, page in pages.items():
        name = Path(rel).name
        if name in SYSTEM_FILES or "outputs" in Path(rel).parts:
            continue
        wc = word_count(page["text"])
        if wc < 100:
            issues.append(f"- `{rel}`: 正文仅 {wc} 字符/词，疑似空壳页面")
    return issues


def check_near_duplicate_concepts(pages):
    issues = []
    concept_slugs = [Path(rel).stem for rel, p in pages.items()
                     if "concepts" in Path(rel).parts and p["fm"].get("type") == "concept"]
    seen = set()
    for i, a in enumerate(concept_slugs):
        for b in concept_slugs[i + 1:]:
            sim = jaccard(a, b)
            key = tuple(sorted([a, b]))
            if sim > 0.7 and key not in seen:
                seen.add(key)
                issues.append(f"- `{a}` ↔ `{b}`：slug Jaccard 相似度 {sim:.2f}，疑似重复概念")
    return issues


def check_sha256(pages):
    issues = []
    for rel, page in pages.items():
        if page["fm"].get("type") not in {"source", "personal-writing"}:
            continue
        raw_file = page["fm"].get("raw_file")
        expected = page["fm"].get("raw_sha256")
        if not raw_file or not expected:
            continue
        raw_path = ROOT / raw_file
        if not raw_path.exists():
            issues.append(f"- `{rel}`: raw_file `{raw_file}` 不存在")
            continue
        actual = sha256_of(raw_path)
        if actual != expected:
            issues.append(f"- ⚠ SOURCE MODIFIED — `{rel}`: raw_file 哈希不匹配（expected `{expected[:12]}...`, actual `{actual[:12]}...`）")
    return issues


def check_stale(pages):
    issues = []
    today = date.today()
    for rel, page in pages.items():
        if page["fm"].get("type") != "concept":
            continue
        volatility = page["fm"].get("domain_volatility", "medium")
        threshold = VOLATILITY_DAYS.get(volatility, 180)
        last_reviewed = page["fm"].get("last_reviewed") or page["fm"].get("updated") or page["fm"].get("date")
        if not last_reviewed:
            continue
        try:
            if isinstance(last_reviewed, date):
                lr = last_reviewed
            else:
                lr = datetime.strptime(str(last_reviewed)[:10], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            issues.append(f"- `{rel}`: last_reviewed 字段格式无效 (`{last_reviewed}`)")
            continue
        age = (today - lr).days
        if age > threshold:
            issues.append(f"- `{rel}`: {age} 天未审阅，volatility={volatility}（阈值 {threshold} 天）")
    return issues


def check_cross_language_duplicates(pages):
    issues = []
    sources = [(rel, p) for rel, p in pages.items() if p["fm"].get("type") == "source"]
    seen_pairs = set()
    for i, (rel_a, pa) in enumerate(sources):
        url_a = pa["fm"].get("source_url") or ""
        for rel_b, pb in sources[i + 1:]:
            url_b = pb["fm"].get("source_url") or ""
            sim = url_similarity(url_a, url_b)
            if sim > 0.7:
                key = tuple(sorted([rel_a, rel_b]))
                if key not in seen_pairs:
                    seen_pairs.add(key)
                    issues.append(f"- `{rel_a}` ↔ `{rel_b}`：source_url 相似度 {sim:.2f}，疑似同来源不同语言版本")

    concepts = [(rel, p) for rel, p in pages.items() if p["fm"].get("type") == "concept"]
    alias_to_pages = {}
    for rel, p in concepts:
        for alias in p["fm"].get("aliases") or []:
            alias_to_pages.setdefault(str(alias).strip().lower(), []).append(rel)
    for alias, pages_list in alias_to_pages.items():
        if len(pages_list) > 1:
            issues.append(f"- 别名 `{alias}` 同时出现在：{', '.join(pages_list)} — 疑似跨语言重复")
    return issues


def check_wikilink_format(pages):
    issues = []
    aliases_map = {}
    for rel, page in pages.items():
        for alias in page["fm"].get("aliases") or []:
            aliases_map[str(alias).strip()] = page["slug"]
    for rel, page in pages.items():
        if Path(rel).name in SYSTEM_FILES or "outputs" in Path(rel).parts:
            continue
        for m in WIKILINK_RE.finditer(page["body"]):
            raw_target = m.group(1).strip()
            target = Path(raw_target).stem
            if target.startswith("<") or not target:
                continue
            if target in FORBIDDEN_WIKILINK_TARGETS:
                issues.append(f"- `{rel}` → `[[{raw_target}]]` 引用系统文件或操作名，禁止使用 wikilink")
                continue
            if not SLUG_VALID_RE.match(target):
                if target in aliases_map:
                    issues.append(f"- `{rel}` → `[[{raw_target}]]` 使用别名而非英文 slug，应改为 `[[{aliases_map[target]}]]`")
                else:
                    issues.append(f"- `{rel}` → `[[{raw_target}]]` 格式不规范（应为英文小写连字符 slug）")
    return issues


def main():
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    pages = collect_pages()

    sections = [
        ("1. YAML Frontmatter 合法性", check_frontmatter(pages)),
        ("2. Broken Wikilinks", check_broken_wikilinks(pages)),
        ("3. Index 一致性", check_index_consistency(pages)),
        ("4. Stub 页面（< 100 字）", check_stubs(pages)),
        ("5. 近重复概念名称（Jaccard > 0.7）", check_near_duplicate_concepts(pages)),
        ("6. SHA-256 完整性", check_sha256(pages)),
        ("7. Stale 页面", check_stale(pages)),
        ("8. 跨语言重复检测", check_cross_language_duplicates(pages)),
        ("9. Wikilink 格式规范", check_wikilink_format(pages)),
    ]

    today_str = date.today().strftime("%Y-%m-%d")
    report_path = OUTPUTS / f"lint-{today_str}.md"

    total_issues = sum(len(s[1]) for s in sections)

    lines = [
        "---",
        "type: lint-report",
        f"date: {today_str}",
        "graph-excluded: true",
        f"total_issues: {total_issues}",
        f"total_pages_scanned: {len(pages)}",
        "---",
        "",
        f"# Lint Report — {today_str}",
        "",
        f"扫描页面数：**{len(pages)}**　|　发现问题：**{total_issues}**",
        "",
    ]
    for title, items in sections:
        lines.append(f"## {title}")
        lines.append("")
        if not items:
            lines.append("_✓ 无问题_")
        else:
            lines.extend(items)
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Lint 完成。报告：{report_path}")
    print(f"共扫描 {len(pages)} 个页面，发现 {total_issues} 个问题。")
    for title, items in sections:
        print(f"  {title}: {len(items)}")
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
