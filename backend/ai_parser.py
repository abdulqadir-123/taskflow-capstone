"""
AI Quick-Add parser.

This module converts natural English into a structured task. It intentionally
has no mandatory external API key, so the application works locally.
The README documents how to replace this parser with an LLM while preserving
the same structured output contract.
"""
import re
from datetime import date, timedelta

PRIORITIES = {
    "urgent": "urgent", "asap": "urgent", "critical": "urgent",
    "high": "high", "important": "high",
    "low": "low",
    "medium": "medium", "normal": "medium",
}

def parse_quick_add(text: str):
    original = text.strip()
    low = original.lower()

    priority = "medium"
    for word, value in PRIORITIES.items():
        if re.search(rf"\b{re.escape(word)}\b", low):
            priority = value
            break

    status = "todo"
    if re.search(r"\b(done|completed|complete)\b", low):
        status = "done"
    elif re.search(r"\b(in progress|ongoing|started)\b", low):
        status = "in_progress"

    due_date = None
    today = date.today()
    if "today" in low:
        due_date = today.isoformat()
    elif "tomorrow" in low:
        due_date = (today + timedelta(days=1)).isoformat()
    else:
        m = re.search(r"\b(?:by|on)\s+(\d{4}-\d{2}-\d{2})\b", low)
        if m:
            due_date = m.group(1)
        else:
            weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
            for i, day in enumerate(weekdays):
                if re.search(rf"\b{day}\b", low):
                    delta = (i - today.weekday()) % 7
                    delta = 7 if delta == 0 else delta
                    due_date = (today + timedelta(days=delta)).isoformat()
                    break

    title = original
    title = re.sub(r"^\s*(create|add|make|new)\s+(a\s+)?(task\s+)?", "", title, flags=re.I)
    title = re.sub(r"\b(urgent|asap|critical|high|important|low|medium|normal)\s*(priority)?\b", "", title, flags=re.I)
    title = re.sub(r"\bby\s+(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|\d{4}-\d{2}-\d{2})\b", "", title, flags=re.I)
    title = re.sub(r"\bon\s+\d{4}-\d{2}-\d{2}\b", "", title, flags=re.I)
    title = re.sub(r"\s+", " ", title).strip(" .,:;-")
    if not title:
        title = original

    return {
        "title": title[:200],
        "description": f"Created via Quick Add: {original}",
        "status": status,
        "priority": priority,
        "due_date": due_date,
        "source": "quick_add",
        "confidence": 0.85,
    }
