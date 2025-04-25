
import json
import re

def extract_metadata_from_llm(chat):
    fallback_prompt = ""
    fallback_keywords = [
        "front of card", "card cover", "card design", "cover design",
        "card front", "cover", "outside design", "greeting card design", "card illustration"
    ]

    for msg in reversed(chat):
        if msg["role"] == "assistant":
            content = msg["content"]
            lines = content.split("\n")
            for i, line in enumerate(lines):
                clean_line = line.lower().strip()
                if any(keyword in clean_line for keyword in fallback_keywords):
                    # Capture the full block after this line (up to next empty line or max 10 lines)
                    extracted_lines = []
                    for j in range(i, min(i + 10, len(lines))):
                        current = lines[j].strip()
                        if not current:
                            break
                        # Remove markdown styling like **bold**
                        cleaned = re.sub(r"[*_~`]", "", current)
                        extracted_lines.append(cleaned)
                    fallback_prompt = " ".join(extracted_lines)
                    break
            if fallback_prompt:
                break

    return {
        "occasion": None,
        "recipient": None,
        "style": None,
        "fallback_prompt": fallback_prompt.strip() if fallback_prompt else None
    }
