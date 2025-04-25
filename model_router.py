
import requests
from config import ANTHROPIC_API_KEY

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL = "claude-3-7-sonnet-20250219"
HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "Content-Type": "application/json"
}

def call_chat_model(messages, temperature=0.7):
    return _call_claude(messages, temperature, context="chat")

def call_metadata_model(messages):
    try:
        res = requests.post("http://localhost:1234/v1/chat/completions", json={
            "model": "phi-3",
            "messages": messages,
            "temperature": 0.0
        })
        print("📡 Phi-3 metadata status:", res.status_code)
        print("🧾 Phi-3 raw response:", res.text)
        return res.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("❌ Phi-3 metadata error:", e)
        return "{}"

def call_image_prompt_model(messages):
    flux_header = {
        "role": "system",
        "content": (
            "You are a professional image prompt writer for the Flux 1 Dev model. "
            "Your job is to write a single-line visual prompt for a greeting card cover. "
            "Use vivid artistic language — style, colors, composition. Do NOT return text content, titles, or explanations. "
            "Just the one-line image prompt."
        )
    }

    full_prompt = [flux_header] + messages[-6:]
    try:
        print("🔍 Sending image_prompt request to Claude (Sonnet 3.7)...")
        res = requests.post(ANTHROPIC_API_URL, headers=HEADERS, json={
            "model": CLAUDE_MODEL,
            "max_tokens": 1024,
            "temperature": 0.6,
            "messages": full_prompt
        })

        print("📡 Claude status (image_prompt):", res.status_code)
        print("📦 Claude raw response (image_prompt):", res.text)
        data = res.json()

        if "content" in data and isinstance(data["content"], list) and data["content"]:
            text = data["content"][0]["text"].strip()
            if text:
                print("🎨 Claude image prompt:", text)
                return text
        print("⚠️ Claude returned no usable content (image_prompt)")

        # Fallback from recent assistant message
        for msg in reversed(messages):
            if msg["role"] == "assistant" and len(msg["content"]) > 30:
                lines = [line.strip() for line in msg["content"].split("\n") if 20 < len(line) < 180]
                visual_lines = [line for line in lines if any(w in line.lower() for w in ["design", "layout", "background", "illustration", "color", "composition", "art"])]
                if visual_lines:
                    fallback = visual_lines[0]
                    print("🪄 Using fallback line from assistant message:", fallback)
                    return fallback
        return "(Claude error — and no fallback found)"
    except Exception as e:
        print("❌ Claude image prompt error:", e)
        return "(Claude exception)"

def _call_claude(messages, temperature, context="general"):
    try:
        system_prompt = None
        cleaned = []
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                cleaned.append(msg)

        payload = {
            "model": CLAUDE_MODEL,
            "max_tokens": 1024,
            "temperature": temperature,
            "messages": cleaned
        }
        if system_prompt:
            payload["system"] = system_prompt

        print(f"🔍 Sending {context} request to Claude (Sonnet 3.7)...")
        res = requests.post(ANTHROPIC_API_URL, headers=HEADERS, json=payload)
        print(f"📡 Claude status ({context}):", res.status_code)
        print(f"📦 Claude raw response ({context}):", res.text)

        data = res.json()
        if "content" in data and isinstance(data["content"], list) and data["content"]:
            print(f"✅ Claude returned content ({context}):", data["content"][0]["text"])
            return data["content"][0]["text"].strip()
        print(f"⚠️ Claude returned no usable content ({context})")
        return "(Claude error)"
    except Exception as e:
        print(f"❌ Claude {context} Error:", e)
        return "(Claude error)"
