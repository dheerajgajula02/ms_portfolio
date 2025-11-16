#!/usr/bin/env python3
"""
Extract text from the resume PDF, create data.json, and generate index.html from
index.template.html. This is a one-time/static generator — run it whenever you
update the resume or `data.json` and it will overwrite `index.html`.

Designed to be minimal and run locally; no servers or extra runtime memory needed
to serve the generated static files.
"""
import json
import re
import os
from pathlib import Path

try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except Exception:
    PDF_AVAILABLE = False
    PdfReader = None


HERE = Path(__file__).resolve().parent
PDF_NAME = "Dheeraj_REsume (1).pdf"
PDF_PATH = HERE / PDF_NAME
TEMPLATE = HERE / "index.template.html"
OUT_HTML = HERE / "index.html"
DATA_JSON = HERE / "data.json"


def extract_pdf_text(path: Path) -> str:
    if not path.exists():
        return ""
    reader = PdfReader(str(path))
    pages = []
    for p in reader.pages:
        try:
            text = p.extract_text()
        except Exception:
            text = None
        if text:
            pages.append(text)
    return "\n\n".join(pages)


def find_email(text: str) -> str:
    m = re.search(r"[A-Za-z0-9.\-_+%]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", text)
    return m.group(0) if m else "your.email@example.com"


def find_name(text: str) -> str:
    # heuristic: first non-empty line that looks like a name (letters and spaces)
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        # skip lines that are all-caps section headers
        if s.upper() == s and len(s.split()) <= 6 and len(s) > 1:
            continue
        # otherwise take this as name if short
        if 2 <= len(s.split()) <= 4 and len(s) < 60:
            return s
    return "Dheeraj"


def split_sections(text: str):
    # Find common headings and slice text between them.
    headings = [
        "CONTACT",
        "EXPERIENCE",
        "PROJECTS",
        "TECHNICAL SKILLS",
        "SKILLS",
        "EDUCATION",
        "ACHIEVEMENTS",
        "SUMMARY",
        "ABOUT",
    ]
    text_upper = text.upper()
    found = []
    for h in headings:
        idx = text_upper.find(h)
        if idx != -1:
            found.append((idx, h))
    found.sort()
    sections = {}
    if not found:
        sections["about"] = text.strip()
        return sections

    # about: from start to first heading
    first_idx = found[0][0]
    sections["about"] = text[:first_idx].strip()
    for i, (idx, h) in enumerate(found):
        start = idx + len(h)
        end = found[i + 1][0] if i + 1 < len(found) else len(text)
        content = text[start:end].strip()
        key = h.lower().replace(" ", "_")
        sections[key] = content
    return sections


def to_html_paragraphs(s: str) -> str:
    if not s:
        return "<p></p>"
    parts = [p.strip() for p in re.split(r"\n{2,}", s) if p.strip()]
    html = "\n".join("<p>{}</p>".format(p.replace("\n", " ").strip()) for p in parts)
    return html


def skills_html(s: str) -> str:
    if not s:
        return "<p>—</p>"
    # split on commas or newlines or heavy whitespace
    parts = re.split(r"[,\n]+", s)
    parts = [p.strip() for p in parts if p.strip()]
    if not parts:
        return f"<p>{s}</p>"
    return "<p>" + ", ".join(parts) + "</p>"


def projects_html(s: str) -> str:
    if not s:
        return "<p>—</p>"
    # split heuristically by lines that look like project headers (lines with title-like formatting)
    items = [p.strip() for p in re.split(r"\n{2,}", s) if p.strip()]
    html_items = []
    for it in items:
        # make a short title from first line
        lines = [l.strip() for l in it.splitlines() if l.strip()]
        title = lines[0] if lines else "Project"
        body = " ".join(lines[1:]) if len(lines) > 1 else ""
        html_items.append(f"<h3>{title}</h3><p>{body}</p>")
    return "\n".join(html_items)


def main():
    # Load data.json if available; otherwise try to extract from PDF and create defaults
    if DATA_JSON.exists():
        print(f"Loading existing {DATA_JSON}")
        with open(DATA_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        raw = ""
        if PDF_AVAILABLE:
            raw = extract_pdf_text(PDF_PATH)
        if not raw:
            print("Warning: could not extract text from PDF. Using empty defaults.")
            raw = ""
        name = find_name(raw)
        email = find_email(raw)
        sections = split_sections(raw)
        data = {
            "name": name,
            "tag": "Minimal portfolio — fast, simple, old-school",
            "email": email,
            "resume_file": PDF_NAME,
            "About": sections.get("about", ""),
            "Projects": sections.get("projects", ""),
            "Technical Skills": sections.get("technical_skills", sections.get("skills", "")),
        }
        with open(DATA_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Wrote {DATA_JSON}")

    # Build content_html from the structured data (allow nested dicts / lists)
    def render_value(val):
        if isinstance(val, str):
            return to_html_paragraphs(val)
        if isinstance(val, list):
            items = "\n".join(f"<li>{item}</li>" for item in val)
            return f"<ul>\n{items}\n</ul>"
        if isinstance(val, dict):
            parts = []
            for sub_k, sub_v in val.items():
                parts.append(f"<h3>{sub_k}</h3>")
                parts.append(render_value(sub_v))
            return "\n".join(parts)
        # fallback
        return to_html_paragraphs(str(val))

    content_parts = []
    # preserve order by iterating items
    for key, value in data.items():
        if key.lower() in ("name", "tag", "email", "resume_file"):
            continue
        section_id = re.sub(r'[^a-zA-Z0-9_-]', '-', key).lower()
        # Special rendering for Technical Skills: wrap each subsection in a skill-group
        if key == "Technical Skills" and isinstance(value, dict):
            groups = []
            for sub_k, sub_v in value.items():
                groups.append(f"<div class=\"skill-group\"><h3>{sub_k}</h3>{render_value(sub_v)}</div>")
            group_html = "\n".join(groups)
            section_html = f"<section id=\"{section_id}\">\n  <h2>{key}</h2>\n  <div class=\"skill-grid\">\n{group_html}\n  </div>\n</section>"
            content_parts.append(section_html)
        else:
            content_parts.append(f"<section id=\"{section_id}\">\n  <h2>{key}</h2>\n  {render_value(value)}\n</section>")

    content_html = "\n\n".join(content_parts)

    if not TEMPLATE.exists():
        print("Template missing; create index.template.html")
        return

    tpl = TEMPLATE.read_text(encoding="utf-8")
    out = tpl.replace("{{name}}", data.get("name", "")).replace("{{tag}}", data.get("tag", "")).replace("{{email}}", data.get("email", "")).replace("{{resume_link}}", data.get("resume_file", PDF_NAME))
    out = out.replace("{{content_html}}", content_html)

    OUT_HTML.write_text(out, encoding="utf-8")
    print(f"Generated {OUT_HTML}")


if __name__ == "__main__":
    main()
