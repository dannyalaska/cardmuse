
import requests
import time
import os
import re
import glob
import json

COMFY_API_URL = "http://localhost:8188"
WORKFLOW_PATH = "/Users/dmcg/Desktop/card generator/cardmuse_one.json"
OUTPUT_DIR = "/Users/dmcg/ComfyUI/output"

def clean_flux_prompt(text):
    text = re.sub(r"[\*\_\[\]\(\)\{\}\#\|<>]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def get_new_matching_image(prompt, start_time, used_seeds=None):
    if used_seeds is None:
        used_seeds = set()
    time.sleep(5)
    for _ in range(240):  # Wait up to 120 seconds
        images = glob.glob(os.path.join(OUTPUT_DIR, "*.png"))
        images = sorted(images, key=os.path.getmtime, reverse=True)
        for img_path in images:
            if os.path.getmtime(img_path) < start_time:
                continue

            json_path = img_path.replace(".png", ".json")
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r") as f:
                        data = json.load(f)
                    metadata_prompt = data.get("prompt", "").strip()
                    seed = str(data.get("seed", ""))

                    if metadata_prompt and prompt.strip() in metadata_prompt and seed not in used_seeds:
                        print(f"✅ Found matching image for prompt (seed {seed})")
                        return img_path, seed
                except Exception as e:
                    print("⚠️ Error reading metadata:", e)
        time.sleep(2)
    return None, None

def generate_card_image(prompt_text, used_seeds=None):
    clean_prompt = clean_flux_prompt(prompt_text)
    print("⚙️ Preparing to send full workflow with prompt:", clean_prompt)

    try:
        with open(WORKFLOW_PATH, "r") as f:
            workflow = json.load(f)

        if "7" in workflow:
            workflow["7"]["inputs"]["text"] = clean_prompt
        else:
            return None, None, "(Workflow Error: Node 7 not found)"

        start_time = time.time()
        res = requests.post(f"{COMFY_API_URL}/prompt", json={"prompt": workflow})

        if not res.ok:
            return None, None, f"(Image Gen Error: {res.status_code} — {res.text})"

        matched_image, seed = get_new_matching_image(clean_prompt, start_time, used_seeds)
        if matched_image:
            return matched_image, seed, None

        return None, None, "(Image Gen Timeout — no matching image found)"
    except Exception as e:
        return None, None, f"(Image Gen Exception: {e})"
