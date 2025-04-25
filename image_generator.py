
import requests
import time
import os
import re
import glob
import json
from PIL import Image

COMFY_API_URL = "http://localhost:8188"
WORKFLOW_PATH = "/Users/dmcg/Desktop/card generator/cardmuse_one.json"
SEEN_PROMPTS = {}

def get_new_matching_image(prompt, start_time, directory="/Users/dmcg/ComfyUI/output", timeout=120):
    deadline = time.time() + timeout
    while time.time() < deadline:
        files = sorted(
            [f for f in glob.glob(os.path.join(directory, "*.png")) if os.path.getmtime(f) > start_time],
            key=os.path.getmtime,
            reverse=True
        )
        for path in files:
            try:
                img = Image.open(path)
                meta = img.text
                embedded_prompt = meta.get("prompt", "").strip().lower()
                seed = meta.get("seed", "unknown")
                if embedded_prompt and embedded_prompt == prompt.strip().lower():
                    if (prompt, seed) not in SEEN_PROMPTS:
                        SEEN_PROMPTS[(prompt, seed)] = path
                        return path
            except Exception:
                continue
        time.sleep(3)
    return None

def clean_flux_prompt(text):
    text = re.sub(r"[\*\_\[\]\(\)\{\}\#\|<>]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def generate_card_image(prompt_text):
    clean_prompt = clean_flux_prompt(prompt_text)
    print("⚙️ Preparing to send full workflow with prompt:", clean_prompt)

    try:
        with open(WORKFLOW_PATH, "r") as f:
            workflow = json.load(f)

        if "7" in workflow:
            workflow["7"]["inputs"]["text"] = clean_prompt
        else:
            return None, "(Workflow Error: Node 7 not found)"

        start_time = time.time()
        res = requests.post(f"{COMFY_API_URL}/prompt", json={"prompt": workflow})

        if not res.ok:
            return None, f"(Image Gen Error: {res.status_code} — {res.text})"

        matched_image = get_new_matching_image(clean_prompt, start_time)
        if matched_image:
            return matched_image, None

        return None, "(Image Gen Timeout — no matching image found)"
    except Exception as e:
        return None, f"(Image Gen Exception: {e})"
